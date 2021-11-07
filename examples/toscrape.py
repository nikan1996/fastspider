from fastspider.core.model import Request
from fastspider.spider import DefaultSpider


class ToScrapeV1(DefaultSpider):
    name = 'toscrape'
    version = 'v1'
    spider_config = {
        ''
    }
    def run(self):
        r = Request
        self.send(r)
    def parse(self,response):
        content = response.content