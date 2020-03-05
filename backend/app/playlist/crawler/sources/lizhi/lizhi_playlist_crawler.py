import os

from playlist.crawler.common.playlist_crawler import PlaylistCrawler
from playlist.crawler.common.url_crawler import UrlCrawler
from playlist.crawler.common.url_parser import UrlParser


class LizhiPlaylistCrawler(PlaylistCrawler):
    def __init__(self):
        super().__init__()

    def crawl(self, name='playlist', base_url=''):

        self.name = name
        self.base_url = base_url
        self.result_map = {}
        page = 1

        while True:
            try:
                self._crawl_page(base_url + '?p={}'.format(page))
                page += 1
            except Exception as ex:
                print(ex)
                break

        print(self.result_map)

        self.generate_m3u8_file()


    def _crawl_page(self, page_url):

        result_map = {}

        tag_filter = lambda tag: tag.name == 'a' and tag.has_attr('title') and len(tag.find_all("p")) > 0
        url_name_getter = lambda tag: tag.find_all("p")[0].get_text()

        url_parser = UrlParser(tag_filter=tag_filter,
                               url_name_getter=url_name_getter)

        crawler = UrlCrawler(parser=url_parser)
        crawler.crawl(page_url)

        print(crawler.url_map)

        if len(crawler.url_map.items()) == 0:
            raise Exception("Failed to get url")
        #
        # html = crawler.curl('http://www.lizhizu.com/player?id=5&val=1')
        tag_filter = lambda tag: tag.name == 'a' and tag.has_attr('onclick') and tag.has_attr('data-player')
        url_getter = lambda tag: tag.attrs['data-player']
        url_parser = UrlParser(tag_filter=tag_filter, url_getter=url_getter)

        def url_mapper(url):
            parts = url.split('_')
            return 'http://www.lizhizu.com/player?id={}&val={}'.format(parts[0], parts[1])

        inner_tag_filter = lambda tag: tag.name == 'script' and not tag.has_attr('src')


        def inner_url_getter(tag):
            s = tag.get_text()
            left = s.find('$http')
            right = s.find('$m3u8')
            if right > left and left > 0:
                result=  s[left + 1:right]
                print(result)
                return result
            return ''
        inner_url_name_getter = lambda x: ''

        inner_url_parser = UrlParser(tag_filter=inner_tag_filter, url_getter=inner_url_getter, url_name_getter=inner_url_name_getter)

        # '信号1$http://223.110.243.168/PLTV/2510088/224/3221227343/1.m3u8$m3u8'
        for url, name in crawler.url_map.items():
            print('{} :{}'.format(url, name))
            result_map[name] = []
            crawler = UrlCrawler(parser=url_parser, debug=False)
            crawler.crawl(url)

            url_map = { url_mapper(k):crawler.url_map[k] for k in sorted(crawler.url_map)}

            for inner_url, inner_name in url_map.items():
                # result_map[name][inner_name] = []

                inner_crawler = UrlCrawler(parser=inner_url_parser, debug=False)
                inner_crawler.crawl(inner_url)

                for m3u8 in inner_crawler.url_map.keys():
                    print('{} {}'.format(name, m3u8))
                    if m3u8 and m3u8.endswith('m3u8'):
                        result_map[name].append(m3u8)

        for name, urls in result_map.items():
            if len(urls) > 0:
                self.result_map[name] = urls


if __name__ == "__main__":
    crawer = LizhiPlaylistCrawler()
    # crawer.crawl("中央电视台", 'http://www.lizhizu.com/channel/cctv')

    # crawer.crawl("地方电视台", 'http://www.lizhizu.com/channel/weishi')

    # crawer.crawl("港澳台电视台", 'http://www.lizhizu.com/channel/gangaotai')
    # crawer.crawl("国外电视台", 'http://www.lizhizu.com/channel/inter')
    crawer.crawl("其他综合台", 'http://www.lizhizu.com/channel/other')





