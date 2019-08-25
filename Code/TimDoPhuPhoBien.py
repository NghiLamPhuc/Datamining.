############################################# IMPORT
from datetime import datetime
from collections import defaultdict

#import pandas as pd
import os
############################################# IMPORT
############################################# INPUT
def read_input_file(link , fileName) -> dict:
    f = open(link + fileName, 'r')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        line = line.rstrip()
        line = sorted(line.split(','))
        inpDict[i] = line
        i += 1
    return inpDict
############################################# INPUT
############################################# HÀM XỬ LÝ INPUT.
# 1. INPUT THEO KIỂU BẢNG NHỊ PHÂN. (EXCEL).
# 1
#def get_input_from_file() -> List[List]:
# 2. INPUT THEO KIỂU DICT: (ID, TRANSACTIONS). -> CHUYỂN VỀ BẢNG NHỊ PHÂN.
# 2.1 Hàm lấy list tần suất theo thứ tự item.
def get_unique_item_dict(inputDict: dict) -> dict:
    uniqueItem = dict()
    for (_, items) in inputDict.items():
        for item in items:
            if item not in uniqueItem:
                uniqueItem[item] = 1
            else:
                uniqueItem[item] += 1
    return uniqueItem
# 2.2 Hàm lấy tên các item từ dict: (item: tần suất) và tổng số item.
# INPUT: dữ liệu dạng dictionary (id: {item1, item2, ...}).
# OUTPUT: (list các item, tổng số item). 
def get_item_list_and_count_total(inputDict: dict) -> (list, int):
    uniqueItem = get_unique_item_dict(inputDict)
    itemList = list()
    total = 0
    for (item, frequency) in uniqueItem.items():
        itemList.append(item)
        total += frequency
    return (sorted(itemList), total)
# 2.3 Hàm tạo bảng nhị phân từ dict.
# INPUT: dữ liệu dạng dictionary (id: {item1, item2, ...}).
# OUTPUT: 2d list, dòng là các id, cột là các item. Xuất hiện là 1, ngược lại 0.
def create_binary_table(inputDict: dict) -> list:
    (itemList, _) = get_item_list_and_count_total(inputDict)
    col = len(itemList)
    row = len(inputDict)
    table = [[0 for r in range(col)] for c in range(row)]
    idList = list(inputDict.keys())

    for indexId in range(len(idList)):
        itemsAtId = inputDict[idList[indexId]]
        for indexItem in range(len(itemList)):
            if itemList[indexItem] in itemsAtId:
               table[indexId][indexItem] = 1
    return table
############################################# HÀM XỬ LÝ INPUT.

############################################# HÀM LẤY TẬP PHỔ BIẾN 1 ITEM.
# Hàm lọc item có tần suất >= minsup.
# itemset là tập phủ phổ biến. (sau khi so minsup).
# Những tập kết hợp gọi là possibleSet.
def get_one_item_set(table: list, minsup: float) -> list:
    numOfId = len(table)
    numOfItem = len(table[0])
    oneItemSet = list()
    minOccur = round(minsup * numOfId) # minsup = frequency(item) / total Id.
    for item in range(numOfItem):
        count = 0
        listItem = list()
        for id in range(numOfId):
            if table[id][item] == 1:
                count += 1
        if count >= minOccur:
            listItem.append(item)
            oneItemSet.append(listItem)
    return oneItemSet
############################################# HÀM LẤY TẬP PHỔ BIẾN 1 PHẦN TỬ.

############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# k_itemset : itemset có k phần tử.
# Ở mỗi k_itemset, duyệt các k_itemset phía sau.
# k_itemset đầu tiên kết hợp với 1 item trong k_itemset phía sau tạo thành (k+1)_itemset mới.
def get_item_set_k_1(table: list, itemSetK: list, minsup: float) -> list:
    if len(itemSetK) == 0:
        return 'Het roi!'
    
    itemSetK_1 = list() # lưu itemset có k+1 phần tử.
    numOfSet = len(itemSetK) # số itemset có k phần tử.
    numOfItem = len(itemSetK[0]) # số phần tử trong một itemset.

    for curr in range(numOfSet - 1):
        for next in range(curr + 1, numOfSet):
            for item in range(numOfItem):
                addItem = itemSetK[next][item] # item trong k_itemset phía sau.
                if addItem not in itemSetK[curr]: # kiểm tra addItem có trùng với item nào trong itemset hay không.
                    possibleSet = itemSetK[curr].copy()
                    possibleSet.append(addItem)
                    checkPossible = 0
                    for newSet in itemSetK_1:
                        if set(possibleSet) == set(newSet): # kiểm tra possibleSet đã tồn tại chưa.
                            checkPossible = 1
                            break
                    if (checkPossible == 0) and check_itemset_minsup(table, possibleSet, minsup): # đếm tần suất của bộ mới tạo, có thỏa minsup thì lấy.
                        itemSetK_1.append(possibleSet)
    return itemSetK_1

# Hàm đếm tần suất của một tập thỏa minsup hay không.
def check_itemset_minsup(table: list, itemSet: list, minsup: float) -> bool:
    if len(itemSet) == 0:
        return False
    
    numOfId = len(table)
    numOfItemInSet = len(itemSet)
    minOccur = round(minsup * numOfId)
    count = 0
    # duyệt theo dòng, mỗi dòng, duyệt theo item trong itemSet
    for id in range(numOfId):
        sumId = 0
        for item in itemSet:
            if table[id][item] == 1:
                sumId += 1
        if sumId == numOfItemInSet:
            count += 1
        if count >= minOccur:
            return True
    return False

# Hàm lấy tất cả tập phủ phổ biến.
# Đầu tiên, lấy tất cả tập phủ phổ biến.
# Sau đó bỏ các tập bị tập khác phủ.
def apriori(table: list, minsup: float) -> list:
    allItemSet = list()
    allMaxItemSet = list()
    preCover = get_one_item_set(table, minsup)
    while len(preCover) >= 1:
        nextCover = get_item_set_k_1(table, preCover, minsup)
        for itemSet in nextCover:
            allItemSet.append(itemSet)
        preCover = nextCover
    for curr in range(len(allItemSet) - 1):
        currSet = allItemSet[curr]
        for next in range(curr + 1, len(allItemSet)):
            nextSet = allItemSet[next]
            check = False
            if set(currSet).issubset(nextSet):
                check = True
                break
        if not check:
            allMaxItemSet.append(currSet)
            
    allMaxItemSet.append(allItemSet[-1])
    return allMaxItemSet

# Hàm lấy tên item từ tập phủ phổ biến tối đại.
def get_item_name(itemList: list, maxItemSet: list) -> list:
    allMaxItemSetName = list()
    for indexSet in range(len(maxItemSet)):
        nameSet = list()
        for item in maxItemSet[indexSet]:
            nameSet.append(itemList[item])
        allMaxItemSetName.append(nameSet)
    return allMaxItemSetName
############################################# HÀM MAIN.

def main():
    start = datetime.now()

    minsup = 0.3
    #inputDict = {100: ['A', 'C', 'D', 'I'], 200: ['A', 'C', 'I'], 300: ['C', 'E', 'I'], 400: ['A', 'B', 'D', 'E'], 500: ['B', 'D', 'I'], 600: ['A', 'B', 'D', 'E']}
    inputDict = {'O1': ['i1', 'i7', 'i8'], 'O2': ['i1', 'i2', 'i6', 'i7', 'i8'], 'O3': ['i1', 'i2', 'i6', 'i7'], 'O4': ['i1', 'i8', 'i7'], 'O5': ['i3', 'i4', 'i5', 'i6', 'i8'], 'O6': ['i1', 'i4', 'i5']}
    #inputDict = {'t1': [1, 3, 4], 't2': [2, 3, 5], 't3': [1,2,3,5], 't4':[2,5],'t5':[1,2,3,5]}

    table = create_binary_table(inputDict)
    #print(*table, sep = '\n')
    #(itemList, _) = get_item_list_and_count_total(inputDict)
    #print(itemList)
    
    #maxItemSet = apriori(table, minsup)
    #print(maxItemSet)
    #print(get_item_name(itemList, maxItemSet))
    link_folder_train = 'D:\\Workspace\\DataMining\\Code\\'
    
    inpDict = read_input_file(link_folder_train, 'input.txt')
    #print(inpDict)
    (itemList, _) = get_item_list_and_count_total(inpDict)
    #print(itemList,_)
    #print(len(itemList))
    table1 = create_binary_table(inpDict)
    maxItemSet = apriori(table1, 0.03) # 43367 / 169 = 256; 256 / 9835 = 0.03
    #print(*maxItemSet, sep = '\n')
    print(*(get_item_name(itemList, maxItemSet)), sep = '\n')
    

    print (datetime.now()-start)
    
if __name__ == "__main__": main()
