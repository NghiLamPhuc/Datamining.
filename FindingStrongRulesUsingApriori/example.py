import random
import write_file

## 10.000 dòng,
## mỗi dòng random 1->50 item.
## mỗi item random từ 0->50
transDict = dict()
for row in range(10000):
    numOfItem = random.randint(1, 20)
    transList = list()
    for col in range(numOfItem):
        item = random.randint(0, 50)
        transList.append(item)
    transDict[row] = transList

fileName = 'generate.txt'
fileDir = './input/'
write_file.dict_to_txt(transDict, fileDir, fileName)# if fileName not in './Generate Input/' else fileName[]
