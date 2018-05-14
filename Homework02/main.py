'''

Autor: Ariel Barros

Para executar esse script:
$ python3 main.py

'''

from node import Node
import numpy as np
import math

def buildTree(data, idx):

	'''
	Constroe Arvore
	'''

	currentEntropy = entropy(data)
	bestGain = 0
	bestAttrib = None

	# Verifica qual melhor atributo
	for attrib in range(nAttributes):
		conjunto1, conjunto2 = dividir(data, attrib)
		if len(conjunto1) >= minNumObj and len(conjunto2) >= minNumObj:
			p = float(len(conjunto1)) / len(data)
			gain = currentEntropy - p * entropy(conjunto1) - (1 - p) * entropy(conjunto2)
			if gain > bestGain:
				bestGain = gain
				bestAttrib = attrib
				bestSets = (conjunto1, conjunto2)

	# Divide o dataset se ouver algum ganho, do contrário marca o no como folha
	if bestGain > 0:
		tree[idx] = Node(currentEntropy, 'no{}'.format(idx), bestAttrib, False, None)
		buildTree(bestSets[0], 2*idx) 
		buildTree(bestSets[1], 2*idx + 1)
	else:
		tree[idx] = Node(currentEntropy, 'no{}'.format(idx), -1, True, mostCommon(data))


def entropy(data):

	'''
	Calcula a entropia de uma dataset
	'''

	count = 0
	for d in data:
		if d[-1] == 0:
			count += 1

	p = float(count) / len(data)
	if p == float(1) or p == float(0):
		return float(0)

	entropy = p * math.log2(p) + (1 - p) * math.log2(1 - p)
	return -entropy

def dividir(data, attrib):

	'''
	Divide o dataset em relacao a um dado atributo
	'''

	conjunto1 = []
	conjunto2 = []

	for d in data:
		if d[attrib] == 0:
			conjunto1.append(d)
		else:
			conjunto2.append(d)

	return (conjunto1, conjunto2)

def mostCommon(data):

	'''
	Retorna a classe mais comum de um dataset 
	'''

	count0, count1 = 0, 0
	for d in data:
		if d[-1] == 0:
			count0 += 1
		else:
			count1 += 1
	if count0 >= count1:
		return str(0)
	else:
		return str(1)

def exportTree():

	'''
	Exporta a arvore em Linguagem DOT
	'''

	f = open('tree.txt', 'w')
	f.write('digraph G {\n')

	for node in tree:
		if node != None:
			if node.isLeaf():
				f.write('\t{} [label = "{}", shape=circle]\n'.format(node.getName(), node.getClass()))
			else:
				f.write('\t{} [label = "{}", shape=rectangle]\n'.format(node.getName(), node.getAttribute()))

	f.write('\n')

	for idx, node in enumerate(tree):
		if node != None:
			if not node.isLeaf():
				f.write('\t{} -> {} [label = "=0"]\n'.format(node.getName(), tree[2*idx].getName()))
				f.write('\t{} -> {} [label = "=1"]\n'.format(node.getName(), tree[2*idx + 1].getName()))

	f.write('}\n')
	f.close()
	print("File tree.txt was generated in DOT language")

if __name__ == "__main__":

	minNumObj = 1

	f = open('dados.txt')
	nSamples  = int(f.readline())
	nAttributes = int(f.readline())
	dataset = f.readlines()
	dataset = np.genfromtxt(dataset, delimiter=',', dtype=int)
	f.close()

	# Cria array global onde serao armazenados os nos da arvore
	tree = [None] * 2**(nAttributes + 1)

	buildTree(dataset, 1)
	exportTree()