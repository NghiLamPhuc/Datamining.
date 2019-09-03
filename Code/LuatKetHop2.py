from collections import defaultdict
from datetime import datetime

link_input = 'D:\\Workspace\\DataMining\\Code\\Input\\'

def display_defaultdict(rules: defaultdict(list)):
    for (left, rightList) in rules.items():
        for right in rightList:
            print('%s -> %s' % (left, right))

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
# >= min_conf thì trả về tỉ lệ, ngược lại -1.
def check_rule_min_conf(inputDict: dict, left: list, right: list, min_conf: float) -> float:
    countLeft = count_occur_itemList(inputDict, left)
    rules = list(set(left) ^ set(right))
    countRule = count_occur_itemList(inputDict, rules)
    conf = countRule / countLeft
    
    return conf if (conf >= min_conf) else -1.0

# Hàm lấy các luật kết hợp TỪ MỘT TẬP (muốn lấy hết thì for) thỏa mãn min_conf. 
def get_associate_rule(inputDict: dict, subList: list, min_conf: float) -> list:
    associateRules = defaultdict(dict)
    for eachSub in subList:
        for nextSub in subList:
            if not (set(eachSub) & set(nextSub)):
                conf = check_rule_min_conf(inputDict, eachSub, nextSub, min_conf)
                if conf > -1.0:
                    left = ' '.join(eachSub)
                    right = ' '.join(nextSub)
                    associateRules[left][right] = conf
                    
    return associateRules

# Hàm lấy tất cả các strong rules.
def get_all_strong_rule(inputDict: dict, frequentItemSet: list, min_conf: float) -> list:
    ruleList = list()
    for iset in frequentItemSet:
        subList = get_sub_list(iset)
        rules = get_associate_rule(inputDict, subList, min_conf)
        for (left, rights) in rules.items():
            for (right, conf) in rights.items():
                ruleList.append('[' + left + ']' + '->' + '[' + right + ']' + ': ' + str(conf) )
    return ruleList

def main():
    start = datetime.now()

    min_conf = 0.5
    frequentItemSet = [['i1', 'i7'],['i6', 'i8'],['i1', 'i2', 'i6'],['i1', 'i7', 'i8']]
    #frequentItemSet = [['B', 'H'], ['A', 'H', 'M', 'N']]
    name = ['baitapbuoi2.txt', 'baitapthem7.txt']
    inputDict = read_input_file(link_input, name[0])
    
    
    ruleList = get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    print(*ruleList, sep = '\n')

    print (datetime.now()-start)
    
if __name__ == "__main__": main()
