# -*- coding: utf-8 -*-
# database

SAVE_DIRECTORY = 'D:\\spider data\\'

from User import User
import os
import threading
import queue

from logger import put

class Database:
    '''
    每1000个用户存成一个文件，section = uid // 1000，存储格式：
    uid name number followee1 followee2 ... followee_n
    '''

    def __init__(self):
        '''探查文件，构造查找树'''
        self.path = SAVE_DIRECTORY + 'user data\\'
        self.tree = DicTree()
        self.buffer = []
        self.fileLock = threading.Lock()
        self.treeLock = threading.Lock()
        # self._initTree()
        self.buffer = queue.Queue()

    def get(self, uid):
        '''返回指定uid的用户类，不存在返回None'''
        filePath = self._uidFilePath(uid)
        if os.path.exists(filePath):

            fileVector = self._readFile(filePath)
            if fileVector[uid // 1000] != ' ':
                components = fileVector[uid // 1000].split(' ')
                user =  User(int(components[0]), components[1], int(components[2]))
                user.setFollowees(components[3:])
            else:
                return None
        else:
            return None

    def getUid(self, name):
        '''返回指定用户名的uid，不存在返回None'''
        with self.treeLock:
            uid = self.tree.search(name)
        return uid

    def saveUser(self, user):
        '''将指定user存到文件中'''
        with self.fileLock:
            # filePath = self._uidFilePath(user.uid)

            # # 若路径不存在，建立填充回车的空文件
            # # if not os.path.exists(filePath):
            # #     self._writeFile(filePath, ['\n']*1000)

            # # 读取->修改->保存
            # ls = self._readFile(filePath)
            # while len(ls) < 1000:
            #     ls.append('')
            # print(user.uid % 1000, user.uid, ls[user.uid % 1000])
            # ls[user.uid % 1000] = '%d %s %d %s\n' % (user.uid, user.id, user.followee_num, ' '.join([x.id for x in user.followees if x!='\n']))

            # self._writeFile(filePath, ls)
            if self.buffer.qsize() > 20:
                self._clearBuffer()

            self.buffer.put(user)

            # update tree
            self.tree.set(user.id, user.uid)

    def checkIntegrity(self):
        '''检查所有文件完整性，返回未完成的用户类'''
        unfinishedUserList = []
        i = 0
        uidcounter = 0
        while os.path.exists(self._numFile(i)):
            lines = self._readFile(self._numFile(i))
            self._delEnter(lines)
            for line in lines:
                components = self._parseLine(line)
                if not self._isLineIntegrated(components):

                    unfinishedUserList.append(User(int(components[0]), components[1], int(components[2])))
                uidcounter += 1
                if uidcounter != components[0]:
                    put(components)
            i += 1
        return unfinishedUserList

    def complete(self):
        '''检查所有文件完整性，返回完成的用户类'''
        finishedUserList = []
        i = 0
        while os.path.exists(self._numFile(i)):
            lines = self._readFile(self._numFile(i))
            self._delEnter(lines)
            for line in lines:
                if len(line) == 0:
                    continue
                if line[-1] == ' ':
                    line = line[0:-1]
                components = self._parseLine(line)
                if self._isLineIntegrated(components):
                    temp = User(int(components[0]), components[1], int(components[2]))
                    temp.followees = components[3:]
                    finishedUserList.append(temp)

            i += 1
        return finishedUserList

    def checkLatest(self):
        '''检查最后的文件的最后一个用户'''
        i = 0
        while os.path.exists(self._numFile(i)):
            i += 1
        lines = self._readFile(self._numFile(i - 1))
        self._delEnter(lines)

        return int(lines[-1].split(' ')[0])



    # todo canceled
    def setUser(self, user):
        '''将指定user加入缓冲等待储存'''
        with self.saveLock:
            pass

    # =================私有函数====================

    # file management

    def _uidFilePath(self, uid):
        return self.path + str(uid // 1000)

    def _numFile(self, number):
        return self.path + str(number)

    def _readFile(self, filePath):

        with open(filePath, 'r') as file:
            ls = file.readlines()
        return ls

    def _writeFile(self, filePath, contentList):
        with open(filePath, 'w') as file:
            file.writelines(contentList)

    def _writeLine(self, uid, content):
        lines = []
        if os.path.exists(self._uidFilePath(uid)):
            with open(self._uidFilePath(uid), 'r+') as file:
                lines = file.readlines()
        

        while len(lines) < 1000:
            lines.append('\n')
        lines[uid % 1000] = content

        with open(self._uidFilePath(uid), 'w') as file:
            file.writelines(lines)

    def _writeUser(self, user):
            self._writeLine(user.uid, '%d %s %d %s\n' % (user.uid, user.id, user.followee_num, ' '.join([x.id for x in user.followees if x!='\n'])))
            # update tree
            self.tree.set(user.id, user.uid)

    # string operations

    def _delEnter(self, lines):
        i = 0
        for line in lines:
            if line[-1] == '\n':
                lines[i] = line[0:-1]
            i += 1



    def _isLineIntegrated(self, line):
        if isinstance(line, str):
            line = line.split(' ')
        elif not isinstance(line, list):
            raise TypeError

        if line[-1] == '\n':
            line.pop()
        if int(line[2]) == len(line) - 3:
            return True
        else:
            return False

    def _parseLine(self, line):
        return line.split(' ')

    # tree

    def _initTree(self):
        '构建姓名查找树'
        print('构造查找树：')
        i = 0
        while os.path.exists(self._numFile(i)):
            path = self._numFile(i)
            with open(self._uidFilePath(i), 'r') as file:
                lines = file.readlines()

            # 取名字
            try:
                t = [line.split(' ') for line in lines if line is not '\n']
                for uid, name in [(x[0], x[1]) for x in [line.split(' ') for line in lines if line is not '\n']]:
                    self.tree.set(name, int(uid))
            except IndexError:
                pass
            i += 1
            print(i)
        print('构造完毕：', i)


    # buffer management

    def _clearBuffer(self, size=100):
        while not self.buffer.empty():
            self._writeUser(self.buffer.get())

class DicTree:
    class _node:
        def __init__(self, data):
            self.data = data
            self.children = {}

        def add(self, char, node):
            self.children[char] = node

    def __init__(self):
        self.root = self._node(None)

    def search(self, name):
        node = self.root
        index = 0
        while index != len(name):
            if name[index] in node.children :
                node = node.children[name[index]]
                index += 1
            else:
                return None
        return node.data

    def set(self, name, data):
        node = self.root
        index = 0
        while index != len(name):
            # 没有则创建
            if not name[index] in node.children:
                node.children[name[index]] = self._node(None)

            node = node.children[name[index]]
            index += 1
        if node.data != None:
            put('error: 重复构造查找树，原始uid/替换uid:' + str(node.data)+'/'+str(data))
        node.data = data

