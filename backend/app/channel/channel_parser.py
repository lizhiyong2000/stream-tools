from bs4 import BeautifulSoup


def default_tag_filter(tag):
    return tag.name == 'a' and tag.has_attr('href')


def default_name_getter(tag):
    return tag.get_text()

def default_thumb_getter(tag):
    return tag.get('href')



class ChannelParser:
    """
    Parser that extracts hrefs
    """

    def __init__(self, tag_filter=default_tag_filter, name_getter=default_name_getter,
                 thumb_getter=default_thumb_getter, charset='utf-8'):
        self.tag_filter = tag_filter
        self.name_getter = name_getter
        self.thumb_getter = thumb_getter
        self.channel_map = {}
        self.charset = charset

    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')

        tags = soup.find_all(self.tag_filter)


        # for tag in tags:
        #
        #     print(tag.get('class')[0] == 'channel-item')

        # print(tags)

        self.channel_map = {self.name_getter(tag): self.thumb_getter(tag) for tag in tags}

        # print(self.url_map)
