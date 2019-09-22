import random
import write_file

# 10.000 dòng,
# mỗi dòng random 1->50 item.
# mỗi item random từ 0->50
# transDict = dict()
# for row in range(10000):
#     numOfItem = random.randint(1, 20)
#     transList = list()
#     for col in range(numOfItem):
#         item = random.randint(0, 50)
#         transList.append(item)
#     transDict[row] = transList

# fileName = '1000itemsIn10000trans.txt'
# fileDir = './Generate Input/'
# write_file.dict_to_txt(transDict, fileDir, fileName)# if fileName not in './Generate Input/' else fileName[]
import os
os.environ["PATH"] += os.pathsep + 'C:/Users/NghiLam/Anaconda3/Library/bin/graphviz'
from graphviz import Digraph
dot = Digraph(comment='Associate Rule')
dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edge('AB')

# print(dot.source)
dot.render('test-output/round-table.gv', view=True)
