from collections import defaultdict

# Hàm đọc file dạng nhiều dòng, mỗi dòng là transaction.
# mỗi transaction chứa item.
def read_lines_to_dict(link, fileName, splitType) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        inpDict[i] = sorted(line.rstrip().split(splitType))
        i += 1
    f.close()
    return inpDict
# Hàm đọc file dạng nhiều dòng, mỗi dòng là transaction.
# Cột đầu tiên là tên transaction.
def read_lines_to_dict_with_row_name(link, fileName, splitType) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    for line in f:
        lineToList = line.rstrip().split(splitType)
        rowName = lineToList[0]
        items = lineToList[1:]
        inpDict[rowName] = sorted(items)
    f.close()
    return inpDict

def read_lines_to_list(link, fileName, splitType) -> list:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    List = list()
    [List.append(line.rstrip().split(splitType)) for line in f]
    f.close()
    return List

def read_columns_to_list(link, fileName, splitType) -> list:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    List = []
    cols = 0
    for line in f:
        cols = len(line.rstrip().split(', '))
        break
    for col in range(cols):
        List.append([x.rstrip().split(', ')[col] for x in f.readlines()])

    f.close()
    return List