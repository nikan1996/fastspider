class TaskManager:
    def __init__(self, storage):
        self.storage = {}  # in memory storage

    def limit(self,request,concurrency):
        pass