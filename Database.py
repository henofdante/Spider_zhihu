# -*- coding: utf-8 -*-
# database

SAVE_DIRECTORY = 'D:\\spider data\\'

from User import User
import os
import threading

class Database:
    '''
    每1000个用户存成一个文件，section = uid / 1000，存储格式：
    uid name number followee1 followee2 ... followee_n
    '''

    def __init__(self):
        '''探查文件，构造查找树'''
        self.path = SAVE_DIRECTORY + 'user data\\'
        self.tree = DicTree()
        self.buffer = []
        self.saveLock = threading.Lock()

    def get(self, uid):
        '''返回指定uid的用户类，不存在返回None'''
        filePath = self._uidFilePath(user.uid)
        if os.path.exists(filePath):
            with open(filePath, 'r') as file:
                fileVector = file.readlines()
            if fileVector[uid // 1000] != ' ':
                components = fileVector[uid // 1000].split(' ')
                user =  User(int(components[0]), components[1], components[2])
                user.setFollowees(components[3:])
            else:
                return None
        else:
            return None


    def getUid(self, name):
        '''返回指定用户名的uid，不存在返回None'''
        return self.tree.search(name)

    def saveUser(self, user):
        '''将指定user存到文件中'''
        filePath = self._uidFilePath(user.uid)

        # 若路径不存在，建立填充回车的空文件
        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                file.write(' \n'*1000)

        # 读取->修改->保存
        with open(self.path + str(user.uid / 1000), 'r') as file:
            ls = file.readlines()

        ls[user.uid // 1000] = '%d %s %d %s' % (user.uid, user.name, user.followee_num, ' '.join(user.followees))

        with open(self.path + str(user.uid / 1000), 'w') as file:
            file.write('\n'.join(ls))

    def checkIntegrity(self):
        '''检查所有文件完整性，返回未完成的用户类'''
        unfinishedUserList = []


    # todo
    def setUser(self, user):
        '''将指定user加入缓冲等待储存'''
        with self.saveLock:
            pass

    # =================私有函数====================

    def _uidFilePath(self, uid):
        return self.path + str(uid / 1000)

    def _numFile(self, number):
        return self.path + str(number)

    def _readFile(self, filePath):
        with open(filePath, 'r') as file:
            ls = file.readlines()
        return ls

    def writeFile(self, filePath, contentList):
        with open(filePath, 'w') as file:
            file.writelines(contentList)


    def _initTree(self):
        '构建姓名查找树'
        i = 0
        while os.path.exists(self._uidFilePath(i)):
            with open(self._uidFilePath(i), 'r') as file:
                lines = file.readlines()
            # 取名字
            for uid, name in [(x[0], x[1]) for x in map(' '.split, lines)]:
                self.tree.set(name, uid)
            i += 1

    #todo
    def _bufferManager(self, filePath, content):
        pass

    def _isLineIntegrated(self, line):
        if isinstance(line, str):
            line = line.split(' ')
        elif not isinstance(line, list):
            raise TypeError

        if line[1] == len(line - 2):
            return True
        else:
            return False



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
            if node.children.has_key(name[index]):
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
            if not node.children.has_key(name[index]):
                node.children[name[index]] = self._node()

            node = node.children[name[index]]
            index += 1
        node.data = data
