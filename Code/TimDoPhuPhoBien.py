
from collections import defaultdict
# import
######################################
#
# Lấy danh sách các giá trị PHÂN BIỆT.
#
def get_unique_item_list(table: dict) -> list:    
    uniqueItemList = set()
    for (_, Items) in table.items():
        uniqueItemList = uniqueItemList.union(set(Items))
    return sorted(uniqueItemList)
#
# Đếm tất cả các giá trị, (để kiểm tra các hàm).
#
def count_all_item(table: dict) -> int:
    count = 0
    for (_, items) in table.items():
        count += len(items)
    return count
#
# Đếm tần suất của một giá trị.
#
def get_count_one_item_list(items: list, table: dict) -> list:
    oneItemCountList = dict()
    for item in items:
        for (_, itemList) in table.items():
            if item in itemList:
                if item not in oneItemCountList:
                    oneItemCountList[item] = 1
                else:
                    oneItemCountList[item] += 1
    return oneItemCountList
#
# Đếm tần suất của một TẬP-x-phần tử giá trị.
#

#
# Lọc lại những item xuất hiện >= minsup.
#
def get_one_item_list_after_minsup(oneItemCount: dict, minsup: int, totalItem :int) -> list:
    afterMinsup = list()
    threshold = round(minsup * totalItem)
    for (item, count) in oneItemCount.items():
        if count >= threshold:
            afterMinsup.append(item)
    return afterMinsup

#
# Đếm tần suất cặp-2-item.
#
def get_count_two_items_list(oneCover: list, table: dict) -> dict:
    twoCount = defaultdict(dict)
    numOfOneCover = len(oneCover)
    for curr in range(numOfOneCover - 1):
        for next in range(curr + 1, numOfOneCover):
            for (_, itemList) in table.items():
                if (oneCover[curr] in itemList) and (oneCover[next] in itemList):
                    if (oneCover[curr] not in twoCount) or (oneCover[next] not in twoCount[oneCover[curr]]):
                        twoCount[oneCover[curr]][oneCover[next]] = 1
                    else:
                        twoCount[oneCover[curr]][oneCover[next]] += 1

    return twoCount


minsup = 0.3
#table = {100: ['A', 'C', 'D', 'I'], 200: ['A', 'C', 'I'], 300: ['C', 'E', 'I'], 400: ['A', 'B', 'D', 'E'], 500: ['B', 'D', 'I'], 600: ['A', 'B', 'D', 'E']}
table = {'O1': ['i1', 'i7', 'i8'], 'O2': ['i1', 'i2', 'i6', 'i7', 'i8'], 'O3': ['i1', 'i2', 'i6', 'i7'], 'O4': ['i1', 'i8', 'i7'], 'O5': ['i3', 'i4', 'i5', 'i6', 'i8'], 'O6': ['i1', 'i4', 'i5']}

items = get_unique_item_list(table)
totalItems = len(items)

oneCount = get_count_one_item_list(items, table)
oneCover = get_one_item_list_after_minsup(oneCount, minsup, totalItems)

twoCount = get_count_two_items_list(oneCover, table)
#twoCover = get_item_list_after_minsup(twoCount, minsup, totalItems)
print(oneCover)

