import os


class PlaylistCrawler:

    result_path = os.path.join(os.getcwd(), "result", "playlist")

    def __init__(self):
        self.result_map = {}
        self.name = ''
        self.base_url = ''
        self.root_url = ''

    def crawl(self, name='playlist', base_url='', root_url=''):

        self.name = name
        self.base_url = base_url
        self.root_url = root_url
        self.result_map = {}

        try:
            self._crawl_page(base_url)
        except Exception as ex:
            print(ex)

        print("playlist :{}, result:{}".format(name, self.result_map))

        self.generate_m3u8_file()

    def _crawl_page(self, page_url):
        print('_crawl_page')
        pass

    def generate_m3u8_file(self):

        # converter = Converter('zh-hans')
        result_path  = PlaylistCrawler.result_path

        if not os.path.exists(result_path):

            os.makedirs(result_path)

        with open(os.path.join(result_path, '{}-playlist.m3u8'.format(self.name)), 'wb') as f:

            f.write(b'#EXTM3U\n\n')

            for channel, urls in self.result_map.items():
                name = '#EXTINF:-1,' + channel + '\n'

                if isinstance(urls, list):
                    for url in urls:

                        if url and len(url) > 0:
                            link = url + '\n\n'

                            f.write(name.encode(encoding='utf8'))
                            f.write(link.encode(encoding='utf8'))
                # elif isinstance(urls, str):
                #     link = urls + '\n\n'
                #
                #     f.write(name.encode(encoding='utf8'))
                #     f.write(link.encode(encoding='utf8'))
