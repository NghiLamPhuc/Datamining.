############################################# IMPORT
from collections import defaultdict
import itertools

import pandas as pd
import os
############################################# IMPORT
############################################# INPUT
#
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
# 1. TẠO CÁC TẬP ỨNG VIÊN K PHẦN TỬ, TỪ TẬP PHỦ PHỔ BIẾN K-1 PHẦN TỬ.
# INPUT: list các Itemset 1 phần tử và số thứ k+1.
# OUTPUT: list các Itemset k+1 phần tử.
# 
# 
# 
#def generate_k_1_item_set_from_one_item_set(itemSetK: list, k_1: int) -> list:
#    listOfCombine = list()
#    lenOfSetK = len(itemSetK[0])

#    for length in range(lenOfSetK + k_1 - 1, lenOfSetK + k_1):
#        for subset in itertools.combinations(itemSetK, length):
#            listOfCombine.append(list(subset))

#    itemSetK_1 = list()
#    for lst in listOfCombine:
#        itemSetK_1.append([j for sub in lst for j in sub])
        
#    return itemSetK_1
def get_item_set_k_1(table: list, itemSetK: list, minsup: float) -> list:
    if len(itemSetK) == 0:
        return 'Het roi!'
    
    itemSetK_1 = list() # lưu itemset có k+1 phần tử.
    numOfSet = len(itemSetK) # số itemset có k phần tử.
    numOfItem = len(itemSetK[0]) # số phần tử trong một itemset.

    # kết hợp itemset trước, với từng item trong các itemset sau.
    
    for curr in range(numOfSet - 1):
        listAdd = list() # đánh dấu các addItem đã thêm vào itemset hay chưa.
        for next in range(curr + 1, numOfSet):
            for item in range(numOfItem):
                addItem = itemSetK[next][item]
                if addItem not in listAdd: # kiểm tra addItem đã từng thêm vào itemset chưa.
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
                            listAdd.append(addItem)
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

# 2. ĐẾM TẦN SUẤT CÁC TẬP K PHẦN TỬ ĐÓ; LOẠI BỎ TẬP CÓ TẦN SUẤT < MINSUP.
#def collect_item_set_after_minsup(itemSet: list, minsup: float) -> list:
    

############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.


############################################# HÀM MAIN.

def main():
    minsup = 0.3
    #inputDict = {100: ['A', 'C', 'D', 'I'], 200: ['A', 'C', 'I'], 300: ['C', 'E', 'I'], 400: ['A', 'B', 'D', 'E'], 500: ['B', 'D', 'I'], 600: ['A', 'B', 'D', 'E']}
    inputDict = {'O1': ['i1', 'i7', 'i8'], 'O2': ['i1', 'i2', 'i6', 'i7', 'i8'], 'O3': ['i1', 'i2', 'i6', 'i7'], 'O4': ['i1', 'i8', 'i7'], 'O5': ['i3', 'i4', 'i5', 'i6', 'i8'], 'O6': ['i1', 'i4', 'i5']}

    table = create_binary_table(inputDict)
    #print(*table, sep = '\n')
    preCover = get_one_item_set(table, minsup)
    while len(preCover) >= 1:
        nextCover = get_item_set_k_1(table, preCover, minsup)
        print(preCover)
        preCover = nextCover
        


 
if __name__ == "__main__": main()
