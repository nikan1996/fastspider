from fastspider.core.model import Request
from fastspider.spider import DefaultSpider


class ToScrapeV1(DefaultSpider):
    name = 'toscrape'
    version = 'v1'
    spider_config = {
    }

    def run(self):
        r = Request(url="https://www.baidu.com/", method="GET")
        response = self.send(r)
        print(response.text())


if __name__ == '__main__':
    script = ToScrapeV1()
    script.run()
