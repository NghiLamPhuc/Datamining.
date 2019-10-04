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
		self.initLabelIndexs()
		self.root = None
		self.entropy = self.getEntropy([x for x in range(len(self.labels))])


	def initLabelIndexs(self):
		self.labelIndexs = list()
		self.labelIndexsCount = list()
		for l in self.labels:
			if l not in self.labelIndexs:
				self.labelIndexs.append(l)
				self.labelIndexsCount.append(0)
			self.labelIndexsCount[self.labelIndexs.index(l)] += 1


	def getLabelIndexId(self, sampleId: int) -> str:
		return self.labelIndexs.index(self.labels[sampleId])


	def getAttributeValues(self, sampleIds: list, attributeId: int) -> list:
		vals = list()
		for sid in sampleIds:
			val = self.sample[sid][attributeId]
			if val not in vals:
				vals.append(val)
		return vals


	def getEntropy(self, sampleIds: list) -> float:
		entropy = 0.0
		labelCount = list()
		[labelCount.append(0) for _ in range(len(self.labelIndexs))]
		
		for sid in sampleIds:
			labelCount[self.getLabelIndexId(sid)] += 1
		for lv in labelCount:
			if lv != 0:
				entropy += -lv/len(sampleIds) * math.log(lv/len(sampleIds), 2)
			else:
				entropy += 0
		return entropy


	def getDominantLabel(self, sampleIds: list) -> str:
		labelIndexsCount = list()
		[labelIndexsCount.append(0) for _ in range(len(self.labelIndexs))]

		for sid in sampleIds:
			labelIndexsCount[self.labelIndexs.index(self.labels[sid])] += 1
		return self.labelIndexs[labelIndexsCount.index(max(labelIndexsCount))]


	def getInformationGain(self, sampleIds: list, attributeId: int) -> float:#, dict):
		gain = self.getEntropy(sampleIds)
		attributeVals = list()
		attributeValsCount = list()
		attributeValsIds = list() # Luu danh sach cac row ung voi attributeVals
		for sid in sampleIds:
			val = self.sample[sid][attributeId]
			if val not in attributeVals:
				attributeVals.append(val)
				attributeValsCount.append(0)
				attributeValsIds.append([])
			vid = attributeVals.index(val)
			attributeValsCount[vid] += 1
			attributeValsIds[vid].append(sid)
		for (vc, vids) in zip(attributeValsCount, attributeValsIds):
			gain -= vc/len(sampleIds) * self.getEntropy(vids)
		return gain


	def getAttributeMaxInformationGain(self, sampleIds: list, attributeIds: list) -> (str, int, float, dict):
		logAttrEntr = dict()
		attributesEntropy = list()
		[attributesEntropy.append(0) for _ in range(len(attributeIds))]
		
		for attId in range(len(attributeIds)):
			attributesEntropy[attId] = self.getInformationGain(sampleIds, attributeIds[attId])
			logAttrEntr[self.attributes[attId]] = attributesEntropy[attId]
			
		maxId = attributeIds[attributesEntropy.index(max(attributesEntropy))]
		
		return (self.attributes[maxId], maxId, max(attributesEntropy), logAttrEntr)


	def isSingleLabeled(self, sampleIds: list) -> bool:
		if not self.labels:
    			return False
		label = self.labels[sampleIds[0]]
		for sid in sampleIds:
			if self.labels[sid] != label:
				return False
		return True


	def getLabel(self, sampleId: int) -> str:
		return self.labels[sampleId]


	def id3(self):
		sampleIds = [x for x in range(len(self.sample))]
		attributeIds = [x for x in range(len(self.attributes))]
		self.root = self.id3Generator(sampleIds, attributeIds, self.root)


	def id3Generator(self, sampleIds: list, attributeIds: list, root: Node) -> Node:
		root = Node()
		if self.isSingleLabeled(sampleIds):
			root.name = self.labels[sampleIds[0]]
			return root

		if len(attributeIds) == 0:
			root.name = self.getDominantLabel(sampleIds)
			return root
		(bestAttrName, bestAttrId, maxInfoGainValue, infoGainDict) = self.getAttributeMaxInformationGain(sampleIds, attributeIds)
		
		print(infoGainDict)
		
		root.name = bestAttrName
		root.value = maxInfoGainValue
		root.childs = list()
		for value in self.getAttributeValues(sampleIds, bestAttrId):
			child = Node()
			child.name = value
			
			root.childs.append(child)
			# root
			childSampleIds = list()
			for sid in sampleIds:
				if self.sample[sid][bestAttrId] == value:
					childSampleIds.append(sid)
			if len(childSampleIds) == 0:
				child.next = self.getDominantLabel(sampleIds)
			else:
				if len(attributeIds) > 0 and bestAttrId in attributeIds:
					toRemove = attributeIds.index(bestAttrId)
					attributeIds.pop(toRemove)
				child.next = self.id3Generator(
					childSampleIds, attributeIds, child.next)
		
		return root

	def printRule(self):
		if self.root:
			while(self.root.next):
				print(self.root.name)
				self.root = self.root.next

	def printTree(self):
		listAns = list()
		ans = ''
		if self.root:
			roots = deque()
			roots.append(self.root)
			while len(roots) > 0:
				root = roots.popleft()
				if root.value != None:
					print('({}): {}'.format(root.name, round(root.value, 5)))
					ans += root.name + ','
				else:
					print('{}'.format(root.name))
					ans += ',' + root.name
					listAns.append(ans)
					ans = ''
				if root.childs:
					for child in root.childs:
						print('({})'.format(child.name))
						roots.append(child.next)
						ans += child.name + ','
				elif root.next:
					print(root.next)
					ans += root.name + ','
		return listAns


def test():
	f = open('./input/WeatherClassic.csv')
	# f = open('./input/BuyComputer.csv')
	# f = open('./input/Bai2.csv')
	attributes = f.readline().split(',')
	attributes = attributes[1:len(attributes)-1]
	# attributes = attributes[:len(attributes) - 1]
	print(attributes)
	sample = f.readlines()
	f.close()
	for i in range(len(sample)):
		sample[i] = re.sub('\d+,', '', sample[i])
		sample[i] = sample[i].strip().split(',')
	labels = list()
	for s in sample:
		labels.append(s.pop())
	# print(*sample, sep = '\n')
	# print(labels)
	decisionTree = DecisionTree(sample, attributes, labels)
	print("entropy(S) = {}".format(round(decisionTree.entropy, 3)))

	decisionTree.id3()
	print(decisionTree.printTree())
	decisionTree.printRule()


if __name__ == '__main__':
	test()
