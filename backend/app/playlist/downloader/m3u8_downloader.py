import base64
import os
import subprocess
import threading
import traceback
import urllib

import requests
from Crypto.Cipher import AES

from playlist.crawler.common.url_crawler import UrlCrawler

"""
下载M3U8文件里的所有片段
"""
def get_file_content(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


class M3u8Downloader(threading.Thread):
    def __init__(self, url, download_path):
        threading.Thread.__init__(self)
        self.url = url
        self.download_path = download_path
        self.key = None

    def run(self):

        download_path = self.download_path

        if not os.path.exists(download_path):
            os.mkdir(download_path)

        if self.url.startswith("http"):

            all_content = UrlCrawler.curl(self.url)

        elif self.url.startswith("/"):
            all_content = get_file_content(self.url)

        # print(all_content)

        file_line = all_content.splitlines()

        if not file_line or len(file_line) == 0:
            raise BaseException(u"获取M3U8失败")
        # 通过判断文件头来确定是否是M3U8文件
        if file_line[0] != "#EXTM3U":
            raise BaseException(u"非M3U8的链接")

        for index, line in enumerate(file_line):

            if "#EXT-X-KEY" in line:  # 找解密Key
                method_pos = line.find("METHOD")
                comma_pos = line.find(",")
                if comma_pos == -1:
                    comma_pos = len(line)
                method = line[method_pos:comma_pos].split('=')[1]
                print("Decode Method：", method)

                if method != 'NONE':
                    uri_pos = line.find("URI")
                    quotation_mark_pos = line.rfind('"')
                    key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

                    key_url = self.get_inner_url(self.url, key_path)# 拼出key解密密钥URL
                    self.key = UrlCrawler.curl(key_url)
                    print("key：", self.key)

            if "EXTINF" in line or "EXT-X-STREAM-INF" in line:
                # 拼出ts片段的URL
                pd_url = file_line[index + 1]

                inner_url = self.get_inner_url(self.url, pd_url)

                if pd_url.find('.ts') > 0:
                    ret, path = self.download_ts_file(self.url, inner_url, download_path, self.key)

                    if ret:
                        print("[OK]: url {}, path {}".format(self.url, path))
                        break
                else:
                    M3u8Downloader(inner_url, download_path).start()



    @staticmethod
    def get_inner_url(url, path):

        base_url = url.rsplit('/', 1)[0]

        if path.startswith('http'):
            return path
        else:
            return '%s/%s' % (base_url, path)

    @staticmethod
    def download_ts_file(m3u8, ts_url, download_dir, key):

        file_name = ts_url[ts_url.rfind('/'):]
        print('[file_name]:', file_name)
        curr_path = '%s%s' % (download_dir, file_name)

        thumb_name = bytes.decode(base64.b64encode(m3u8.encode(encoding="UTF-8")))

        thumb_path = os.path.join(download_dir, '%s.jpg' % (thumb_name))
        print('[download]:', ts_url)
        print('[target]:', curr_path)
        if os.path.isfile(curr_path):
            print('[warn]: file already exist')
            return True, curr_path
        try:
            res = requests.get(ts_url)
            with open(curr_path, 'ab') as f:
                if key and len(key): # AES 解密
                    cryptor = AES.new(key, AES.MODE_CBC, key)
                    f.write(cryptor.decrypt(res.content))
                else:
                    f.write(res.content)

                f.flush()
            print('[OK]: {} saved'.format(curr_path))

            print("thumb path:{}".format(thumb_path))

            command = [ 'ffmpeg',
                        '-y',
                        '-i', curr_path,
                        '-ss', '00:00:01.000',
                        '-vframes', '1',
                        thumb_path
                        ]

            process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

            (stdoutdata, stderrdata) = process.communicate()

            print(stdoutdata)

            print(stderrdata)

            os.remove(curr_path)
            if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:

                return True, thumb_path
            else:

                return False, None
        except Exception as es:
            print('[warn]: download error:{}'.format(ts_url))
            print('[warn]: {} deleted'.format(curr_path))
            print(es)
            traceback.print_stack()
            os.remove(curr_path)

            return False, None


if __name__ == '__main__':
    m3u8_url = "https://raw.githubusercontent.com/lizhiyong2000/stream-tools/master/resource/%E7%94%B5%E5%BD%B1-playlist.m3u8"

    # m3u = m3u8.load('http://161.0.157.5/PLTV/88888888/224/3221226253/03.m3u8')
    #
    # m3u2 = m3u8.load(m3u8_url)

    download_path = os.getcwd() + "/download"
    M3u8Downloader(url=m3u8_url, path=download_path).start()
