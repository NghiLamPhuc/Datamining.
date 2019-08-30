from collections import defaultdict

maxItemSet = [['i4', 'i5'], ['i6', 'i8'], ['i1', 'i7', 'i8'], ['i1', 'i2', 'i6', 'i7']]
table = [[' ', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8'], ['O1', 1, 0, 0, 0, 0, 0, 1, 1], ['O2', 1, 1, 0, 0, 0, 1, 1, 1], ['O3', 1, 1, 0, 0, 0, 1, 1, 0], ['O4', 1, 0, 0, 0, 0, 0, 1, 1], ['O5', 0, 0, 1, 1, 1, 1, 0, 1], ['O6', 1, 0, 0, 1, 1, 0, 0, 0]]
min_conf = 1.0

def display_defaultdict(rules: defaultdict(list)):
    for (left, rightList) in rules.items():
        for right in rightList:
            print('%s -> %s' % (left, right))

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

# Hàm lấy các luật kết hợp thỏa mãn min_conf.
def get_associate_rule(table: list, subList: list, min_conf: float) -> list:
    associateRules = defaultdict(list)
    for eachSub in subList:
        for nextSub in subList:
            if not (set(eachSub) & set(nextSub)):
                if check_rule_min_conf(table, eachSub, nextSub, min_conf):
                    left = ' '.join(eachSub)
                    right = ' '.join(nextSub)
                    associateRules[left].append(right)
                
    return associateRules
# Hàm đếm tần suất của itemList (các item xuất hiện cùng trong 1 id).
def count_occur_itemList(table: list, itemList: list) -> int:
    count = 0
    for id in range(len(table)):
        sumId = 0
        for item in itemList:
            if table[id][table[0].index(item)] == 1:
                sumId += 1
        if sumId == len(itemList):
            count += 1
    return count
# Luật = left -> right.
# Đếm tần suất các item trong left, right xuất hiện cùng nhau.
# Chia cho tần suất các item trong left xuất hiện cùng nhau.
# >= min_conf thì TRUE.
def check_rule_min_conf(table: list, left: list, right: list, min_conf: float) -> bool:
    countLeft = count_occur_itemList(table, left)
    rules = list(set(left) ^ set(right))
    countRule = count_occur_itemList(table, rules)

    return ((countRule / countLeft) >= min_conf)

ans = list()
for indexSet in range(len(maxItemSet)):
    subList = get_sub_list(maxItemSet[indexSet])
    listRule = get_associate_rule(table, subList, min_conf)
    if len(listRule) > 0:
        ans.append(listRule)

for a in ans:
    print(a)