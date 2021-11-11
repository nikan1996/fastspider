from fastspider.core.model import Request
from fastspider.spider import DefaultSpider

class ToScrapeV1(DefaultSpider):
    name = 'toscrape'
    version = 'v1'
    spider_config = {
    }

    def run(self):
        for i in range(10):
            r = Request(url="https://www.baidu.com/", method="GET")
            response = self.send(r,callback=)
            print(response.text())
            print(response.cookies)

    def callback(self):

if __name__ == '__main__':
    script = ToScrapeV1()
    script.run()
