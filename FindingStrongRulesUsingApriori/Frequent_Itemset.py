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

def get_total_items(inputDict: dict) -> int:
    count = 0
    for (id, items) in inputDict.items():
        count += len(items) - 1
    return count
# HÀM LẤY TẬP PHỔ BIẾN 1 ITEM.
# Đếm theo item_list, duyệt từng dòng inputDict, nếu item xuất hiện >= số lần cần thiết, lấy.
# oneItemSet là list lớn, chứa các list nhỏ, mỗi list nhỏ là 1_itemset.
def get_one_itemSet(inputDict: dict, minsup: float) -> list(list()):
    numOfId = len(inputDict)
    uniqueItem = get_unique_item_dict(inputDict)
    itemList = sorted(list(uniqueItem.keys()))
    oneItemSet = list(list())
    minOccur = round(minsup * numOfId) # minsup = frequency(item) / total Id.
    for item in itemList:
        count = 0
        for (_, items) in inputDict.items():
            if item in items:
                count += 1
            if count == minOccur:
                oneItemSet.append([item])
                break
    return oneItemSet

# HÀM LẤY TẬP PHỔ BIẾN >= 2 PHẦN TỬ.
# Tìm các tập k+1 phần tử từ các tập k phần tử.
# k_itemset : itemset có k phần tử. k_1 = k+1
# Duyệt qua list k_itemset, tại mỗi k_itemset, ghép đôi một với các k_itemset phía sau.
# Lấy 1 item trong k_itemset phía sau, ghép với k_itemset đang duyệt. -> gọi tập mới này là possibleSet (hay candidate).
# Kiểm tra possibleSet này đã từng lấy chưa? Kiểm tra các tập con possibleSet có bị infrequent không? Kiểm tra min support.
def get_k_1_itemSet(inputDict: dict, kItemSet: list(list()), minsup: float) -> list:
    if len(kItemSet) == 0:
        return 'kItemset input rỗng!'

    # lưu itemset có k+1 phần tử.
    k_1ItemSet = list()
    # số itemset có k phần tử.
    numOfSet = len(kItemSet)
    # số phần tử trong một itemset.
    numOfItem = len(kItemSet[0])

    for curr in range(numOfSet - 1):
        for next in range(curr + 1, numOfSet):
            for item in range(numOfItem):
                # item trong k_itemset phía sau.
                addItem = kItemSet[next][item]
                # kiểm tra addItem có trùng với item nào trong itemset hay không.
                if addItem not in kItemSet[curr]:
                    # itemset ứng viên. (candidate)
                    possibleSet = kItemSet[curr].copy()
                    possibleSet.append(addItem)
                    # kiểm tra possibleSet đã tồn tại trong k_1ItemSet chưa.
                    if not check_in_list(k_1ItemSet, possibleSet):
                        if not check_infrequent_subset(kItemSet, possibleSet):
                            # đếm tần suất của bộ mới tạo, có thỏa minsup thì lấy.
                            if check_itemset_minsup(inputDict, possibleSet, minsup):
                                k_1ItemSet.append(possibleSet)
    return k_1ItemSet

# Hàm kiểm tra itemset đã từng thêm vào list chưa.
def check_in_list(List: list, candidate: list) -> bool:
    for iList in List:
        if set(iList) == set(candidate):
            return True
    return False

# Ham kiem tra theo Apriori property.
# "All non-empty subsets of a frequent itemset must also be frequent"
def check_infrequent_subset(kItemSet: list(list()), possibleSet: list) -> bool:
    k_1 = len(possibleSet)
    for i in range(k_1):
        iSub = possibleSet[:i] + possibleSet[i+1:]
        if iSub not in kItemSet:
            return True
    return False

# Hàm đếm tần suất của một tập thỏa minsup hay không.
# min occurance số lần xuất hiện tối thiểu theo min_support.
# Duyệt từng dòng (transaction) trong inputDict, nếu itemset có thì count++, đến khi = min occurance.
def check_itemset_minsup(inputDict: dict, itemset: list, minsup: float) -> bool:
    if len(itemset) == 0:
        return False
    
    numOfId = len(inputDict)
    minOccur = round(minsup * numOfId)
    count = 0
    # duyệt theo dòng, mỗi dòng, duyệt theo item trong itemset
    for (_, items) in inputDict.items():
        if set(itemset).issubset(items):
            count += 1     
        if count == minOccur:
            return True
    return False

# Hàm lấy các tập phổ biến.
# Lấy tập phủ phổ biến 1 phần tử.
# Duyệt đến khi tập phủ phổ biến chỉ còn 1 tập.
# Mỗi bước lặp, tìm tập phủ phổ biến k+1 phần tử từ tập phổ biến k phần tử.
def get_all_possible_itemset(inputDict: dict, minsup: float) -> list:
    allPosItemSet = list()
    preItemSet = get_one_itemSet(inputDict, minsup)
    allPosItemSet = preItemSet.copy()
    while len(preItemSet) >= 1:
        nextItemSet = get_k_1_itemSet(inputDict, preItemSet, minsup)
        [allPosItemSet.append(itemSet) for itemSet in nextItemSet] 
        preItemSet = nextItemSet
    return allPosItemSet

# Hàm lấy tất cả tập phủ phổ biến.
# Đầu tiên, lấy tất cả tập phủ phổ biến.
# Sau đó bỏ các tập bị tập khác phủ.
def apriori(inputDict: dict, minsup: float) -> list:
    allFrequentItemSet = list()
    allItemSet = get_all_possible_itemset(inputDict, minsup)
    
    if not allItemSet:
        print('Khong co itemset thoa man min_supp.')
        return allItemSet

    # Loại itemset bị chứa.
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
