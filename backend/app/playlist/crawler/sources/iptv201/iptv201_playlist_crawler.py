import os
import urllib
from urllib.request import Request, urlopen

from playlist.crawler.common.playlist_crawler import PlaylistCrawler
from playlist.crawler.common.url_crawler import UrlCrawler
from playlist.crawler.common.url_parser import UrlParser
from playlist.crawler.sources.iptv201.langconv import Converter


class Iptv201PlaylistCrawler(PlaylistCrawler):
    def __init__(self):
        super().__init__()


    def get_url(self, url):

        try:
            print("get_url retrieving url... %s, is m3u8:%s" % (url, url.find('m3u8') > 0))
            # req = Request('%s://%s%s' % (self.scheme, self.domain, url))
            req = Request(url)

            req.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.i/605.1.15')

            response = urlopen(req, timeout=10)


            # print(response.encoding)

            if response.url != req.full_url:
                print("====get_url {} result:{}".format(url, response.url))
                return response.url

            charset = 'utf-8'

            if response.headers.get_content_charset():
                charset = response.headers.get_content_charset()

            res = response.read().decode(charset, 'ignore')

            if res.startswith('#EXTM3U'):
                print("====get_url {} result:{}".format(url, url))
                return url

            print("===get_url {} result:{}".format(url, res))
            return res
        except Exception as e:
            print("get_url error %s: %s" % (url, e))
            return ''

    def _crawl_page(self, page_url):

        converter = Converter('zh-hans')

        result_map = {}

        def tag_filter(tag):
            result = (tag.name == 'a' and tag.has_attr('href'))

            if not result:
                return result

            href = tag.attrs['href']

            if href:
                return href.startswith('?act=play')

            return False

        # url_name_getter = lambda tag: tag.find_all("p")[0].get_text()

        url_parser = UrlParser(tag_filter=tag_filter)

        crawler = UrlCrawler(parser=url_parser)

        crawler.crawl(page_url)

        def url_mapper(url):
            return urllib.parse.urljoin(self.root_url, url)

        url_map = {url_mapper(k): converter.convert(crawler.url_map[k]) for k in sorted(crawler.url_map)}

        print("playlist:{} channel map:{}".format(self.name, url_map))

        tag_filter = lambda tag: tag.name == 'option' and tag.has_attr('value')

        def url_getter(tag):
            return tag.attrs['value']
        url_parser = UrlParser(tag_filter=tag_filter, url_getter=url_getter)

        second_crawler = UrlCrawler(parser=url_parser, debug=False)


        def third_tag_filter(tag):

            if tag.name != 'script' or not tag.has_attr('type'):
                return False
            try:
                tag.get_text().index("HlsJsPlayer")
            except Exception as ex:
                # print(ex)
                return False
            # print("tag text:" + tag.get_text())
            return True

        def third_url_getter(tag):
            text = tag.get_text()
            # print(text)
            try:

                left = text.index("url: '")
                right = text.index("',", left)

                innner_text = text[left+ len("url: '"):right]
                # print(innner_text)
                return innner_text
            except Exception as ex:
                # print(ex)
                return ''



        third_url_parser = UrlParser(tag_filter=third_tag_filter, url_getter=third_url_getter)
        third_crawler = UrlCrawler(parser=third_url_parser, debug=False)



        for url, name in url_map.items():

            second_crawler.crawl(url)

            print("craw url:{} result map:{} ".format(url, second_crawler.url_map))

            if len(second_crawler.url_map.items()) == 0:
                print("Failed to get url" + url)
                continue

            for m3u8 in second_crawler.url_map.keys():
                print('{} m3u8:{}'.format(name, m3u8))

                if not m3u8.find('m3u8') > 0:

                    third_crawler.crawl(m3u8)

                    if len(third_crawler.url_map.items()) == 0:
                        print("Failed to get url" + m3u8)
                        continue

                    new_m3u8_url = list(third_crawler.url_map.keys())[0]

                    new_url = self.get_url(new_m3u8_url)

                    if name in result_map.keys():

                        result_map[name].append(new_url)
                    else:
                        result_map[name] = [new_url]
                else:
                    if name in result_map.keys():

                        result_map[name].append(m3u8)
                    else:
                        result_map[name] = [m3u8]


        print(result_map)
        for inner_name, urls in result_map.items():
            if len(urls) > 0:

                # urls = [self.get_url(u) for u in urls]
                print("{} urls:{}".format(inner_name, urls))
                self.result_map[inner_name] = urls






