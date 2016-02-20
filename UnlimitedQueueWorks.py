# -*- coding: utf-8 -*-
# queue

import queue

class UnlimitedQueueWorks:

    def __init__(self):
        self.queue = queue.Queue()

    def push(self, obj):
        self.queue.put(obj)

    def pop(self):
        return self.queue.get()

    def isEmpty(self):
        if 0 == len(self.queue):
            return True
        else:
            return False
