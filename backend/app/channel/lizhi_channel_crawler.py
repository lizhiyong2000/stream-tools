import os
import urllib
from urllib.parse import urlparse

import pymongo

from channel.channel_crawler import ChannelCrawler
from channel.channel_parser import ChannelParser
from config import Config
from playlist.crawler.common.url_parser import UrlParser

result_map = {}

tag_filter = lambda tag: tag.name == 'div' and tag.has_attr('class') and tag.get('class')[0] == 'channel-item'
name_getter = lambda tag: tag.find_all("p")[0].get_text()

thumb_getter = lambda tag: "http://www.lizhizu.com{}".format(tag.find_all("img")[0].get('data-echo'))

channel_parser = ChannelParser(tag_filter=tag_filter,
                       name_getter=name_getter, thumb_getter=thumb_getter)


page_url_base = 'http://www.lizhizu.com/channel?p={}'

crawler = ChannelCrawler(parser=channel_parser)

for i in range(16, 0, -1):

    page_url = page_url_base.format(i)

    crawler.crawl(page_url)

    # print(crawler.channel_map)

    for name, thumb in crawler.channel_map.items():
        result_map[name] = thumb

print(result_map)

mongodb_url = Config.MONGO_URI
mongo_client = pymongo.MongoClient(mongodb_url)
data_list = mongo_client['freeiptv']['channels']


def save_image(img_url, file_dir):
    try:

        url = urlparse(img_url)
        file_name = os.path.basename(url.path)

        #是否有这个路径
        if not os.path.exists(file_dir):
            #创建路径
            os.makedirs(file_dir)
            #获得图片后缀
        #拼接图片名（包含路径）
        file_path = os.path.join(file_dir, file_name)
        print(file_path)
        #下载图片，并保存到文件夹中
        urllib.request.urlretrieve(img_url, filename=file_path)

        return file_name

    except IOError as e:
        print("IOError")
    except Exception as e:
        print("Exception")



filepath = os.path.abspath(__file__)

path = os.path.join(os.path.dirname(filepath), "../../../frontend/public/images/channels")


for name, thumb in result_map.items():

    print("[Index-Channel]: {}".format(name))

    file_name = save_image(thumb, path)


    myquery = {"name": name}

    doc = {
        "name": name,
        "thumb": "{}".format(file_name)
    }
    data_list.update_one(myquery, {'$set': doc}, upsert=True)