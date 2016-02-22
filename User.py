# -*- coding: utf-8 -*-
# user

class User:

    def __init__(self, uid=0, name='', followee_num=0, user=None, withFollowee=False):
        self.followees = []
        if user == None:
            self.set(name, uid, followee_num)
        else:
            self.set(user.name, user.uid, user.followee_num)
            if withFollowee == True:
                self.setFollowees(list(user.followees))

    def set(self, uid=0, name='', followee_num=0):
        self.uid = uid
        self.name = name
        self.followee_num = followee_num

    def setFollowees(self, followees):
        self.followees = followees

    def addFollow(self, uid):
        self.followees.append(uid)

    def isIntegrated(self):
        if len(self.followees) == self.followee_num:
            return True
        else:
            return False