import threading
import time
from typing import Callable, Optional, Any

from loguru import logger

from fastspider.config import downloader_in_queue_local, downloader_out_queue_local
from fastspider.core.model import Request, Response
from fastspider.core.threadpool import ThreadPool
from fastspider.run import run_local_downloader_in_thread


class DefaultSpider:
    name = 'default'
    version = 'default'
    default_config = {
        'download_concurrency_limit': 10,
        'parse_concurrency_limit': 10,
        'download_concurrency_limit_global': 10 + 100,
        'parse_concurrency_limit_global': 10 + 100,
        'headers': {
            'User-Agent': 'DefaultSpider',
        }
    }
    spider_config = {}
    adjust_interval = 10 * 1000

    def __init__(self):
        run_local_downloader_in_thread()
        logger.info(f"name:{self.name},version:{self.version}")
        self.download_concurrency = 0
        self.parse_concurrency = 0
        self.lock = threading.Lock()
        self.register_spider_config()
        self.register_flag = 0
        self.last_adjust_time = time.time()
        self.send_pool = ThreadPool(max_workers=40, name=self.__class__.__name__ + '-send-')
        self.parse_pool = ThreadPool(max_workers=20, name=self.__class__.__name__ + '-parse-')
        self.other_pool = ThreadPool(max_workers=5, name=self.__class__.__name__ + '-other-')

    def run(self):
        raise NotImplementedError

    def register_spider_config(self):
        pass

    def increase_down_concurrency(self):
        self.lock.acquire()
        self.download_concurrency += 1
        self.lock.release()

    def decrease_down_concurrency(self):
        self.lock.acquire()
        self.download_concurrency -= 1
        self.lock.release()

    def increase_parse_concurrency(self):
        self.lock.acquire()
        self.parse_concurrency += 1
        self.lock.release()

    def decrease_parse_concurrency(self):
        self.lock.acquire()
        self.parse_concurrency -= 1
        self.lock.release()

    def parse_in_thread(self, callback: Optional[Callable[[Response], Any]], resp: Response):
        f = self.parse_pool.submit(callback, resp)
        f.add_done_callback(self.done_parse)

    def done_parse(self, future):
        print('parse task completed...')
        self.decrease_parse_concurrency()

    def done_send(self, future):
        print('send task completed...')
        self.decrease_down_concurrency()

    def send(self, request: Request, callback: Optional[Callable[[Response], Any], None] = None) -> Response:
        with self.lock:
            if self.register_flag:
                self.register_spider_config()
        f = self.send_pool.submit(self.send_in_thread, request, callback)
        f.add_done_callback(self.done_send)

    def send_in_thread(self, request: Request, callback: Optional[Callable[[Response], Any], None]) -> Response:
        self.increase_down_concurrency()
        downloader_in_queue_local.put(request.serialize())
        data = downloader_out_queue_local.get()
        self.decrease_down_concurrency()
        resp = Response.deserialize(data)
        # Execute callback
        self.increase_parse_concurrency()
        self.parse_in_thread(callback, resp)

        return resp
