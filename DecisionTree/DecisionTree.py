import os
import math
import make_folder, read_file, write_file

# a = os.getcwd()
# b = os.path.normpath(a + os.sep + os.pardir)
# c = os.path.normpath(b + os.sep + os.pardir)

#
def count_each_tag_from_table(table: list(list()), indexTag: int) -> dict:
    tagCount = dict()
    for row in table:
        if row[indexTag] not in tagCount:
            tagCount[row[indexTag]] = 1
        else:
            tagCount[row[indexTag]] += 1
    return tagCount
# Entropy cho 1 thuoc tinh la tag.
# Sau nay can cai thien, input la list cac thuoc tinh.
def Entropy(table: list(list()), indexTag: int) -> float:
    ans = 0.0
    rows = len(table)
    tagCount = count_each_tag_from_table(table, indexTag)
    for (tag, counts) in tagCount.items():
        num = counts / rows
        ans -= num * math.log(num, 2)
        
    return ans



def main():
    inputDir = './input/'
    splitType = [', ']
    table = read_file.read_lines_to_list(inputDir, 'ClassicWeather.txt', splitType[0])

    print(Entropy(table, -1))
    

if __name__ == "__main__": main()