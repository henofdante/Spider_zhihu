# -*- coding: utf-8 -*-
#rebuild spider
import os

from zhihu                  import ZhihuClient
from threading              import Thread

from UnlimitedQueueWorks    import UnlimitedQueueWorks
from User                   import User
from Database               import Database


class Spider:

    def __init__(self):
        '''

        '''
        # 登陆对象
        self.client = None
        # 队列对象
        self.queue = UnlimitedQueueWorks()
        # 运行状态
        self.onRunning = True
        # database对象
        self.database = Database()


    def login(self, cookie='cookie.json'):
        '''
        从cookie中登陆，若cookie不存在，手动登陆
        '''
        client = ZhihuClient()
        if cookie == None:
            cookie = ''

        if os.path.exists(cookie):
            client.login_with_cookies(cookie)
        else:
            client.create_cookies(cookie)
        self.client = client


    def mainLoop(self, poolSize):
        '''
        多线程执行下载，使用类线程池模型
        '''
        
        # 开启队列
        self.queue.push()# a user
        # 启动线程池
        pool = []
        for _ in range(poolSize):
            pool.append(Thread(target=self._downloadUser))
            pool[-1].start()

        # 等待执行完毕
        for singleThread in pool:
            singleThread.join()


    def _downloadUser(self):
        '''
        下载单个用户线程，循环从队列中取用户，并向队列中加入下载的用户
        下载后加入缓存等待写入硬盘
        '''
        while self.onRunning:
            currentUser = self.queue.pop()
            cnt = 0

            # 下载&入队
            for newUser in currentUser.followees:
                self.queue.push(newUser)
                cnt += 1

            # 验证
            if cnt == currentUser.followee_num:
                # 储存
                self.database.setUser(currentUser)
            else:
                # 重入队
                self.queue.push(currentUser)




    def displayStatus(self):
        '''
        输出循环，显示下载状态
        '''



spider = Spider()
spider.login()
spider.mainLoop()