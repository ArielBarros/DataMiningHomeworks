'''

Autor: Ariel Barros

Para executar esse script:
$ python3 main.py <path/file>

'''

from monomial import Monomial
import numpy as np
import sys

def createMonomials():

	'''
	Função que cria todos os monômios até grau 2
	Os monômios são criados levando em conta o número do atributo 
	e o sinal de menos para indicar barrado
	Ex:
	Para o monômio ~X2 tem-se o vetor [-2]
	Para o monômio ~X1X3 tem-se o vetor [-1, 3]
	'''

	for i in range(1, nAttributes + 1):
		hypothesis.append(Monomial([i]))
		hypothesis.append(Monomial([-i]))

	for i in range(1, nAttributes):
		for j in range(i + 1, nAttributes + 1):
			hypothesis.append(Monomial([i, j]))
			hypothesis.append(Monomial([-i, j]))
			hypothesis.append(Monomial([i, -j]))
			hypothesis.append(Monomial([-i, -j]))

def computeHypothesis(d):

	'''
	Computa a hipotese atual para um vetor d
	'''

	result = 0
	for m in hypothesis:
		if m.isValid():
			result += m.checkMonomial(d)
	return 1 if result else 0

def remove(d):

	'''
	Remove monomio que resulta positivo para a vetor d
	'''

	for m in hypothesis:
		m.removeMonomial(d)

def printHypothesis():

	'''
	Imprime Hipótese atual em Human-readable
	'''

	text = "H = "
	aux = False
	for m in hypothesis:
		if m.isValid():
			if aux:
				text += " v " 
			aux = True
			text += m.stringMonomial()
	return text

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("formato: python3 {} <path/file>".format(sys.argv[0]))
		exit(1);

	f = open(sys.argv[1])
	nSamples  = int(f.readline())
	nAttributes = int(f.readline())
	data = f.readlines()
	data = np.genfromtxt(data, delimiter=',', dtype=int)
	hypothesis = []

	createMonomials()

	for d in data:
		if d[-1] == 0 and computeHypothesis(d[:nAttributes]) == 1:

			if False: # Verbose Output
				print("Hipótese atual:")
				print(printHypothesis(), end="\n\n")

			remove(d[:nAttributes])

	print(printHypothesis())