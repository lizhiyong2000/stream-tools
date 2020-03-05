import datetime
import hashlib
import logging
import os
import queue
import subprocess
import threading
import time
import traceback
from pathlib import Path
from queue import Queue
from urllib.parse import urlparse

from bson.objectid import ObjectId

import requests

from common import JSONEncoder
from config import Config
from log import start_thread_logging, stop_thread_logging


class ThumbIndexJob(threading.Thread):

    def __init__(self, thumb_path, mongo):
        threading.Thread.__init__(self)
        self.thumb_path = thumb_path
        self.mongo = mongo
        self.queue = Queue(Config.THUMB_WORKDER_COUNT)
        self.running_job = True

    def run(self):

        log_handler = start_thread_logging()

        if not os.path.exists(self.thumb_path):
            os.makedirs(self.thumb_path)

        for i in range(0, Config.THUMB_WORKDER_COUNT):
            worker = ThumbDownloadWorker(self.queue, self.thumb_path, self.mongo)
            worker.setName("THUMB_WORKER-{}".format(i + 1))
            worker.start()

            logging.info(' {} started...............'.format(worker.getName()))

        full_count = 0

        while self.running_job:

            if self.queue.full():
                logging.info('queue full:{}, {}- {}'.format(self.queue.qsize(),self.queue.maxsize, full_count))
                time.sleep(3)
                full_count += 1
                continue


            full_count = 0
            try:

                interval_time = time.mktime(datetime.datetime.now().timetuple()) - 60*60*2

                logging.info("query by time < {}".format(interval_time))

                result = self.mongo.db.playitems.find({"$or":[{"thumb_time": {"$exists": False}},{"thumb_time": {"$lt": interval_time}} ]}).sort([("thumb_success", -1), ("thumb_time", -1)]).limit(Config.THUMB_WORKDER_COUNT)

                logging.info('{} url to thumb: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), result.count()))


                if result.count() == 0:

                    time.sleep(60)
                else:

                    for s in result:
                        logging.info(JSONEncoder().encode(s))


                        # output.append(s)
                        self.queue.put([s['_id'], s['url']], block=True, timeout=None)

                        logging.info('url in queue:{}'.format(self.queue.qsize()))

            except Exception as ex:
                traceback.print_exc()
                logging.error('queue except:{}, {}'.format(self.queue.qsize(), self.queue.maxsize))
                pass

        stop_thread_logging(log_handler)


class ThumbDownloadWorker(threading.Thread):
    def __init__(self, queue, download_path, mongo):
        threading.Thread.__init__(self)

        self.queue = queue
        self.download_path = download_path
        self.mongo = mongo
        self.thread_stop = False

    def run(self):

        log_handler = start_thread_logging()

        while not self.thread_stop:

            try:
                task=self.queue.get(block=True, timeout=10)#接收消息

                logging.info("\n\n----------------------------------------------")

                logging.info("task recv:%s ,task url:%s" % (task[0], task[1]))

                self.download_and_index(task[0], task[1])

                self.queue.task_done()

            except queue.Empty:
                logging.error("%s: waiting for task" %(self.name))
                time.sleep(60)
            except Exception as ex:
                logging.error("%s: exception for task" %(self.name))
                pass
            except:
                pass

        stop_thread_logging(log_handler)

    def download_and_index(self, id, url):

        logging.info("[Thread] start:{}".format(url))

        download_path = self.download_path

        try:

            all_content = requests.get(url, timeout=1).text
        except:

            self.index_thumb(id, url, path='')
            return

        # logging.info("all_content:" + all_content)

        file_line = all_content.splitlines()

        if not file_line or len(file_line) == 0:
            self.index_thumb(id, url, path='')

            logging.error("get m3u8 failed:{}".format(url))
            raise Exception(u"获取M3U8失败")
        # 通过判断文件头来确定是否是M3U8文件
        if file_line[0] != "#EXTM3U":
            self.index_thumb(id, url, delete=True, path='')

            logging.error("not m3u8 url:{}".format(url))
            raise Exception(u"非M3U8的链接")

        for index, line in enumerate(file_line):
            if "EXTINF" in line or "EXT-X-STREAM-INF" in line:
                # 拼出ts片段的URL
                pd_url = file_line[index + 1]

                inner_url = self.get_inner_url(url, pd_url)

                logging.info(inner_url)

                if pd_url.find('.ts') > 0:
                    ret, path, resolution = self.download_ts_file(url, inner_url, download_path)

                    if ret:
                        logging.info("[OK-TS]: id:{}, url {}, path {}, resolution:{}".format(id, url, path, resolution))
                        self.index_thumb(id, url, path=path, resolution=resolution)
                    else:

                        logging.error("[ERROR-TS]: id:{}, url {}, path {}".format(id, url, path))
                        self.index_thumb(id, url)

                else:

                    # logging.error("not ts url:{}, pd_url:{}".format(url, pd_url))
                    # raise Exception(u"no ts url found in m3u8")

                    self.queue.put([id, inner_url], block=True, timeout=None)

                break

    def index_thumb(self, id, url, delete=False, path=None, resolution=None):
        logging.info("[Index-Thumb]{}: {}".format(id, url))
        try:
            myquery = {"_id": ObjectId(id)}
            #
            # if delete:
            #     self.mongo.db.playitems.delete_one(myquery)
            #     return

            if path:
                file_name = Path(path).name
            else:
                file_name = ''

            thumb_resolution = ''

            if resolution:

                thumb_resolution = resolution

            if len(file_name) > 0:

                doc = {
                    "thumb_time": time.mktime(datetime.datetime.now().timetuple()),
                    "thumb": file_name,
                    "thumb_success": len(file_name) > 0,
                    "thumb_resolution": thumb_resolution,
                    "thumb_failed_count": 0

                }

                updateQuery = {'$set': doc}

                logging.info("[OK-MONGO]:{}".format(id))

                result = self.mongo.db.playitems.update_one(myquery, updateQuery, upsert=False)

                logging.info("[UPDATE-MONGO:matched-{}, modified-{}]".format(result.matched_count, result.modified_count))


            else:
                doc = {
                    "thumb_time": time.mktime(datetime.datetime.now().timetuple()),
                    "thumb": file_name,
                    "thumb_success": len(file_name) > 0,
                    "thumb_resolution": thumb_resolution,

                }
                updateQuery = {'$set': doc, '$inc': {"thumb_failed_count": 1}}

                self.mongo.db.playitems.update_one(myquery, updateQuery, upsert=False)

        except Exception as ex:
            traceback.print_exc()
            logging.error("index_thumb {} error for url :{}".format(id, url))
            pass

    @staticmethod
    def get_inner_url(url, path):

        base_url = url.rsplit('/', 1)[0]

        if path.startswith('http'):
            return path
        else:
            return '%s/%s' % (base_url, path)

    @staticmethod
    def md5_filepath(filepath):

        hl = hashlib.md5()
        hl.update(filepath.encode(encoding='utf-8'))

        return hl.hexdigest()



    @staticmethod
    def download_ts_file(m3u8, ts_url, download_dir):

        o = urlparse(ts_url)

        # logging.info(o.path)

        file_name = o.path[o.path.rfind('/'):]
        logging.info('[file_name]:{}'.format(file_name))
        curr_path = '%s%s' % (download_dir, file_name)

        thumb_name = ThumbDownloadWorker.md5_filepath(m3u8)

        thumb_path = os.path.join(download_dir, '%s.jpg' % (thumb_name))
        logging.info('[download]:{}'.format(ts_url))
        logging.info('[target]:{}'.format(curr_path))
        # if os.path.isfile(curr_path):
        #     logging.info('[warn]: file already exist')
        #     return True, curr_path
        try:
            res = requests.get(ts_url, timeout=(5, 30))

            logging.info('[requests]: status_code{}'.format(res.status_code))

            if res.status_code != 200:

                return False, None, None

            with open(curr_path, 'ab') as f:
                # if key and len(key): # AES 解密
                #     cryptor = AES.new(key, AES.MODE_CBC, key)
                #     f.write(cryptor.decrypt(res.content))
                # else:
                f.write(res.content)

                f.flush()
            # logging.info('[OK]: {} saved'.format(curr_path))

            logging.info("[thumb]ts:{},thumb path:{}".format(curr_path, thumb_path))


            ## ffmpeg -v -ss '00:00:01.000' -vframes 1 -i
            command = ['ffmpeg',
                       '-y',
                       '-v', 'error',
                       '-i', curr_path,
                       '-ss', '00:00:01.000',
                       # '-vf', 'scale="256:192"'
                       '-vframes', '1',
                       thumb_path
                       ]

            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            (stdoutdata, stderrdata) = process.communicate()


            logging.info('[FFMPEG]:{}{}'.format(stdoutdata, stderrdata))


            thumb_resolution = None

            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                logging.info("[Success]:{}".format(curr_path))

                os.remove(curr_path)
                #ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0

                try:
                    command = ['ffprobe',
                               '-v', 'error',
                               '-select_streams', 'v:0',
                               '-show_entries', 'stream=width,height',
                               '-of', 'csv=s=x:p=0',
                               thumb_path
                               ]

                    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    (stdoutdata, stderrdata) = process.communicate()

                    logging.info('[FFMPROB]:{}{}'.format(stdoutdata, stderrdata))

                    if stdoutdata and len(stdoutdata) > 0:
                        logging.info("[thumb_resolution]:{}-{}".format(stdoutdata, curr_path))

                        thumb_resolution = stdoutdata.decode('utf-8').strip()
                except:
                    pass

                return True, thumb_path, thumb_resolution
            else:
                logging.error("[Failed]:{}".format(curr_path))
                return False, None, None

        except Exception as es:
            logging.error('[warn]: download error:{}'.format(ts_url))
            logging.error('[warn]: {} deleted'.format(curr_path))
            logging.error(es)
            traceback.print_stack()
            try:
                os.remove(curr_path)
            except:
                pass

            return False, None, None