from fastspider.core.model import Request, Task


class DefaultSpider:
    name = 'default'
    version = 'default'
    default_config = {
        'concurrency':10,
        'headers': {
            'User-Agent': 'DefaultSpider',
        }
    }
    spider_config = {}
    def send(self,request:Request):
        task = Task()
        task.set_request(request)


