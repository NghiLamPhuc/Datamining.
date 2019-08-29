from collections import defaultdict

maxItemSet = [['i4', 'i5'], ['i6', 'i8'], ['i1', 'i7', 'i8'], ['i1', 'i2', 'i6', 'i7']]
table = [[' ', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8'], ['O1', 1, 0, 0, 0, 0, 0, 1, 1], ['O2', 1, 1, 0, 0, 0, 1, 1, 1], ['O3', 1, 1, 0, 0, 0, 1, 1, 0], ['O4', 1, 0, 0, 0, 0, 0, 1, 1], ['O5', 0, 0, 1, 1, 1, 1, 0, 1], ['O6', 1, 0, 0, 1, 1, 0, 0, 0]]
min_conf = 1.0

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

def get_associate_rule(subList: list) -> list:
    associateRules = defaultdict(list)
    for eachSub in subList:
        for nextSub in subList:
            if not (set(eachSub) & set(nextSub)):
                left = ' '.join(eachSub)
                right = ' '.join(nextSub)
                associateRules[left].append(right)
                
    return associateRules

def count_occur_itemList(table: list, itemList: list) -> int:
    count = 0
    for id in range(len(table)):
        sumId = 0
        for item in itemList:
            if table[id][item] == 1:
                sumId += 1
        if sumId == len(itemList):
            count += 1
    return count

def check_rule_min_conf(table: list, left: list, right: list, min_conf: float) -> bool:
    countLeft = count_occur_itemList(table, left)
    rules = list(set(left) ^ set(right))
    countRule = count_occur_itemList(table, rules)

    return ((countRule / countLeft) >= min_conf)


subList = get_sub_list(maxItemSet[3])
#listRule = get_associate_rule(subList)
#print(listRule[5].split(' -> '))
print(get_associate_rule(subList))
print(*table, sep = '\n')