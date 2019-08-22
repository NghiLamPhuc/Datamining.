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
# 1.1 Hàm lấy tần suất của 1 item.
# INPUT: 2d list, dòng là các id, cột là các item. Xuất hiện là 1, ngược lại 0.
# OUTPUT: dictionary (item: frequency)
# Hàm này trùng hàm get_unique_item_dict
#def get_one_item_count(table: list) -> dict:
#    oneItemCount = dict()
#    for indexItem in range(1, len(table[0])):
#        for indexId in range(1, len(table)):
#            if table[indexId][indexItem] == ' 1':
#                if table[0][indexItem] not in oneItemCount:
#                   oneItemCount[table[0][indexItem]] = 1
#                else:
#                    oneItemCount[table[0][indexItem]] += 1
#    return oneItemCount
# 1.2 Hàm lọc item có tần suất >= minsup.
def get_one_item_cover(inputDict: dict, minsup: float) -> list:
    oneItemCount = get_unique_item_dict(inputDict)
    (itemList, _) = get_item_list_and_count_total(inputDict)
    minOccur = round(minsup * len(inputDict)) # minsup = frequency(item)/number of ID.
    oneCover = list()
    for (item, count) in oneItemCount.items():
        itemSet = list()
        if count >= minOccur:
            itemSet.append(itemList.index(item))
            oneCover.append(itemSet)
    return sorted(oneCover)
    
############################################# HÀM LẤY TẬP PHỔ BIẾN 1 PHẦN TỬ.

############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# 1. TẠO CÁC TẬP ỨNG VIÊN K PHẦN TỬ, TỪ TẬP PHỦ PHỔ BIẾN K-1 PHẦN TỬ.
# INPUT: list các Itemset 1 phần tử và số thứ k+1.
# OUTPUT: list các Itemset k+1 phần tử.
# 
# 
# 
def generate_k_1_item_set_from_one_item_set(itemSetK: list, k_1: int) -> list:
    listOfCombine = list()
    lenOfSetK = len(itemSetK[0])

    for length in range(lenOfSetK + k_1 - 1, lenOfSetK + k_1):
        for subset in itertools.combinations(itemSetK, length):
            listOfCombine.append(list(subset))

    itemSetK_1 = list()
    for lst in listOfCombine:
        itemSetK_1.append([j for sub in lst for j in sub])
        
    return itemSetK_1

# 2. ĐẾM TẦN SUẤT CÁC TẬP K PHẦN TỬ ĐÓ.
# 3. LOẠI BỎ TẬP CÓ TẦN SUẤT < MINSUP.
############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.


############################################# HÀM MAIN.

def main():
    minsup = 0.3
    #inputDict = {100: ['A', 'C', 'D', 'I'], 200: ['A', 'C', 'I'], 300: ['C', 'E', 'I'], 400: ['A', 'B', 'D', 'E'], 500: ['B', 'D', 'I'], 600: ['A', 'B', 'D', 'E']}
    inputDict = {'O1': ['i1', 'i7', 'i8'], 'O2': ['i1', 'i2', 'i6', 'i7', 'i8'], 'O3': ['i1', 'i2', 'i6', 'i7'], 'O4': ['i1', 'i8', 'i7'], 'O5': ['i3', 'i4', 'i5', 'i6', 'i8'], 'O6': ['i1', 'i4', 'i5']}

    table = create_binary_table(inputDict)
    #print(*table, sep = '\n')
    #(items, total) = get_item_list_and_count_total(inputDict)
    oneCover = get_one_item_cover(inputDict, minsup)
    #print(oneCover)
    for k in range(2, len(oneCover) + 1):
        kCount = generate_k_1_item_set_from_one_item_set(oneCover, k)
        print(kCount)
        print()
    
    
if __name__ == "__main__": main()
