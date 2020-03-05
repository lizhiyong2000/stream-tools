import datetime
import os
import time
from os.path import isfile, join
from pathlib import Path

import pymongo

from playlist.downloader.m3u8_downloader import get_file_content, M3u8Downloader


class M3u8Indexer:
    def __init__(self, mongodb_url, db_name, collection_name):
        self.mongodb_url = mongodb_url
        self.mongo_client = pymongo.MongoClient(mongodb_url)
        self.data_list = self.mongo_client[db_name][collection_name]

    def find_all(self):
        return self.data_list.find()

    def find_by_url(self, url):
        myquery = {"url": url}
        return self.data_list.find_one(myquery)

    def find_by_tag(self, tag):

        myquery = {"tags": {"$elemMatch": {"$regex": ".*{}.*".format(tag), "$options": "i" }}}

        return self.data_list.find(myquery)

    def update_thumb(self, url, thumb):
        myquery = {"url": url}
        newvalues = {"$set": {"thumb": thumb}}
        self.data_list.update_one(myquery, newvalues)

    def save(self, url='', name='', thumb='', category='', tag=''):
        myquery = {"url": url}

        doc = {
            "url": url,
            "name": name,
            "thumb": thumb
        }
        return self.data_list.update_one(myquery, {'$set': doc, '$addToSet': {'categories': category,
                                                        'tags': tag}}, upsert=True)


    def index(self, file):

        all_content = get_file_content(file)

        file_name = Path(file).name

        category = file_name[:file_name.find("-")]

        # print(all_content)

        file_line = all_content.splitlines()

        if not file_line or len(file_line) == 0:
            raise BaseException(u"获取M3U8失败")
        # 通过判断文件头来确定是否是M3U8文件
        if file_line[0] != "#EXTM3U":
            raise BaseException(u"非M3U8的链接")

        for index, line in enumerate(file_line):


            if "EXTINF" in line:
                # 拼出ts片段的URL
                pd_name = line[line.find(",") + 1 :].strip()
                pd_url = file_line[index + 1].strip()

                self.save(url=pd_url, name=pd_name, category=category, tag=pd_name)

    def index_thumb(self, url, thumb):

        print("[Index-Thumb]: {}".format(url))
        myquery = {"url": url}

        doc = {
            "url": url,
            "thumb_time": time.mktime(datetime.datetime.now().timetuple()),
            "thumb": thumb
        }
        return self.data_list.update_one(myquery, {'$set': doc}, upsert=True)

    def delete(self, url):
        myquery = {"url": url}

        self.data_list.delete_one(myquery)

    def delete_all(self):
        self.data_list.delete_many({})


if __name__ == '__main__':
    # mongo_url = 'mongodb://192.168.2.26:32717,192.168.2.26:32727,192.168.2.26:32737/playlist?replicaSet=rs0'

    mongo_url = 'mongodb://freeiptv.cn:27070'

    indexer = M3u8Indexer(mongo_url, 'freeiptv', 'playitems')


    filepath = os.path.abspath(__file__)

    playlist_path = os.path.join(os.path.dirname(filepath), "../../../../resource")



    m3u8_files = [f for f in os.listdir(playlist_path) if isfile(join(playlist_path, f))]

    # file = os.path.join(os.path.dirname(filepath), "../../../../result/playlist/中央电视台-playlist.m3u8")

    for f in m3u8_files:
        file = os.path.join(playlist_path, f)
        indexer.index(file)

    # indexer.delete_all()
    #
    # indexer.save('url', 'new name', 'new thumb', 'new cat', 'new tag2')

    # result = indexer.find_by_tag("安徽")

    # for item in result:
    #     print(item)

    # print(list(indexer.find_all()))
