from collections import defaultdict

def read_input_file(link, fileName, splitType) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    i = 0
    for line in f:
        inpDict[i] = sorted(line.rstrip().split(splitType))
        i += 1
    f.close()
    return inpDict

def read_input_file_plant_input(link, fileName, splitType) -> dict:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    inpDict = defaultdict(dict)
    for line in f:
        lineToList = line.rstrip().split(splitType)
        plant = lineToList[0]
        states = lineToList[1:]
        inpDict[plant] = sorted(states)
    f.close()
    return inpDict

def read_lines_to_list(link, fileName, splitType) -> list:
    f = open(link + fileName, 'r', encoding = 'utf-8')
    List = list()
    [List.append(line.rstrip().split(splitType)) for line in f]
    f.close()
    return List
