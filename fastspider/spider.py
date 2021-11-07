from loguru import logger

from fastspider.config import downloader_in_queue_local, downloader_out_queue_local
from fastspider.core.model import Request, Response
from fastspider.run import run_local_downloader_in_thread


class DefaultSpider:
    name = 'default'
    version = 'default'
    default_config = {
        'download_concurrency': 10,
        'parse_concurrency': 10,
        'headers': {
            'User-Agent': 'DefaultSpider',
        }
    }
    spider_config = {}

    def __init__(self):
        run_local_downloader_in_thread()
        logger.info(f"name:{self.name},version:{self.version}")

    def run(self):
        raise NotImplementedError

    def send(self, request: Request) -> Response:
        downloader_in_queue_local.put(request.serialize())
        data = downloader_out_queue_local.get()
        resp = Response.deserialize(data)
        return resp
