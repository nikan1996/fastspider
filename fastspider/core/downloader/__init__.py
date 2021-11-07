import concurrent.futures


class ThreadPool:
    def __init__(self, max_workers=100):
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def close(self):
        self.pool.shutdown()


class Downloader:
    def __init__(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        pass
