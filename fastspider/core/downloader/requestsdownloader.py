import concurrent.futures
import queue
import time
import traceback

import requests
import requests.utils
from loguru import logger

from fastspider.core.model import Request, Response


class RequestDownloader:

    def __init__(self, in_queue, out_queue, thread_size=50):
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_size)
        self.request_results = {}

    def run(self):
        while True:
            try:
                data = self.in_queue.get()
                request: Request = Request.deserialize(data)
                self.dispatch_request(request)
            except Exception as e:
                logger.error(traceback.format_exc())
            time.sleep(0.01)

    def _do_request(self, request: Request):
        try:
            s = requests.Session()
            r = s.request(request.method, request.url, cookies=request.cookies, headers=request.headers)
            resp = Response(r.url, r.status_code, r.content, dict(r.headers), dict(r.cookies), r.history, r.reason,)
            self.out_queue.put(resp.serialize())
        except Exception:
            logger.error(traceback.format_exc())

    def dispatch_request(self, request: Request):
        self.pool.submit(self._do_request, request)


if __name__ == '__main__':
    q1 = queue.Queue()
    q2 = queue.Queue()
    r = RequestDownloader(q1, q2)
    req1 = Request(url='https://www.baidu.com/', method='GET')
    q1.put(req1.serialize())
    r.run()
