############################################# IMPORT
from datetime import datetime
from collections import defaultdict

import csv
import pandas as pd
from pandas import DataFrame
import os
############################################# INPUT
def read_input_file(link, fileName) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        line = line.rstrip()
        line = sorted(line.split(', '))
        inpDict[i] = line
        i += 1
    return inpDict

def read_input_file_2(link, fileName) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        line = line.rstrip()
        line = sorted(line.split(' '))
        inpDict[i] = line
        i += 1
    return inpDict

# Ghi list ra text.
def list_to_txt(List: list, link, name):
    createFolder(link)
    if not List:
        print('Khong co tap thoa man minsup!')
        return
    file = link + name
    with open(file, 'w', encoding = 'utf-8') as fout:
        i = 0
        for itemSet in List:
            fout.write('%d %s\n' % (i, itemSet) )
            i += 1

def list_to_txt_no_index(List: list, link, name):
    createFolder(link)
    if not List:
        print('Khong co tap thoa man minsup!')
        return
    file = link + name
    with open(file, 'w', encoding = 'utf-8') as fout:
        for itemSet in List:
            for index in range(len(itemSet) - 1):
                fout.write('%s,' % itemSet[index] )
            fout.write('%s' % itemSet[-1] )
            fout.write('\n')

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return directory
    except OSError:
        print ('Khong the tao duoc thu muc!' +  directory)

############################################# HÀM XỬ LÝ INPUT.
# 2. INPUT THEO KIỂU DICT: (ID, TRANSACTIONS). -> CHUYỂN VỀ BẢNG NHỊ PHÂN.
# 2.1 Hàm lấy list tần suất theo thứ tự item.
def get_unique_item_dict(inputDict: dict) -> dict:
    uniqueItem = dict()
    total = 0
    for (_, items) in inputDict.items():
        total += len(items)
        for item in items:
            if item not in uniqueItem:
                uniqueItem[item] = 1
            else:
                uniqueItem[item] += 1
    # có n item khác nhau, xuất hiện tổng là m.
    # 1 item, xuất hiện m/n.
    # min_sup = (m/n) / số id
    min_sup = round( ( total/len(uniqueItem) ) / len(inputDict), 5 )
    
    return (uniqueItem, min_sup)

############################################# HÀM LẤY TẬP PHỔ BIẾN 1 ITEM.
def get_one_itemSet(inputDict: dict, minsup: float) -> list:
    numOfId = len(inputDict)
    (uniqueItem, min_sup) = get_unique_item_dict(inputDict)
    itemList = sorted(list(uniqueItem.keys()))
    oneItemSet = list(list())
    minOccur = round(minsup * numOfId) # minsup = frequency(item) / total Id.
    for item in itemList:
        count = 0
        for (id, items) in inputDict.items():
            if item in items:
                count += 1
            if count == minOccur:
                oneItemSet.append([item])
                break
        
    return oneItemSet

############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# k_itemset : itemset có k phần tử.
# Ở mỗi k_itemset, duyệt các k_itemset phía sau.
# k_itemset đầu tiên kết hợp với 1 item trong k_itemset phía sau tạo thành (k+1)_itemset mới.
# thật ra Apriori ở đây. =))
def get_k_1_itemSet(inputDict: dict, kItemSet: list, minsup: float) -> list:
    if len(kItemSet) == 0:
        return 'Het roi!'
    
    k_1ItemSet = list() # lưu itemset có k+1 phần tử.
    numOfSet = len(kItemSet) # số itemset có k phần tử.
    numOfItem = len(kItemSet[0]) # số phần tử trong một itemset.

    for curr in range(numOfSet - 1):
        for next in range(curr + 1, numOfSet):
            for item in range(numOfItem):
                addItem = kItemSet[next][item] # item trong k_itemset phía sau.
                if addItem not in kItemSet[curr]: # kiểm tra addItem có trùng với item nào trong itemset hay không.
                    possibleSet = kItemSet[curr].copy()
                    possibleSet.append(addItem)
                    checkPossible = 0
                    for newSet in k_1ItemSet:
                        if set(possibleSet) == set(newSet): # kiểm tra possibleSet đã tồn tại chưa.
                            checkPossible = 1
                            break
                    if (checkPossible == 0) and check_itemSet_minsup(inputDict, possibleSet, minsup): # đếm tần suất của bộ mới tạo, có thỏa minsup thì lấy.
                        k_1ItemSet.append(possibleSet)

    return k_1ItemSet

# Hàm đếm tần suất của một tập thỏa minsup hay không.
def check_itemSet_minsup(inputDict: dict, itemSet: list, minsup: float) -> bool:
    if len(itemSet) == 0:
        return False
    
    numOfId = len(inputDict)
    numOfItemInSet = len(itemSet)
    minOccur = round(minsup * numOfId)
    count = 0
    # duyệt theo dòng, mỗi dòng, duyệt theo item trong itemSet
    for (id, items) in inputDict.items():
        sumId = 0
        for item in itemSet:
            if item in items:
                sumId += 1
        if sumId == numOfItemInSet:
            count += 1
        if count >= minOccur:
            return True
    return False

# Hàm lấy tất cả tập phủ phổ biến.
# Đầu tiên, lấy tất cả tập phủ phổ biến.
# Sau đó bỏ các tập bị tập khác phủ.
def apriori(inputDict: dict, minsup: float) -> list:
    allItemSet = list()
    allFrequentItemSet = list()
    preCover = get_one_itemSet(inputDict, minsup)
    while len(preCover) >= 1:
        nextCover = get_k_1_itemSet(inputDict, preCover, minsup)
        for itemSet in nextCover:
            allItemSet.append(itemSet)
        preCover = nextCover
    
    if not allItemSet:
        print('Khong co itemset thoa man min_sup.')
        return allItemSet

    # Remove all itemSet be covered.
    for curr in range(len(allItemSet) - 1):
        currSet = allItemSet[curr]
        for next in range(curr + 1, len(allItemSet)):
            nextSet = allItemSet[next]
            check = False
            if set(currSet).issubset(nextSet):
                check = True
                break
        if not check:
            allFrequentItemSet.append(currSet)
           
    allFrequentItemSet.append(allItemSet[-1])
    
    return allFrequentItemSet

############################################# HÀM MAIN.
def main():
    start = datetime.now()

    link_folder = 'D:\\Workspace\\DataMining\\Code\\'
    link_input = link_folder + 'Input\\'
    nameFile = ['baitapbuoi2.txt', 'input.txt', 'input2.txt', 'baitapthem7.txt', 'baitapbuoi22.txt', 'baitapbuoi23.txt', 'test_da2.input']

    minsup = [0.3, 0.03, 0.3, 0.6]
    
    number = -1

    #inputDict = read_input_file(link_input, nameFile[number])
    inputDict = read_input_file_2(link_input, nameFile[number])
    
    #(items, _) = get_unique_item_dict(inputDict)
    maxItemSet = apriori(inputDict, minsup[1])
    
    list_to_txt_no_index(maxItemSet, link_folder + 'Frequent_ItemSet\\', 'FIS_' + nameFile[number])
    
    print (datetime.now() - start)
    
if __name__ == "__main__": main()