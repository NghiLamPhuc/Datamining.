import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDict: dict, minsup: float, splitType, nameFile) -> int:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    if maxItemSet:
        write_file.list_to_txt_with_last_comma(maxItemSet, './Frequent_ItemSet/', 'FIS_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến tối đại.')
        return 0

def get_possile_itemset(inputDict: dict, minsup: float, nameFile) -> int:
    allPosItemSet = Frequent_Itemset.get_all_possible_itemset(inputDict, minsup)
    if allPosItemSet:
        write_file.list_to_txt_with_last_comma(allPosItemSet, './Possible_ItemSet/', 'Pos_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến.')
        return 0

def get_SR(inputDict: dict, FISDir, FISName, min_conf: float, splitType):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, splitType)
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule/', 'Rule_' + FISName) if ruleList else print('Không có luật thỏa mãn.')

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.
    inputDir = './input/'
    # inputDir = './Generate Input/'
    nameFileList = sorted(os.listdir(inputDir))
    
    splitType = [' ', ', ', ',']

    minsup = 0.3
    minconf = 0.8

    #indexInput = nameFileList.index('z.txt') # luu y khi plants.txt, minsup = 0.05, minconf = 0.3
    indexInput = 0
    nameFile = nameFileList[indexInput]
    print(nameFile)

    ## Dau tien, doc input.
    inputDict = read_file.read_input_file(inputDir, nameFile, splitType[1])
    # inputDict = read_file.read_input_file_plant_input(inputDir, nameFile[indexInput], splitType[-1])
    
    # # Chay buoc 1.
    itemset = get_possile_itemset(inputDict, minsup, nameFile)
    freqitemset = get_FIS(inputDict, minsup, splitType[1], nameFile)
    
    # ## Chay buoc 2.
    if freqitemset == 1:
        FISDir = './Frequent_ItemSet/'
        FISNames = sorted(os.listdir(FISDir))
        FISName = 'FIS_' + nameFile
        if FISName in FISNames:
            get_SR(inputDict, FISDir, FISName, minconf, splitType[1])
    else:
        print('Không có luật, do không có tập phổ biến.')
    # print(Strong_rules.get_subsets([1,2,3,4,5,6,7]))
    # print(Strong_rules.get_sub_list([1,2,3,4,5,6,7]))
    print(datetime.now() - start)

if __name__ == "__main__": main()
