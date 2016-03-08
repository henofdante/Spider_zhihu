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

        # 从硬盘恢复队列
        # for user in database.checkIntegrity():
        #     print(BASIC_ADRESS + user.id, ':')
        #     temp = client.author(BASIC_ADRESS + user.id)
        #     temp.uid = user.uid
        #     self.queue.put(temp)

    def push(self, user):

        # 分配uid
        if not hasattr(user, 'uid'):
            uid = self.database.getUid(user.id)
            if uid == None:

                with self.uidLock:
                    self.uidcounter += 1
                    user.uid = self.uidcounter
                self.database.saveUser(User(user.uid, user.id, followee_num=1))
            else:
                user.uid = uid

        self.queue.put(user)
        # print('UQW.push, self.queue.qsize():', self.queue.qsize())
        print('.', end='')

    def pop(self):
        return self.queue.get()

    def isEmpty(self):
        return self.queue.empty()
