import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDict: dict, minsup: float, nameFile) -> int:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    if maxItemSet:
        write_file.list_to_txt_with_last_comma(maxItemSet, './Frequent_ItemSet_' + str(minsup) + '/', 'FIS_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến tối đại.')
        return 0

def get_possile_itemset(inputDict: dict, minsup: float, nameFile) -> int:
    allPosItemSet = Frequent_Itemset.get_all_possible_itemset(inputDict, minsup)
    if allPosItemSet:
        write_file.list_to_txt_with_last_comma(allPosItemSet, './Possible_ItemSet_' + str(minsup) + '/', 'Pos_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến.')
        return 0

def get_SR(inputDict: dict, FISDir, FISName, min_conf: float):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, ', ')
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule_' + str(min_conf) + '/', 'Rule_' + FISName) if ruleList else print('Không có luật thỏa mãn.')

def run(inputDict: dict, minsup: float, minconf: float, nameFile):
    ## Chay buoc 1.
    itemset = get_possile_itemset(inputDict, minsup, nameFile)
    freqitemset = get_FIS(inputDict, minsup, nameFile)
    
    ## Chay buoc 2.
    if freqitemset == 1:
        FISDir = './Frequent_ItemSet_' + str(minsup) + '/'
        FISNames = sorted(os.listdir(FISDir))
        FISName = 'FIS_' + nameFile
        if FISName in FISNames:
            get_SR(inputDict, FISDir, FISName, minconf)
    else:
        print('Không có luật, do không có tập phổ biến.')

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.
    
    inputDir = './input/'
    # inputDir = './Generate Input/'
    
    nameFileList = sorted(os.listdir(inputDir))
    splitType = [' ', ', ', ',']
    minsup = 0.3
    minconf = 0.85
    
    # indexInput = nameFileList.index('plants.txt')
    for indexInput in range(8):
        # indexInput = 0
    
        nameFile = nameFileList[indexInput]
        print(nameFile)
        
        inputDict = read_file.read_input_file(inputDir, nameFile, splitType[1])
        # inputDict = read_file.read_input_file_with_row_name(inputDir, nameFile, splitType[2])
        run(inputDict, minsup, minconf, nameFile)
        
        print(datetime.now() - start)

if __name__ == "__main__": main()
