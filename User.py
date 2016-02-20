# -*- coding: utf-8 -*-
# user

class User:

    def __init__(self, uid=0, name='', followee_num=0):
        self.followees = []
        self.set(name, uid, followee_num)

    def set(self, uid=0, name='', followee_num=0):
        self.uid = uid
        self.name = name
        self.followee_num = followee_num

    def setFollowees(self, followees):
        self.followees = followees

    def addFollow(self, uid):
        self.followees.append(uid)