import requests

class RequestDownloader:

    def __init__(self, in_queue, out_queue):
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            self.in_queue.get()

    def produce_response(self):

