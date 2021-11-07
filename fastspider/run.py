import threading

from fastspider.config import downloader_in_queue_local, downloader_out_queue_local
from fastspider.core.downloader.requestsdownloader import RequestDownloader
from loguru import logger


def run_local_downloader():
    r = RequestDownloader(downloader_in_queue_local, downloader_out_queue_local)
    r.run()


_start_local_downloader = False


def run_local_downloader_in_thread():
    global _start_local_downloader
    if not _start_local_downloader:
        t = threading.Thread(target=run_local_downloader, daemon=True)
        t.start()
        logger.info('Local downloader is running in background..')
        _start_local_downloader = True


if __name__ == '__main__':
    pass
