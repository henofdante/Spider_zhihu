# -*- coding: utf-8 -*-

__author__ = 'HenofDante'

from IPython import start_ipython
from zhihu import ZhihuClient
import os.path
import os
import json

import time
import threading
from io import StringIO
import msvcrt


def sample_code():
    client = ZhihuClient()
    cookie_file_name = 'cookie.json'
    
    people_main_page = 'http://www.zhihu.com/people/liu-shi-qi-5-21'
    if os.path.exists(cookie_file_name):
        client.login_with_cookies(cookie_file_name)
    else:
        client.create_cookies(cookie_file_name)

    me = client.author(people_main_page)

    print('id:', me.id)
    print('name:', me.name)
    print('motto:', me.motto)
    print('photo:', me.photo_url)
    print('followee number:', me.followee_num)
    print('follower number:', me.follower_num)

    start_ipython()


    followees = []
    followers = []
    for man in me.followees:
        print(man.id, '/', man.name)
        followees.append(man.id)

    for man in me.followers:
        print(man.id, '/', man.name)
        followers.append(man.id)
    print(followees)
    print(followers)

    # save = ZhihuUser(me.id, followees, followers)
    # save.save('save.json')


def multi_threading(max_threading, sleep_time, function):

    ls = []
    #cnt = 0
    while True:
        print('总线程数：', len(ls))
        while len(ls) < max_threading:
            #print('new thread created')
            ls.append(threading.Thread(target=function))
            ls[-1].start()
            #cnt += 1

        del_ls = []
        for thread in ls:
            if not thread.is_alive():
                del_ls.append(thread)
        for i in del_ls:
            ls.remove(i)

        time.sleep(sleep_time)


class ZhihuUser:

    def __init__(self, id, followees=[], followers=[], followee_num=-1, follower_num=-1):
        self.id = id
        self.followees = followees
        self.followers = followers

        if follower_num == -1:
            self.follower_num = len(self.followers)
        else:
            self.follower_num = follower_num

        if followee_num == -1:
            self.followee_num = len(self.followees)
        else:
            self.followee_num = followee_num

    def save(self, file_name):
        save_data = json.dumps(
            {'id': self.id, 'followee_num': self.followee_num, 'followees': self.followees, }) + '\n'
        with open(file_name, 'a') as f:
            # print('saving...')
            f.write(save_data)
        # print('saved')


# class ZhihuUserSet:

#     def __init__(self, init_user=None):
#         self.userset = {}
#         if init_user != None:
#             self.append(init_user)

#     def append(self, user):
#         if isinstance(user, ZhihuUser):
#             if self.userset.get(user.id) != None:
#                 self.userset[user.id] = copy.copy(user)
#                 del self.userset[user.id].id
#                 return 0  # 正常
#             else:
#                 return 1  # 错误
#         else:
#             raise TypeError

class Quit(BaseException):
    pass







class ZhihuSpider:

    status = {}

    def __init__(self, cookie=None):
        self.client = self.spider_login(cookie)
        self.people_url = 'http://www.zhihu.com/people/'
        self.work_save_file_name = 'work-save.json'
        self.queue = []  # 任务队列
        self.nameset = set()  # 已有id集合


        # 线程锁
        self.saver_lock = threading.Lock()
        self.fucklock = threading.Lock()
        self.iolock = threading.Lock()
        self.setlock = threading.Lock()

    # 爬虫登陆
    def spider_login(self, cookie=None):
        client = ZhihuClient()
        if cookie == None:
            cookie_file_name = ''
        else:
            cookie_file_name = cookie

        if os.path.exists(cookie_file_name):
            client.login_with_cookies(cookie_file_name)
        else:
            client.create_cookies(cookie_file_name)
        return client

    # 处理队首用户
    def _spider_collect_a_user(self, save_file):
        
        usr = self.queue.pop(0)

        with self.iolock:
            self.status[threading.current_thread().name] = [0, 0]  # 初始化状态传出

        # 下载id&关注数
        with self.fucklock:
            usr.id
            usr.followee_num

        # 总关注数传出线程
        with self.iolock:
            self.status[threading.current_thread().name][0] = usr.followee_num

        # 下载关注用户
        followeelist = []
        cnt = 0
        for x in usr.followees:
            followeelist.append(x.id)
            cnt += 1
            self.status[threading.current_thread().name][1] = cnt

        # 储存到硬盘
        with self.saver_lock:
            saver = ZhihuUser(
                usr.id, followeelist, followee_num=usr.followee_num)
            saver.save(save_file)
        # 加入到nameset
        with self.setlock:
            self.nameset.add(usr.id)

        # 入队关注的用户
        for followee in usr.followees and len(self.queue) < 1000000 :
            with self.setlock:
                if not followee in self.nameset:
                    self.queue.append(followee)

        with self.iolock:
            del self.status[threading.current_thread().name]

    # 输出循环
    def _show_status(self):
        cnt = 0
        while True:
            # if cnt % 5 == 0:
            #     self._show_list_gc()
            out = StringIO()

            # with self.setlock:
            #     for x in self.nameset:
            #         out.write('%s' % x)
            # out.write('\n')
            with self.iolock:
                for x in self.status.keys():
                    out.write('%s:(%d/%d)2\n' %
                              (x, self.status[x][1], self.status[x][0]))
            out = out.getvalue()

            os.system('cls')
            print(out)
            cnt += 1
            time.sleep(2)

    # 清理下载状态列表, canceled
    def _show_list_gc(self):
        del_ls = []
        with self.iolock:
            for x in self.status.keys():
                if self.status[x][0] != 0 and self.status[x][1] == self.status[x][0]:
                    del_ls.append(x)
            for x in del_ls:
                del self.status[x]

    # 爬虫工作
    def collect_user(self):

        def climb():
            try:
                self._spider_collect_a_user('save-from-motithreading.json')
            except Exception:
                pass

        if (len(self.queue) == 0):
            print('初始化...')
            l = self.client.author(self.people_url + 'liu-shi-qi-5-21')  # todo
            self.queue.append(l)
            climb()
        
        # 启动输出循环线程
        show = threading.Thread(target=self._show_status)
        show.setDaemon(True)
        show.start()

        # 启动退出检测线程
        try:
            threading.Thread(target=self._exit_detect).start()
        except Quit:
            return

        # 全线程循环参数
        max_threading = 20
        sleep_time = 1
        ls = []

        # 全线程循环
        while True:
            # 补足未完成线程
            while len(ls) < max_threading :
                if len(self.queue):
                    ls.append(
                        threading.Thread(target=climb, name=self.queue[0].id))
                    ls[-1].setDaemon(True)
                    ls[-1].start()

            # 删除已完成线程
            del_ls = []
            for thread in ls:
                if not thread.is_alive():
                    del_ls.append(thread)

            for i in del_ls:
                ls.remove(i)


            # 扫描周期
            time.sleep(sleep_time)

        self.exit()

    def exit(self):
        print('正在退出，请等待')
        self.iolock.acquire()
        self.saver_lock.acquire()
        self.fucklock.acquire()
        self.setlock.acquire()

        print('name saved', len(self.nameset))
        print('queue number', len(self.queue))

        with open(self.work_save_file_name, 'w') as f:

            s = json.dumps({ 'nameset':list(self.nameset),'queue': [i.id for i in self.queue]})

            f.write(s)
            print('完成')
            raise Quit


    def _exit_detect(self):
        while True:
            e = msvcrt.getch()
            if e == b'\x1b':
                self.exit()

    def load_file(self, file = 'default'):
        if file == 'default':
            file = self.work_save_file_name

        try:
            with open(file, 'r') as f:
                work_saved = json.loads(f.read())
        except FileNotFoundError:
            print('未找到文件')
            return
         
        self.nameset = set(work_saved['nameset'])
        print('队列恢复中...')
        for name in work_saved['queue']:
            self.queue.append(self.client.author(self.people_url + name))
        print('恢复成功，共', len(self.queue))

        # todo: 读取队列和已有列表
        # todo: 判断已有列表

# END <class zhihu_spider>


# if __name__ == '__main__':
#     spider = ZhihuSpider('cookie.json')
#     #spider.spider_collect_user('liu-shi-qi-5-21', 'from-me.json', 100)
#     spider.load_file()
#     spider.collect_user()


sample_code()