import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDir, nameFile: list, minsup: float, splitType, indexFile: int):
    inputDict = read_file.read_input_file(inputDir, nameFile[indexFile], splitType)
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    write_file.list_to_txt_with_last_comma(maxItemSet, './FrequentItemSet/', 'FIS_' + nameFile[indexFile])

def get_SR(FISDir, FISName: list, min_conf: float, splitType, indexFile: int):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName[indexFile], splitType)
    inputDict = read_file.read_input_file(FISDir, FISName[indexFile], splitType)
    ruleList = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, min_conf)
    write_file.list_to_txt(ruleList, './Strong_rule/', 'Rule_' + FISName[indexFile])

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.

    inputDir = './input/'
    nameFile = sorted(os.listdir(inputDir))

    splitType = [' ', ', ', ',']

    minsup = [0.3]
    minconf = 1.0

    indexInput = 0
    indexFIS = 0
    print(nameFile[indexInput])

    # Chay buoc 1.
    get_FIS(inputDir, nameFile, minsup[0], splitType[1], indexInput)
    # Chay buoc 2.
    FISDir = './FrequentItemSet/'
    FISName = sorted(os.listdir(FISDir))
    get_SR(FISDir, FISName, minconf, splitType[1], indexFIS)

    
    
    print(datetime.now() - start)

if __name__ == "__main__": main()
