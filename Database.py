# -*- coding: utf-8 -*-
# database

SAVE_DIRECTORY = 'D:\\spider data\\'

from User import User
import os

class Database:
    '''
    每1000个用户存成一个文件，section = uid / 1000，存储格式：
    uid name number followee1 followee2 ... folloween
    '''

    def __init__(self):
        '''探查文件，构造查找树'''
        self.path = SAVE_DIRECTORY + 'user data\\'
        self.tree = DicTree()

    def get(self, uid):
        '''返回指定uid的用户类，不存在返回None'''
        filePath = self._filePath(user.uid)
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

    def setUser(self, user):
        '''将指定user存到文件中'''
        filePath = self._filePath(user.uid)

        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                file.write(' \n'*1000)

        with open(self.path + str(user.uid / 1000), 'r') as file:
            ls = file.readlines()

        ls[user.uid // 1000] = '%d %s %d %s' % (user.uid, user.name, user.followee_num, ' '.join(user.followees))

    def _filePath(self, uid):
        return self.path + str(uid / 1000)

    def _initTree(self):
        pass


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
        pass