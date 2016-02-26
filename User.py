# -*- coding: utf-8 -*-
# user

class User:

    def __init__(self, uid=0, id='', followee_num=0, user=None, withFollowee=False):
        self.followees = []
        if user == None:
            self.set(uid, id, followee_num)
        else:
            self.set(user.uid, user.id, user.followee_num)
            if withFollowee == True:
                self.setFollowees(list(user.followees))

    def set(self, uid=0, id='', followee_num=0):
        self.uid = uid
        self.id = id
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