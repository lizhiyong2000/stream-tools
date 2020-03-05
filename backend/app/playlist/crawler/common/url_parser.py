from bs4 import BeautifulSoup


def default_tag_filter(tag):
    return tag.name == 'a' and tag.has_attr('href')


def default_url_getter(tag):
    return tag.get('href')


def default_name_getter(tag):
    return tag.get_text()


class UrlParser:
    """
    Parser that extracts hrefs
    """

    def __init__(self, tag_filter=default_tag_filter, url_getter=default_url_getter,
                 url_name_getter=default_name_getter, charset='utf-8'):
        self.tag_filter = tag_filter
        self.url_getter = url_getter
        self.url_name_getter = url_name_getter
        self.url_map = {}
        self.charset = charset

    def parse(self, html):
        soup = BeautifulSoup(html, 'lxml')

        tags = soup.find_all(self.tag_filter)

        # print(tags)

        self.url_map = {self.url_getter(tag): self.url_name_getter(tag) for tag in tags}

        # print(self.url_map)
