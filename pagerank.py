# -*- coding:utf-8 -*-

# python-graph https://code.google.com/p/python-graph/

# Import graphviz
import graphviz as gv

# Import pygraph
from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write

def pagerank(graph, damping_factor=0.85, max_iterations=100, min_delta=0.00001):
             # 图      阻尼系数           最大迭代次数       两次迭代最大差
    nodes = graph.nodes()
    graph_size = len(nodes)
    if graph_size == 0:
        return {}

    # pagerank最小值
    min_value = (1.0-damping_factor)/graph_size

    # 初始化字典储存pagerank值
    pagerank = dict.fromkeys(nodes, 1.0)

    for i in range(max_iterations):
        diff = 0 
        # 直接遍历所有节点
        for node in nodes:
            rank = min_value

            # 所有指向这一节点的pagerank值加到这一节点中
            for referring_page in graph.incidents(node):
                rank += damping_factor * pagerank[referring_page] / len(graph.neighbors(referring_page))
            diff += abs(pagerank[node] - rank)
            pagerank[node] = rank

        print('第%d次迭代' % (i+1))
        print(pagerank)

        # 两次迭代结果差趋近于0，程序结束
        if diff < min_delta:
            break

    return pagerank

# 测试样例 需要类库
# Graph creation
gr = digraph()

# Add nodes and edges
gr.add_nodes(["1","2","3","4"])

gr.add_edge(("1","2"))
gr.add_edge(("1","3"))
gr.add_edge(("1","4"))
gr.add_edge(("2","3"))
gr.add_edge(("2","4"))
gr.add_edge(("3","4"))
gr.add_edge(("4","2"))

# Draw as PNG
# dot = write(gr)
# gvv = gv.readstring(dot)
# gv.layout(gvv,'dot')
# gv.render(gvv,'png','Model.png')

pagerank(gr)
