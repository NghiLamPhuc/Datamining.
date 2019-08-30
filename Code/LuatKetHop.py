from collections import defaultdict
def read_input_file(link , fileName) -> dict:
    f = open(link + fileName, 'r')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        line = line.rstrip()
        line = sorted(line.split(','))
        inpDict[i] = line
        i += 1
    return inpDict

def get_unique_item_dict(inputDict: dict) -> dict:
    uniqueItem = dict()
    for (_, items) in inputDict.items():
        for item in items:
            if item not in uniqueItem:
                uniqueItem[item] = 1
            else:
                uniqueItem[item] += 1
    return uniqueItem

def get_item_list_and_count_total(inputDict: dict) -> (list, int):
    uniqueItem = get_unique_item_dict(inputDict)
    itemList = list()
    total = 0
    for (item, frequency) in uniqueItem.items():
        itemList.append(item)
        total += frequency
    return (sorted(itemList), total)

def create_binary_table(inputDict: dict) -> list:
    (itemList, _) = get_item_list_and_count_total(inputDict)
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
    return table

#maxItemSet = [['i4', 'i5'], ['i6', 'i8'], ['i1', 'i7', 'i8'], ['i1', 'i2', 'i6', 'i7']]
#table = [[' ', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8'], ['O1', 1, 0, 0, 0, 0, 0, 1, 1], ['O2', 1, 1, 0, 0, 0, 1, 1, 1], ['O3', 1, 1, 0, 0, 0, 1, 1, 0], ['O4', 1, 0, 0, 0, 0, 0, 1, 1], ['O5', 0, 0, 1, 1, 1, 1, 0, 1], ['O6', 1, 0, 0, 1, 1, 0, 0, 0]]
min_conf = 1.0

maxItemSet = [['bottled water', 'whole milk'], ['citrus fruit', 'whole milk'], ['domestic eggs', 'whole milk'], ['other vegetables', 'rolls/buns'], ['other vegetables', 'root vegetables'], ['other vegetables', 'soda'], ['other vegetables', 'tropical fruit'], ['other vegetables', 'whole milk'], ['other vegetables', 'yogurt'], ['pastry', 'whole milk'], ['pip fruit', 'whole milk'], ['rolls/buns', 'sausage'], ['rolls/buns', 'soda'], ['rolls/buns', 'whole milk'], ['rolls/buns', 'yogurt'], ['root vegetables', 'whole milk'], ['soda', 'whole milk'], ['tropical fruit', 'whole milk'], ['whipped/sour cream', 'whole milk'], ['whole milk', 'yogurt']]

link_folder_train = 'D:\\Workspace\\DataMining\\Code\\'

inpDict = read_input_file(link_folder_train, 'input.txt')
table = create_binary_table(inpDict)


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
#print(get_associate_rule(table, get_sub_list(maxItemSet[19]), 1.0))
#for a in ans:
#    print(a)