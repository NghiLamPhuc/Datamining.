from collections import defaultdict

# Hàm lấy danh sách tập con của tập cho trước.
def get_sub_list(List: list) -> list:
    l = len(List)
    allSubList = list() # has 2**len(List) subset. Because each item has two choices, choose or not. 2 * 2 * 2 * ... * 2.
    for i in range(1, 1 << l):
        subList = list()
        for j in range(l):
            if ( i & (1 << j) ) > 0:
                subList.append(List[j])
        allSubList.append(subList)
    
    return allSubList

# Hàm đếm tần suất của itemList (các item xuất hiện cùng trong 1 id).
def count_occur_itemList(inputDict: dict, itemList: list) -> int:
    count = 0
    for id in range(len(inputDict)):
        if set(itemList).issubset(inputDict[id]):
            count += 1
    return count
# Luật = left -> right.
# Đếm tần suất các item trong left, right xuất hiện cùng nhau.
# Chia cho tần suất các item trong left xuất hiện cùng nhau.
def calc_rule_conf(inputDict: dict, left: list, right: list) -> float:
    countLeft = count_occur_itemList(inputDict, left)
    rule = left + right
    countRule = count_occur_itemList(inputDict, rule)
    if countLeft == 0:
        return -1.0
    conf = round(countRule / countLeft, 1)
    
    return (conf, countLeft)

# Hàm lấy các luật kết hợp TỪ MỘT TẬP (muốn lấy hết thì for) thỏa mãn min_conf.
# subList -> tat ca cac luat da sinh ra tu frequentItemSet
# Duyet qua subList, neu 2 sub bat ki giao nhau >= 1 phan tu, thi luat bi trung -> loa.i.
# Neu 2 sub giao nhau = ro^~ng. Tinh conf.
def get_strong_rule(inputDict: dict, subList: list, min_conf: float) -> list:
    strongRules = defaultdict(dict)
    for eachSub in subList:
        for nextSub in subList:
            if not (set(eachSub) & set(nextSub)):
                (conf, supp) = calc_rule_conf(inputDict, eachSub, nextSub)
                if conf >= min_conf:
                    left = ', '.join(eachSub)
                    right = ', '.join(nextSub)
                    strongRules[left][right] = (supp, conf)
                    
    return strongRules
# Ham lay danh sach cac tap con co the sinh ra luat.
# subRule: tat ca left, right.
def get_sub_make_rule(frequentItemSet: list(list())) -> list:
    subRule = list()
    for kItemSet in frequentItemSet:
        allSubList = get_sub_list(kItemSet) # bị trùng lại các tập con. Cần loại trước khi chạy luật.
        for sL in allSubList:
            if sL not in subRule:
                subRule.append(sL)
    return subRule

# Hàm lấy tất cả các strong rules.
def get_all_strong_rule(inputDict: dict, frequentItemSet: list(list()), min_conf: float) -> list:
    ruleList = list()
    subRules = get_sub_make_rule(frequentItemSet)
    
    rules = get_strong_rule(inputDict, subRules, min_conf)
    
    for (left, rights) in rules.items():
        for (right, conf) in rights.items():
            ruleList.append('[' + left + ']' + '->' + '[' + right + ']' + ': ' + str(conf) )
    return ruleList
