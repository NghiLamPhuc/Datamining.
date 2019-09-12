import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_possile_itemset(inputDict: dict, minsup: float, nameFile) -> list:
    allPosItemSet = Frequent_Itemset.get_all_possible_itemset(inputDict, minsup)
    write_file.list_to_txt_with_last_comma(allPosItemSet, './Possible Itemset/', 'Pos_' + nameFile) if allPosItemSet else print('Không có tập phủ phổ biến.')
    return allPosItemSet

def get_FIS(inputDict: dict, minsup: float, nameFile) -> dict:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    write_file.list_to_txt_with_last_comma(maxItemSet, './Frequent Itemset/', 'FIS_' + nameFile) if maxItemSet else print('Không có tập phủ tối đại.')
    return maxItemSet

def get_SR(inputDict: dict, FISDir, FISName, min_conf: float, splitType) -> list:
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, splitType)
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule/', 'Rule_' + FISName)
    return ruleList

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.

    inputDir = './input/'
    nameFileList = sorted(os.listdir(inputDir))
    # File input, các item cách nhau bằng ' ', ', ', ','...
    splitType = [' ', ', ', ',']

    minsupp = 0.3
    minconf = 1.0

    #indexInput = nameFile.index('plants.txt') # luu y khi , minsup = 0.05, minconf = 0.3
    indexInput = 3
    nameFile = nameFileList[indexInput]
    print(nameFile)

    # Dau tien, doc input.
    inputDict = read_file.read_input_file(inputDir, nameFile, splitType[1])
    # inputDict = read_file.read_input_file_plant_input(inputDir, nameFile[indexInput], splitType[-1])
    
    # Chay buoc 1.
    get_FIS(inputDict, minsupp, nameFile)
    get_possile_itemset(inputDict, minsupp, nameFile)
    # Chay buoc 2.
    # FISDir = './Frequent Itemset/'
    # FISNames = sorted(os.listdir(FISDir))
    # FISName = 'FIS_' + nameFile
    # if FISName not in FISNames:
    #    print('Chưa có tập phổ biến.')
    # else:
    #    get_SR(inputDict, FISDir, FISName, minconf, splitType[1])

    print(datetime.now() - start)

if __name__ == "__main__": main()
