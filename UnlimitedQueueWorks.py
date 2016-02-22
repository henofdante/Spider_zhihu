# -*- coding: utf-8 -*-
# queue

import queue
from Database   import Database
from User       import User

class UnlimitedQueueWorks:

    def __init__(self):
        self.queue = queue.Queue()

    def push(self, user, database):
        self.queue.put(user)
        database.saveUser(User(user=user))

    def pop(self):
        return self.queue.get()

    def isEmpty(self):
        if 0 == len(self.queue):
            return True
        else:
            return False
