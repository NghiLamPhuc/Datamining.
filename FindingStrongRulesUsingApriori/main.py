import Frequent_Itemset
import Strong_rules
import read_file
import write_file

from datetime import datetime
import os

def get_FIS(inputDict: dict, minsup: float, nameFile) -> int:
    maxItemSet = Frequent_Itemset.apriori(inputDict, minsup)
    if maxItemSet:
        write_file.list_to_txt_with_last_comma(maxItemSet, './RESULT/Frequent_ItemSet_minsup_' + str(minsup) + '/', 'FIS_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến tối đại.')
        return 0

def get_possile_itemset(inputDict: dict, minsup: float, nameFile) -> int:
    allPosItemSet = Frequent_Itemset.get_all_possible_itemset(inputDict, minsup)
    if allPosItemSet:
        write_file.list_to_txt_with_last_comma(allPosItemSet, './RESULT/Possible_ItemSet_minsup_' + str(minsup) + '/', 'Pos_' + nameFile)
        return 1
    else:
        #print('Không có tập phổ biến.')
        return 0

def get_SR(inputDict: dict, FISDir, FISName, minconf: float, minsupp: float):
    frequentItemSet = read_file.read_lines_to_list(FISDir, FISName, ', ')
    (ruleList, topTenRules) = Strong_rules.get_all_strong_rule(inputDict, frequentItemSet, minconf)
    write_file.list_to_txt(ruleList, './RESULT/Strong_rule_minsupp_' + str(minsupp) + ' minconf_' + str(minconf) + '/', 'Rule_' + FISName) if ruleList else print('Không có luật thỏa mãn.')
    write_file.list_to_txt(topTenRules, './RESULT/Topten_Strong_rule_minsupp_' + str(minsupp) + ' minconf_' + str(minconf) + '/', '10_Rules_' + FISName) if topTenRules else print('Không có luật thỏa mãn.')

def run(inputDict: dict, minsupp: float, minconf: float, nameFile):
    ## Chay buoc 1.
    itemset = get_possile_itemset(inputDict, minsupp, nameFile)
    freqitemset = list()
    if itemset == 1:
        freqitemset = get_FIS(inputDict, minsupp, nameFile)
    else:
        print('Không có tập phủ phổ biến!')
    
    ## Chay buoc 2.
    if freqitemset == 1:
        FISDir = './RESULT/Frequent_ItemSet_minsup_' + str(minsupp) + '/'
        FISNames = sorted(os.listdir(FISDir))
        FISName = 'FIS_' + nameFile
        if FISName in FISNames:
            get_SR(inputDict, FISDir, FISName, minconf, minsupp)
    else:
        print('Không có luật, do không có tập phổ biến.')

def main():
    start = datetime.now()
    ## Cac thiet lap dau tien.
    
    inputDir = './input/'
    # inputDir = './Generate Input/'
    # print(Frequent_Itemset.get_total_items(read_file.read_input_file(inputDir, 'plants.txt', splitType[2]))) # Tổng số item trong input.
    nameFileList = sorted(os.listdir(inputDir))
    splitType = [' ', ', ', ',']
    # minsupp = 0.3
    # minconf = 0.9
    
    minsupp = 0.1
    minconf = 0.85

    # chạy 7 file input đầu, trừ plants.txt
    # for indexInput in range(len(nameFileList) - 1):
    #     nameFile = nameFileList[indexInput]
    #     print(nameFile)
        
    #     # inputDict = read_file.read_input_file(inputDir, nameFile, splitType[1]) # input khong co te^n transaction, khi đó, trong Strong_rule đổi hàm count_occur_itemlist.
    #     inputDict = read_file.read_input_file_with_row_name(inputDir, nameFile, splitType[1])
    #     run(inputDict, minsupp, minconf, nameFile)
    
    ## Chạy plants.txt
    indexInput = nameFileList.index('plants.txt')
    nameFile = nameFileList[indexInput]
    print(nameFile)

    inputDict = read_file.read_input_file_with_row_name(inputDir, nameFile, splitType[1])
    run(inputDict, minsupp, minconf, nameFile)
    # minsup = 0.1
    # while (minsup < 0.9):
    #     run(inputDict, minsup, minconf, nameFile)
    #     minsup += 0.1
    #     print(minsup)

    
    print(datetime.now() - start)

if __name__ == "__main__": main()
