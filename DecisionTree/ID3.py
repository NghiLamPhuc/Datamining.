import os
import numpy as np
import pandas as pd
eps = np.finfo(float).eps # truong hop neu log(0) se bi loi. log(0+eps) khong bi loi.

import math
import pprint
import csv

def import_data(inputDir: str, name: str) -> pd.DataFrame:
    dataDF = pd.read_csv(inputDir + name, encoding = 'utf-8')
    columns = list(dataDF.columns) # attributes = columns[1 : len(columns) - 1] # classifies = columns[-1]
    return dataDF.drop(columns[0], axis = 1) 

def find_entropy(df) -> float:
    Class = df.keys()[-1] # thuoc tinh phan lop
    entropy = 0
    values = df[Class].unique() # thuoc tinh con lai.
    for value in values:
        fraction = df[Class].value_counts()[value] / len(df[Class])
        entropy -= fraction * math.log(fraction, 2)
    return entropy
  
def find_entropy_attribute(df, attribute) -> float:
  Class = df.keys()[-1] # Thuộc tính phân lớp. VD: Play.
  target_variables = df[Class].unique() # Các giá trị của thuộc tính phân lớp. VD: Play có Yes, No.
  variables = df[attribute].unique() # Ứng với attribute, sẽ lấy các giá trị. VD: attribute : outlook. variables[sunny, overcast, rainy].
  entropy2 = 0
  for variable in variables:
      entropy = 0
      for target_variable in target_variables: # vd: [true, false]
          numerator = len(df[attribute][df[attribute] == variable][df[Class] == target_variable])
          denominator = len(df[attribute][df[attribute] == variable])
          fraction = numerator / (denominator + eps) # numer / denom - VD: [outlook:sunny and play:true] / [outlook:sunny]
          entropy += -fraction * math.log(fraction + eps, 2)
      fraction2 = denominator / len(df)
      entropy2 += -fraction2 * entropy
  return abs(entropy2)


def find_winner(df):
    # Entropy_att = []
    IG = []
    for key in df.keys()[:-1]:
#         Entropy_att.append(find_entropy_attribute(df,key))
        IG.append(find_entropy(df)-find_entropy_attribute(df,key))
    return df.keys()[:-1][np.argmax(IG)]
  
  
def get_subtable(df, node, value) -> pd.DataFrame:
  return df[df[node] == value].reset_index(drop=True)


def buildTree(df, tree=None) -> dict: 
    Class = df.keys()[-1] # Thuoc tinh phan lop.
    node = find_winner(df)# thuoc tinh MAX information gain
    attValue = np.unique(df[node]) #VD outlook co 3 gia tri: sunny, overcast, rainy
    
    if tree is None:                    
        tree={}
        tree[node] = {}
    
   #We make loop to construct a tree by calling this function recursively. 
    #In this we check if the subset is pure and stops if it is pure. 

    for value in attValue:
        
        subtable = get_subtable(df,node,value) # lay tu df nhung dong co gia tri value cua thuoc tinh node.
        '''    
            Đếm số dòng có value của node VÀ từng thuộc tính phân lớp. 
            VD: Thuoc tinh co info gain cao nhat la node = outlook, giá trị value = sunny.
            clValue là [yes, no]. Đếm sunny yes có 9, sunny no có 5. clValue = [yes,no], counts= [9,5]
        '''
        clValue,counts = np.unique(subtable[Class], return_counts = True) 
        
        '''
            Nếu counts = 1, nghĩa là tại value của node đang đếm, chỉ có 1 thuộc tính phân lớp.
            Thì thêm vào cây luôn. clValue[0] sẽ là lớp được phân. 
                VD: overcast chỉ có yes.
            Ngược lại, nếu counts > 1. Thì tại value của node đang đếm, cần duyệt tiếp các nhánh.
                VD: sunny sẽ có 9 yes và 5 no. Cần duyệt nếu sunny là yes thì đi đâu, no thì đi đâu.
                    Do đó, đệ quy lại với input là dataFrame đã được cắt theo value = sunny đang xét.
        '''

        if len(counts) == 1:
            tree[node][value] = clValue[0]                                                    
        else:
            tree[node][value] = buildTree(subtable)
                   
    return tree

def predict(inst: dict, tree: dict) -> str:
    for nodes in tree.keys():
        value = inst[nodes]
        tree = tree[nodes][value]
        prediction = 0
            
        if type(tree) is dict:
            prediction = predict(inst, tree)
        else:
            prediction = tree
            break                            
        
    return prediction

def main():
    inputDir = './input/'
    nameInput = ['WeatherClassic.csv', 'Bai2.csv', 'BuyComputer.csv']
    # dataset = import_data(inputDir, nameInput[0])

    # tree = buildTree(dataset)
    # pprint.pprint(tree)

    # inst = {'outlook':'sunny','temperature':'hot','humidity':'high','wind':'false'}
    # inst = {'Voc dang': 'Nho', 'Quoc tich': 'Duc', 'Gia canh': 'Co gia dinh'}
    # inst = pd.Series(inst)
    # prediction = predict(inst, tree)
    # print(prediction)
	
if __name__=="__main__": 
	main()
	