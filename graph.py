# -*- coding: utf-8 -*-
# graph

from Database import DicTree, Database
from User import User


class Graph:

    def __init__(self):

        self.namespace = []
        self.userset = None
        self.matrix = None
        self.tree = DicTree()
        self.database = Database()

    def addPoint(self, name):
        self.namespace.append(name)

    def setEdge(self, start, target, weight):
        self.matrix[start][target] = weight

    

    def buidGraph(self):

        # fill namespace
        print('check complete')
        self.userset = self.database.complete()
        print('fill namespace')
        for user in self.userset:
            self.namespace.append(user.id)

        # build tree
        print('build tree')
        i = 0
        for name in self.namespace:
            self.tree.set(name, i)
            i += 1

        # add Edge
        print('add edge', len(self.namespace))
        self.matrix = [[0]*len(self.namespace) for j in range(len(self.namespace))]

        i = 0
        for user in self.userset:
            for followee in user.followees:
                start = self.tree.search(user.id)
                end = self.tree.search(followee)
                if end is None:
                    continue
                self.setEdge(start, end, user.followee_num)
                print(start, end)
                i += 1
        print('all finished', i)

    def show(self):
        print(self.namespace)
        print(self.matrix)

class PageRank:

    def __init__(self):

        self.graph = Graph()
        self.graph.buidGraph()
        self.pagerank = [1] * len(self.graph.namespace)

    def calculate(self, damping_factor=0.85, max_iterations=100, min_delta=0.0000000001):
        lenth = len(self.graph.namespace)
        min_value = (1.0-damping_factor)/lenth
        start = 0
        target = 0

        # n次迭代
        for iterTime in range(max_iterations):
            delta = 0
            print('第%d次迭代:'%iterTime)

            # 遍历节点
            for target in range(lenth):

                newRank = min_value
                # 所有关注者的pagerank加到它中
                for start in range(lenth):
                    if self.graph.matrix[start][target] != 0:
                        newRank += damping_factor * self.pagerank[start] / self.graph.matrix[start][target]
                delta += abs(newRank - self.pagerank[target])
                self.pagerank[target] = newRank

            print(self.pagerank)

            if delta < min_delta:
                break
    

        print(self.pagerank)

    def findBiggest(self):

        maxSoFar = 0
        pos = 0
        i = 0
        for item in self.pagerank:
            if maxSoFar < item:
                maxSoFar = item
                pos = i
            i += 1
        print(self.graph.namespace[pos], maxSoFar)

    def rank(self):
        pair = zip(self.graph.namespace, self.pagerank)
        ls = ''
        for i in sorted(pair, key=lambda a: a[1], reverse=True):
            ls += i + '\n'
        with open('D:\\spider data\\result.txt', mode='w') as file:
            file.write(ls)

        print(pair)







p = PageRank()
p.calculate()
p.findBiggest()
p.rank()


