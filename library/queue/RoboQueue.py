import queue

class RoboQueue(object):

    def __init__(self):
        self.__queues = {}

    def create(self, name):
        q = queue.Queue()
        self.__queues[name] = q
        return q

    def get(self, name):
        return self.__queues[name]