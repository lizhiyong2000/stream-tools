import os

from playlist.crawler.common.playlist_crawler import PlaylistCrawler
from playlist.crawler.common.url_crawler import UrlCrawler
from playlist.crawler.common.url_parser import UrlParser

#北京邮电大学ivi测试源
class BuptPlaylistCrawler(PlaylistCrawler):
    def __init__(self):
        super().__init__()

    def crawl(self, name='playlist', base_url=''):

        self.name = name
        self.base_url = base_url
        self.result_map = {}

        try:
            self._crawl_page(base_url)
        except Exception as ex:
                print(ex)

        print(self.result_map)

        self.generate_m3u8_file()

    def _crawl_page(self, page_url):

        result_map = {}

        def tag_filter(tag):
            if not tag.name == 'div':
                return False

            if len(tag.find_all("p")) > 0 and len(tag.find_all("a")) > 0:
                return True

            return False

        def url_getter(tag):
            return  tag.find_all("a")[1].get('href')

        # attr_filter = lambda x: x.has_attr('title')
        url_name_getter = lambda tag: tag.find_all("p")[0].get_text()

        url_parser = UrlParser(tag_filter=tag_filter,
                               url_getter=url_getter,
                               url_name_getter=url_name_getter)

        crawler = UrlCrawler(parser=url_parser)
        crawler.crawl(page_url)

        print(crawler.url_map)

        if len(crawler.url_map.items()) == 0:
            raise Exception("Failed to get url")

        result_map = {}

        for url, name in crawler.url_map.items():
            url = crawer.base_url + url
            print('{} {}'.format(name, url))
            if not result_map.get(name):
                result_map[name] = []
            result_map[name].append(url)

        for name, urls in result_map.items():
            if len(urls) > 0:
                self.result_map[name] = urls


if __name__ == "__main__":
    crawer = BuptPlaylistCrawler()

    crawer.crawl("北京邮电大学ivi测试源", 'http://ivi.bupt.edu.cn')





