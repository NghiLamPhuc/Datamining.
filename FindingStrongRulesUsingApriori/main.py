import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDict: dict, nameFile: list, minsup: float, splitType, indexFile: int) -> dict:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    write_file.list_to_txt_with_last_comma(maxItemSet, './FrequentItemSet/', 'FIS_' + nameFile[indexFile])
    

def get_SR(inputDict: dict, FISDir, FISName, min_conf: float, splitType):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, splitType)
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule/', 'Rule_' + FISName)

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.

    inputDir = './input/'
    nameFile = sorted(os.listdir(inputDir))
    
    splitType = [' ', ', ', ',']

    minsup = 0.09
    minconf = 0.8

    
    indexInput = nameFile.index('plants.txt') # luu y khi index = 6, minsup = 0.05, minconf = 0.3
    
    print(nameFile[indexInput])

    # Dau tien, doc input.
    #inputDict = read_file.read_input_file(inputDir, nameFile[indexInput], splitType[1])
    inputDict = read_file.read_input_file_plant_input(inputDir, nameFile[indexInput], splitType[-1])
    # Chay buoc 1.
    get_FIS(inputDict, nameFile, minsup, splitType[1], indexInput)
    # Chay buoc 2.
    FISDir = './FrequentItemSet/'
    FISNames = sorted(os.listdir(FISDir))
    FISName = 'FIS_' + nameFile[indexInput]
    if FISName not in FISNames:
       print('Chưa có tập phổ biến.')
    else:
       get_SR(inputDict, FISDir, FISName, minconf, splitType[1])

    
    
    print(datetime.now() - start)

if __name__ == "__main__": main()
