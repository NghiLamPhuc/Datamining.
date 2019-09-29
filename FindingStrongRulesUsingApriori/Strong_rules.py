from collections import defaultdict
from heapq import nlargest
from operator import itemgetter
from pprint import pprint
# from graphviz import Digraph
# import os
# os.environ["PATH"] += os.pathsep + 'C:/Users/NghiLam/Anaconda3/Library/bin/graphviz'

# Hàm lấy danh sách tập con của tập cho trước.
def get_sub_list(List: list) -> list(list()):
    l = len(List)
    allSubList = list() # has 2**len(List) subset. Because each item has two choices, choose or not. 2 * 2 * 2 * ... * 2.
    for i in range(1, 1 << l):
        subList = list()
        for j in range(l):
            if ( i & (1 << j) ) > 0:
                subList.append(List[j])
        allSubList.append(subList)
    return allSubList
# Hàm lấy danh sách tập con của tập cho trước, bỏ đi tập rỗng và tập input.
# Kết quả là 1 list chứa các list.
# Duyệt từng item trong list, đưa item đó vào 1 list.
# Ghép list trên với các list con trong list kết quả.
def get_subsets(List: list) -> list():
    List.sort()
    # result = list() # result.append(list()) # same same :))
    result = [[]]
    ##################### Viet Pythonic cho gon lai.
    # for item in List:#     temp = []#     itemList = []#     itemList.append(item)#     for i in result:#         temp.append(i + itemList)#     result += temp
    for item in List:
        result += [i + [item] for i in result]
    del result[0]
    del result[-1]
    return result

# Hàm đếm tần suất của itemList (các item xuất hiện cùng trong 1 id).
def count_occur_itemList(inputDict: dict, itemList: list) -> int:
    count = 0
    # for id in range(len(inputDict)):
    for (id, items) in inputDict.items():
        if set(itemList).issubset(items):
            count += 1
    return count
def count_occur_itemList_2(inputDict: dict, itemList: list) -> int:
    count = 0
    for id in range(len(inputDict)):
        if set(itemList).issubset(inputDict[id]):
            count += 1
    return count
# Luật = left -> right.
# Đếm tần suất các item trong left, right xuất hiện cùng nhau.
# Chia cho tần suất các item trong left xuất hiện cùng nhau.
def calc_rule_conf(inputDict: dict, cLeft: int, rule: list) -> (float, int):
    countRule = count_occur_itemList(inputDict, rule)
    if countRule == 0:
        return (-1.0, -1)
    # conf = round(countRule / cLeft, 1)
    conf = countRule / cLeft
    return (conf, countRule)

# Hàm lấy các luật kết hợp TỪ MỘT TẬP (muốn lấy hết thì for) thỏa mãn min_conf.
# subList -> tat ca cac luat da sinh ra tu frequentItemSet
# Duyet qua subList, neu 2 sub bat ki giao nhau >= 1 phan tu, thi luat bi trung -> loa.i.
# Neu 2 sub giao nhau = ro^~ng. Tinh conf.
def get_strong_rule(inputDict: dict, subList: list, min_conf: float) -> defaultdict(dict):
    strongRules = defaultdict(dict)
    counted = dict()
    for eachSub in subList:
        cLeft = count_occur_itemList(inputDict, eachSub)
        if cLeft > 0:
            for nextSub in subList:
                if not (set(eachSub) & set(nextSub)):
                    rule = sorted(eachSub + nextSub)
                    strRule = str(rule)
                    if strRule in counted:
                        cRule = counted[strRule]
                        conf = cRule / cLeft
                    else:
                        (conf, cRule) = calc_rule_conf(inputDict, cLeft, rule )
                        if cRule > 0:
                            counted[strRule] = cRule
                    if conf >= min_conf:
                        left = ', '.join(eachSub)
                        right = ', '.join(nextSub)
                        strongRules[left][right] = [conf, cLeft, cRule]
                        
    return strongRules

# Ham lay danh sach cac tap con co the sinh ra luat.
# subRule: tat ca left, right.
def get_sub_make_rule(frequentItemSet: list(list())) -> list:
    subRule = list()
    for kItemSet in frequentItemSet:
        # bị trùng lại các tập con. Cần loại trước khi chạy luật.
        allSubList = get_subsets(kItemSet)
        for sL in allSubList:
            if sL not in subRule:
                subRule.append(sL)
    return subRule

# Hàm ở trên, lấy tất cả tập freqItemSet xẻ ra các tập con.
# Hàm này sẽ xẻ tập con theo từng ItemSet trong freqItemSet.
def get_sub_make_rule_2(freqItemSetX: list()) -> list:
    return get_subsets(freqItemSetX)

# Hàm lấy tất cả các strong rules.
def get_all_strong_rule(inputDict: dict, frequentItemSet: list(list()), min_conf: float) -> list:
    ruleList = list()
    subRules = get_sub_make_rule(frequentItemSet)
    rules = get_strong_rule(inputDict, subRules, min_conf)
    topTen = get_top_ten(rules)
    for (left, rights) in rules.items():
        for (right, someVal) in rights.items():
            # ruleList.append('[ %s ] -> [ %s ]: (conf=%f, left=%d, rule=%d)' % (left, right, someVal[0], someVal[1], someVal[2]) )
            ruleList.append(' %s -> %s: (conf=%f, left=%d, rule=%d)' % (left, right, someVal[0], someVal[1], someVal[2]) )
    
    return (ruleList, topTen)
# Hàm ở trên, bị lỗi -> xét các kết hợp, mặc dù chúng không cùng ItemSet.
# Hàm này sửa lỗi đó. Chạy thử thôi. Chưa chắc đúng nên còn cmt ở đây. Éc Éc.
def get_all_strong_rule_2(inputDict: dict, frequentItemSet: list(list()), min_conf: float) -> list:
    ruleList = list()
    allRules = defaultdict(dict)
    for itemSet in frequentItemSet:
        subRules = get_sub_make_rule_2(itemSet)
        rules = get_strong_rule(inputDict, subRules, min_conf)
        for (left, rights) in rules.items():
            allRules[left] = rights

    topTen = get_top_ten(allRules)
    for (left, rights) in allRules.items():
        for (right, someVal) in rights.items():
            ruleList.append(' %s -> %s: (conf=%f, left=%d, rule=%d)' % (left, right, someVal[0], someVal[1], someVal[2]) )
    
    return (ruleList, topTen)
# For Fun!!!
def get_top_ten(rules: dict) -> list:
    flattened = ((outerkey, innerkey, value) for (outerkey, innerdict) in rules.items() for (innerkey, value) in innerdict.items())
    topTen = nlargest(10, flattened, key = itemgetter(2))
    return topTen
