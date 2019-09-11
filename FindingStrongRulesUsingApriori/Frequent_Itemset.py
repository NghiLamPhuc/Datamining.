# INPUT THEO KIỂU DICT: (ID, TRANSACTIONS).
# Hàm lấy list tần suất theo thứ tự item.
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
    return uniqueItem

# HÀM LẤY TẬP PHỔ BIẾN 1 ITEM.
def get_one_itemSet(inputDict: dict, minsup: float) -> list:
    numOfId = len(inputDict)
    uniqueItem = get_unique_item_dict(inputDict)
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

# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# k_itemset : itemset có k phần tử.
# Ở mỗi k_itemset, duyệt các k_itemset phía sau.
# k_itemset đầu tiên kết hợp với 1 item trong k_itemset phía sau tạo thành (k+1)_itemset mới.
# thật ra Apriori ở đây. =))
def get_k_1_itemSet(inputDict: dict, kItemSet: list(list()), minsup: float) -> list:
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
                    # itemset ứng viên. (candidate)
                    possibleSet = kItemSet[curr].copy()
                    possibleSet.append(addItem)
                    
                    if not check_infrequent_subset(kItemSet, possibleSet):
                        checkPossibleAdded = 0
                        for newSet in k_1ItemSet:
                            if set(possibleSet) == set(newSet): # kiểm tra possibleSet đã tồn tại chưa.
                                checkPossibleAdded = 1
                                break
                        if (checkPossibleAdded == 0) and check_itemSet_minsup(inputDict, possibleSet, minsup): # đếm tần suất của bộ mới tạo, có thỏa minsup thì lấy.
                            k_1ItemSet.append(possibleSet)
    return k_1ItemSet

def get_possible_k_1_itemSet(inputDict: dict, kItemSet: list(list()), minsup: float) -> list:
    if len(kItemSet) == 0:
        return 'Het roi!'

    posk_1ItemSet = list() # lưu itemset có k+1 phần tử.
    numOfSet = len(kItemSet) # số itemset có k phần tử.
    numOfItem = len(kItemSet[0]) # số phần tử trong một itemset.

    for curr in range(numOfSet - 1):
        for next in range(curr + 1, numOfSet):
            for item in range(numOfItem):
                addItem = kItemSet[next][item] # item trong k_itemset phía sau.
                if addItem not in kItemSet[curr]: # kiểm tra addItem có trùng với item nào trong itemset hay không.
                    possibleSet = kItemSet[curr].copy()
                    possibleSet.append(addItem)
                    checkPossibleAdded = 0
                    for newSet in posk_1ItemSet:
                        if set(possibleSet) == set(newSet): # kiểm tra possibleSet đã tồn tại chưa.
                            checkPossibleAdded = 1
                            break
                    if (checkPossibleAdded == 0) and check_itemSet_minsup(inputDict, possibleSet, minsup): # đếm tần suất của bộ mới tạo, có thỏa minsup thì lấy.
                    # if check_itemSet_minsup(inputDict, possibleSet, minsup):
                        posk_1ItemSet.append(possibleSet)
    return posk_1ItemSet

# Ham kiem tra theo Apriori property
def check_infrequent_subset(kItemSet: list(list()), possibleSet: list) -> bool:
    k_1 = len(possibleSet)
    for i in range(k_1):
        iSub = possibleSet[:i] + possibleSet[i+1:]
        if iSub not in kItemSet:
            return True
    return False

# Hàm đếm tần suất của một tập thỏa minsup hay không.
# Duyệt từng dòng (là từng transaction), nếu itemset có trong dòng thì sumId++
# 
def check_itemSet_minsup(inputDict: dict, itemSet: list, minsup: float) -> bool:
    if len(itemSet) == 0:
        return False
    
    numOfId = len(inputDict)
    numOfItemInSet = len(itemSet)
    minOccur = round(minsup * numOfId)
    count = 0
    # duyệt theo dòng, mỗi dòng, duyệt theo item trong itemSet
    for (id, items) in inputDict.items():
    #     sumId = 0
        # for item in itemSet:
        #     if item in items:
        #         sumId += 1
        # if sumId == numOfItemInSet:
        #     count += 1
        if set(itemSet).issubset(items):
            count += 1     
        if count >= minOccur:
            return True
    return False

# Hàm lấy các tập phổ biến.
def get_all_possible_itemset(inputDict: dict, minsup):
    allPosItemSet = list()
    preItemSet = get_one_itemSet(inputDict, minsup)
    # [allPosItemSet.append(itemSet) for itemSet in preItemSet]
    allPosItemSet = preItemSet.copy()
    while len(preItemSet) >= 1:
        nextItemSet = get_possible_k_1_itemSet(inputDict, preItemSet, minsup)
        [allPosItemSet.append(itemSet) for itemSet in nextItemSet] 
        preItemSet = nextItemSet
    return allPosItemSet

# Hàm lấy tất cả tập phủ phổ biến.
# Đầu tiên, lấy tất cả tập phủ phổ biến.
# Sau đó bỏ các tập bị tập khác phủ.
def apriori(inputDict: dict, minsup: float) -> list:
    allItemSet = list()
    allFrequentItemSet = list()
    preCover = get_one_itemSet(inputDict, minsup)
    # can bo sung, them tap 1 itemset.
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

    