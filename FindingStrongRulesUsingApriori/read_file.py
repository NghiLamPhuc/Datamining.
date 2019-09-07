from collections import defaultdict

def read_input_file(link, fileName, splitType) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        inpDict[i] = sorted(line.rstrip().split(splitType))
        i += 1
    return inpDict

def read_lines_to_list(link, fileName, splitType) -> list:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    List = list()
    [List.append(line.rstrip().split(splitType)) for line in f]
    return List
