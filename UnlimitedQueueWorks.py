# -*- coding: utf-8 -*-
# queue

import queue
from Database   import Database
from User       import User
import threading

BASIC_ADRESS = 'http://www.zhihu.com/people/'

class UnlimitedQueueWorks:

    def __init__(self, database, client):
        self.queue = queue.Queue()
        self.database = database
        self.uidcounter = database.checkLatest()
        self.uidLock = threading.Lock()
        for user in database.checkIntegrity():
            print(BASIC_ADRESS + user.id, ':')
            temp = client.author(BASIC_ADRESS + user.id)
            temp.uid = user.uid
            print(temp.name)
            self.queue.put(temp)

    def push(self, user):
        if self.database.getUid(user.id) == None:
            
            with self.uidLock:
                self.uidcounter += 1
                user.uid = self.uidcounter
            self.database.saveUser(User(user=user))
            self.queue.put(user)
            print(len(self.queue))
            
        

    def pop(self):
        return self.queue.get()

    def isEmpty(self):
        if 0 == len(self.queue):
            return True
        else:
            return False
