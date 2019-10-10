import re
import math
from collections import deque


class Node():
	def __init__(self):
		self.name = None
		self.next = None
		self.childs = None
		self.value = None

class DecisionTree():
	def __init__(self, sample, attributes, labels):
		self.sample = sample
		self.attributes = attributes
		self.labels = labels
		self.labelIndexs = None
		self.labelIndexsCount = None
		self.init_label_indexs()
		self.root = None
		self.entropy = self.get_entropy([x for x in range(len(self.labels))])


	def init_label_indexs(self):
		self.labelIndexs = list()
		self.labelIndexsCount = list()
		for l in self.labels:
			if l not in self.labelIndexs:
				self.labelIndexs.append(l)
				self.labelIndexsCount.append(0)
			self.labelIndexsCount[self.labelIndexs.index(l)] += 1


	def get_label_indexId(self, sampleId: int) -> str:
		return self.labelIndexs.index(self.labels[sampleId])


	def get_attribute_values(self, sampleIds: list, attributeId: int) -> list:
		vals = list()
		for sid in sampleIds:
			val = self.sample[sid][attributeId]
			if val not in vals:
				vals.append(val)
		return vals


	def get_entropy(self, sampleIds: list) -> float:
		entropy = 0.0
		labelCount = list()
		[labelCount.append(0) for _ in range(len(self.labelIndexs))]
		
		for sid in sampleIds:
			labelCount[self.get_label_indexId(sid)] += 1
		for lv in labelCount:
			if lv != 0:
				entropy += -lv/len(sampleIds) * math.log(lv/len(sampleIds), 2)
			else:
				entropy += 0
		return entropy


	def get_dominant_label(self, sampleIds: list) -> str:
		labelIndexsCount = list()
		[labelIndexsCount.append(0) for _ in range(len(self.labelIndexs))]

		for sid in sampleIds:
			labelIndexsCount[self.labelIndexs.index(self.labels[sid])] += 1
		return self.labelIndexs[labelIndexsCount.index(max(labelIndexsCount))]

	# attributeNames List tên giá trị của thuộc tính đang xét.
    # vd: outlook có 3 giá trị sunny, rainy, overcast
    # attributeNamesCount List đếm lần xuất hiện từng giá trị của thuộc tính trong inputdata
    # vd sunny có 5, overcast có 4, rainy có 5.
    # attributeNameIds List() lớn chứa các list nhỏ: các index của dòng có giá trị của thuộc tính đang xét.
    # vd: sunny ở dòng 1,2,8,9,11 rainy ở dòng 4,5,6,10,14 overcast ở dòng 3,7,12,13
	def get_informationGain(self, sampleIds: list, attributeId: int) -> float:#, dict):
		gain = self.get_entropy(sampleIds)
		attributeNames = list()
		attributeNamesCount = list()
		attributeNamesIds = list() # Luu danh sach cac row ung voi attributeNames
		for sid in sampleIds:
			val = self.sample[sid][attributeId]
			if val not in attributeNames:
				attributeNames.append(val)
				attributeNamesCount.append(0)
				attributeNamesIds.append([])
			vid = attributeNames.index(val)
			attributeNamesCount[vid] += 1
			attributeNamesIds[vid].append(sid)
		for (vc, vids) in zip(attributeNamesCount, attributeNamesIds):
			gain -= vc/len(sampleIds) * self.get_entropy(vids)
		return gain


	def get_attribute_max_informationGain(self, sampleIds: list, attributeIds: list) -> (str, int, float, dict):
		logAttrEntr = dict()
		attributesEntropy = list()
		[attributesEntropy.append(0) for _ in range(len(attributeIds))]
		
		for attId in range(len(attributeIds)):
			attributesEntropy[attId] = self.get_informationGain(sampleIds, attributeIds[attId])
			logAttrEntr[self.attributes[attributeIds[attId]]] = attributesEntropy[attId]
			
		maxId = attributeIds[attributesEntropy.index(max(attributesEntropy))]
		
		return (self.attributes[maxId], maxId, max(attributesEntropy), logAttrEntr)


	def is_single_labeled(self, sampleIds: list) -> bool:
		if not self.labels:
    			return False
		label = self.labels[sampleIds[0]]
		for sid in sampleIds:
			if self.labels[sid] != label:
				return False
		return True


	def get_label(self, sampleId: int) -> str:
		return self.labels[sampleId]


	def id3(self):
		sampleIds = [x for x in range(len(self.sample))]
		attributeIds = [x for x in range(len(self.attributes))]
		self.root = self.id3Generator(sampleIds, attributeIds, self.root)


	def id3Generator(self, sampleIds: list, attributeIds: list, root: Node) -> Node:
		root = Node()
		if self.is_single_labeled(sampleIds):
			root.name = self.labels[sampleIds[0]]
			return root

		if len(attributeIds) == 0:
			root.name = self.get_dominant_label(sampleIds)
			return root
		(bestAttrName, bestAttrId, maxInfoGainValue, infoGainDict) = self.get_attribute_max_informationGain(sampleIds, attributeIds)
		
		print(infoGainDict)
		
		root.name = bestAttrName
		root.value = maxInfoGainValue
		root.childs = list()
		for value in self.get_attribute_values(sampleIds, bestAttrId):
			child = Node()
			child.name = value
			
			root.childs.append(child)
			# root
			childSampleIds = list()
			for sid in sampleIds:
				if self.sample[sid][bestAttrId] == value:
					childSampleIds.append(sid)
			if len(childSampleIds) == 0:
				child.next = self.get_dominant_label(sampleIds)
			else:
				if len(attributeIds) > 0 and bestAttrId in attributeIds:
					toRemove = attributeIds.index(bestAttrId)
					attributeIds.pop(toRemove)
				child.next = self.id3Generator(childSampleIds, attributeIds, child.next)
		return root

	def print_tree(self):
		if self.root:
			roots = deque()
			roots.append(self.root)
			while len(roots) > 0:
				root = roots.popleft()
				if root.value != None:
					print('({}): {}'.format(root.name, round(root.value, 5)))
				else:
					print('{}'.format(root.name))
				if root.childs:
					for child in root.childs:
						print('({})'.format(child.name))
						roots.append(child.next)
						
				elif root.next:
					print(root.next)
		
	def predict(self, inst: dict) -> str:
		node = self.root
		while node.next or node.childs:
			for (attribute, value) in inst.items():
				if node.name == attribute:
					for child in node.childs:
						if value == child.name:
							node = child.next
		
		return node.name
		

def test():
	f = open('./input/WeatherClassic.csv')
	# f = open('./input/Bai2.csv')
	attributes = f.readline().split(',')
	attributes = attributes[1:len(attributes)-1]
	print(attributes)
	sample = f.readlines()
	f.close()
	for i in range(len(sample)):
		sample[i] = re.sub('\d+,', '', sample[i])
		sample[i] = sample[i].strip().split(',')
	labels = list()
	for s in sample:
		labels.append(s.pop())
	
	decisionTree = DecisionTree(sample, attributes, labels)
	print("entropy(S) = {}".format(decisionTree.entropy))

	decisionTree.id3()
	# decisionTree.print_tree()
	inst = {'outlook':'overcast','temperature':'hot','humidity':'high','wind':'weak'}
	print(decisionTree.predict(inst))
	

if __name__ == '__main__':
	test()
	
	