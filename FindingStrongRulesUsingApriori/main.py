import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDict: dict, minsup: float, splitType, nameFile) -> dict:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    # print('Tập phổ biến tối đại: ')
    # print(maxItemSet)
    write_file.list_to_txt_with_last_comma(maxItemSet, './FrequentItemSet/', 'FIS_' + nameFile)
    return maxItemSet    

def get_possile_itemset(inputDict: dict, minsup: float, nameFile) -> list:
    allPosIS = list()
    print('Tất cả tập phổ biến.')
    preItemSet = Frequent_Itemset.get_one_itemSet(inputDict, minsup)
    [allPosIS.append(itemSet) for itemSet in preItemSet]
    while len(preItemSet) >= 1:
        nextItemSet = Frequent_Itemset.get_k_1_itemSet(inputDict, preItemSet, minsup)
        [allPosIS.append(itemSet) for itemSet in nextItemSet]
        preItemSet = nextItemSet
    write_file.list_to_txt_with_last_comma(allPosIS, './Possible Itemset/', 'Pos_' + nameFile)
    return allPosIS

def get_SR(inputDict: dict, FISDir, FISName, min_conf: float, splitType):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, splitType)
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule/', 'Rule_' + FISName)

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.

    inputDir = './input/'
    nameFileList = sorted(os.listdir(inputDir))
    
    splitType = [' ', ', ', ',']

    minsup = 0.3
    minconf = 1.0

    #indexInput = nameFile.index('baitapbuoi3.txt') # luu y khi index = 6, minsup = 0.05, minconf = 0.3
    indexInput = 1
    nameFile = nameFileList[indexInput]
    print(nameFile)

    # Dau tien, doc input.
    inputDict = read_file.read_input_file(inputDir, nameFile, splitType[1])
    # inputDict = read_file.read_input_file_plant_input(inputDir, nameFile[indexInput], splitType[-1])
    
    # Chay buoc 1.
    get_FIS(inputDict, minsup, splitType[1], nameFile)
    # Chay buoc 2.
    FISDir = './FrequentItemSet/'
    FISNames = sorted(os.listdir(FISDir))
    FISName = 'FIS_' + nameFile
    if FISName not in FISNames:
       print('Chưa có tập phổ biến.')
    else:
       get_SR(inputDict, FISDir, FISName, minconf, splitType[1])

    print(datetime.now() - start)

if __name__ == "__main__": main()
