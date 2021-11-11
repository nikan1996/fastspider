import concurrent.futures
import time


class ThreadPool:
    def __init__(self, max_workers=100,name='default-threadpool-'):
        self.max_workers = max_workers
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix=name)
        self.idle_threads = 0
        self.name = name

    def __repr__(self):
        jobs = self.pool._work_queue.qsize()
        _threads = len(self.pool._threads)
        _idle_threads = self.pool._idle_semaphore._value
        return f"jobs:{jobs},idle_threads/current_threads:{_idle_threads}/{_threads},max_workers:{self.max_workers}"

    def submit(self,*args, **kwargs):
        return self.pool.submit(*args, **kwargs)
    def close(self):
        self.pool.shutdown()
if __name__ == '__main__':
    def s():
        time.sleep(2)
        return 5
    t = ThreadPool()
    print(t)
    t.submit(s)
    print(t)
    time.sleep(2)
    print(t)
