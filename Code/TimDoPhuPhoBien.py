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
        #line = sorted(line.split(','))
        line = sorted(line.split(' '))
        inpDict[i] = line
        i += 1
    return inpDict

# Xuất table ra file excel.
def table_to_xlsx(table: list, name, link):
    createFolder(link)
    df = DataFrame(table)
    df.to_excel(link + name + '.xlsx', index = False)

# Ghi list ra text.
def list_to_txt(List: list, link, name):
    createFolder(link)
    file = link + name
    with open(file, 'w', encoding = 'utf-8') as fout:
        i = 0
        for itemSet in List:
            fout.write('%d %s\n' % (i, itemSet) )
            i += 1

def list_to_txt_no_index(List: list, link, name):
    createFolder(link)
    file = link + name
    with open(file, 'w', encoding = 'utf-8') as fout:
        for itemSet in List:
            row = ''
            for item in range(len(itemSet) - 1):
                row += itemSet[item] + ', '
            row += itemSet[-1]
            fout.write('%s\n' % row )

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            return directory
    except OSError:
        print ('Error: Creating directory. ' +  directory)

############################################# HÀM XỬ LÝ INPUT.
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
    min_sup = round( ( total/len(uniqueItem) ) / len(inputDict), 5 )
    print('has %d items, total item: %d, has %d ids' % (len(uniqueItem), total, len(inputDict)) )
    
    return (sorted(itemList), total, min_sup)
# 2.3 Hàm tạo bảng nhị phân từ dict.
# INPUT: dữ liệu dạng dictionary (id: {item1, item2, ...}).
# OUTPUT: 2d list, dòng là các id, cột là các item. Xuất hiện là 1, ngược lại 0.
def create_binary_table(inputDict: dict) -> list:
    (itemList, _, min_sup) = get_item_list_and_count_total(inputDict)
    col = len(itemList)
    row = len(inputDict)
    table = [[0 for r in range(col + 1)] for c in range(row  + 1)]
    idList = list(inputDict.keys())

    table[0][0] = '  '
    for id in range(1, row + 1):
        table[id][0] = idList[id - 1]
    for item in range(1, col + 1):
        table[0][item] = itemList[item - 1]
    
    for indexId in range(len(idList)):
        itemsAtId = inputDict[idList[indexId]]
        for indexItem in range(len(itemList)):
            if itemList[indexItem] in itemsAtId:
               table[indexId + 1][indexItem + 1] = 1
    return (table, min_sup)

############################################# HÀM LẤY TẬP PHỔ BIẾN 1 ITEM.
# Hàm lọc item có tần suất >= minsup.
# itemset là tập phủ phổ biến. (sau khi so minsup).
# Những tập kết hợp gọi là possibleSet.
def get_one_item_set(table: list, minsup: float) -> list:
    numOfId = len(table)
    numOfItem = len(table[0])
    oneItemSet = list()
    minOccur = round(minsup * numOfId) # minsup = frequency(item) / total Id.
    for item in range(1, numOfItem):
        count = 0
        listItem = list()
        for id in range(1, numOfId):
            if table[id][item] == 1:
                count += 1
        if count >= minOccur:
            listItem.append(item)
            oneItemSet.append(listItem)
    return oneItemSet

############################################# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# k_itemset : itemset có k phần tử.
# Ở mỗi k_itemset, duyệt các k_itemset phía sau.
# k_itemset đầu tiên kết hợp với 1 item trong k_itemset phía sau tạo thành (k+1)_itemset mới.
# thật ra Apriori ở đây. =))
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
            
    #allMaxItemSet.append(allItemSet[-1])
    # lấy tên item.
    allMaxItemSetName = list()
    for indexSet in range(len(allMaxItemSet)):
        nameSet = list()
        for item in allMaxItemSet[indexSet]:
            nameSet.append(table[0][item])
        allMaxItemSetName.append(nameSet)
    
    return allMaxItemSetName#,allMaxItemSet

############################################# HÀM MAIN.
def main():
    start = datetime.now()

    link_folder_train = 'D:\\Workspace\\DataMining\\Code\\'
    
    minsup = 0.3
    #inputDict = {'O1': ['i1', 'i7', 'i8'], 'O2': ['i1', 'i2', 'i6', 'i7', 'i8'], 'O3': ['i1', 'i2', 'i6', 'i7'], 'O4': ['i1', 'i8', 'i7'], 'O5': ['i3', 'i4', 'i5', 'i6', 'i8'], 'O6': ['i1', 'i4', 'i5']}
    
    #B1
    inputDict = read_input_file(link_folder_train, 'input.txt')
    #inpDict = read_input_file(link_folder_train, 'GroceryStoreDataSet.txt')
    #inpDict = read_input_file(link_folder_train, 'input2.txt')
    #inpDict = read_input_file(link_folder_train, 'test_da2.input')
    (table, min_sup) = create_binary_table(inputDict)
    #print(apriori(table, min_sup))
    #B2
    #table_to_xlsx(table, 'table', link_folder_train + 'Table\\')
    #table_to_xlsx(table, 'table_input', link_folder_train + 'Table\\')
    #table_to_xlsx(table, 'table_Gro', link_folder_train + 'Table\\')
    ##table_to_xlsx(table, 'table_input2', link_folder_train + 'Table\\')
    #table_to_xlsx(table, 'table_test_da2', link_folder_train + 'Table\\')
    #B3
    #axItemSet1 = apriori(table, minsup)
    maxItemSet2 = apriori(table, min_sup) # 43367 / 169 = 256; 256 / 9835 = 0.03
    #maxItemSet3 = apriori(table, min_sup)
    ##maxItemSet4 = apriori(table, min_sup)
    #maxItemSet5 = apriori(table, min_sup)
    #print(min_sup)
    
    #list_to_txt(maxItemSet1, link_folder_train + 'Max_ItemSet_By_Table\\', 'ItemSet.txt')
    #list_to_txt_no_index(maxItemSet1, link_folder_train + 'String_Max_ItemSet\\', 'ItemSet1str.txt')

    list_to_txt(maxItemSet2, link_folder_train + 'Max_ItemSet_By_Table\\', 'Max_ItemSet_input.txt')
    #list_to_txt_no_index(maxItemSet2, link_folder_train + 'String_Max_ItemSet\\', 'Max_ItemSetinputstr.txt')

    #list_to_txt(maxItemSet3, link_folder_train + 'Max_ItemSet\\', 'Max_ItemSetGro.txt')
    #list_to_txt_no_index(maxItemSet3, link_folder_train + 'String_Max_ItemSet\\', 'Max_ItemSetGrostr.txt')

    #list_to_txt(maxItemSet4, link_folder_train + 'Max_ItemSet\\', 'Max_ItemSet_input2.txt')
    #list_to_txt_no_index(maxItemSet4, link_folder_train + 'String_Max_ItemSet\\', 'Max_ItemSetinput2str.txt')

    #list_to_txt(maxItemSet5, link_folder_train + 'Max_ItemSet\\', 'Max_ItemSet_test_da2.txt')
    #list_to_txt_no_index(maxItemSet5, link_folder_train + 'String_Max_ItemSet\\', 'Max_ItemSettest_da2str.txt')

    print (datetime.now()-start)
    
if __name__ == "__main__": main()
