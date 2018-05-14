'''

Autor: Ariel Barros

Para executar esse script:
$ python3 main.py

'''

import os
import sys
import random

def randomPopulation(numberIndividuals):

	"""
	Gera uma populacao de maneira aleatoria
	"""

	population = []
	for _ in range(numberIndividuals):
		MinNo 	       = random.randint(2,50) 			# MinNo -N
		Optimizations  = random.randint(2,50) 			# Optimizations -O
		checkErrorRate = bool(random.getrandbits(1)) 	# checkErrorRate -E quando for False
		usePruning     = bool(random.getrandbits(1)) 	# usePruning -P quando for False

		population.append([MinNo, Optimizations, checkErrorRate, usePruning])

	return population

def objectiveFunction(individual):

	"""
	Calcula a precisao de um determinado individuo
	"""

	opts = '-N {} -O {} '.format(str(float(individual[0])), str(individual[1]))

	if individual[2] == False:
		opts += '-E '	# Adiciona a flag de checkErrorRate no comando

	if individual[3] == False:
		opts += '-P '	# Adiciona a flag de usePruning no comando

	precision = []
	for i in range(5):
		command = 'java -classpath {} weka.classifiers.rules.JRip {}-t {} -S {} -p 0 {} > saida.txt'.format(pathWeka, opts, ConjuntoDeDados, i, stderrPlataform)
		print(command)
		os.system(command)

		f = open('saida.txt')
		data = str(f.readlines())
		precision.append(1 - data.count("+") / float(data.count(":") / 2) ) # Adiciona a precisao na lista de precisoes
		f.close()
	
	return sum(precision) / float(len(precision)) # retorna precisao media

def selection(population, n):

	"""
	Seleciona n individuos de um populacao baseado no algoritmo de roleta viciada 
	"""

	selectedIndividuals = []
	totalLenght = sum((individual[1] for individual in population)) # soma das precisoes

	for _ in range(n):
		choice = random.uniform(0, totalLenght) # escolha aleatoria
		for idx, (individual, weight) in enumerate(population):
			if choice < weight:
				selectedIndividuals.append((individual, weight)) # seleciona o elemento corrente
				totalLenght -= weight # Diminue o comprimento total para a proxima selecao
				del population[idx] # deleta o elemento selecionado para evitar ser selecionado outra vez
				break
			else:
				choice = choice - weight
		
	return selectedIndividuals

def crossover(ind1, ind2):

	"""
	Realiza o crossover entre dois dados individuos
	"""

	children = []
	for threshold in range(1, len(ind1)):
		children.append(ind1[:threshold] + ind2[threshold:])
		children.append(ind2[:threshold] + ind1[threshold:])

	return children

def mutation(individual):

	"""
	Promove uma mutacao aleatoria em uma caracteristica qualquer de um dado individuo
	"""

	feature = random.randint(0, 3)
	if feature <= 1:
		# causa uma perturbacao aleatoria com no maximo 5 unidades de diferenca
		individual[feature] = min(50, max(2, random.randint(individual[feature] - 5, individual[feature] + 5))) 
	else:
		# inverte de True para False ou vice versa
		individual[feature] = not individual[feature]
	
	return individual
	
def bestIndividuals(population, n):

	"""
	Seleciona os N melhores individuos de uma dada populacao
	"""

	population = sorted(population, key=lambda ind: ind[1], reverse=True) # ordena baseado na precisao
	return population[:n]

if __name__ == "__main__":

	# Parametros Globais
	ConjuntoDeDados = 'diabetes.arff'		# Conjunto de dados
	pathWeka        = 'weka.jar'			# Caminho para o JAR do Weka
	populationSize  = 20					# Tamanho da populacao
	numGenerations  = 5						# Numero de geracoes
	numSelected     = 8						# Numero PAR de individuos selecionados
	mutationRate    = 0.01					# Taxa de mutacao

	# stderr weka warnings
	if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
		stderrPlataform = '2> /dev/null'
	elif sys.platform.startswith("win") or sys.platform.startswith("dos") or sys.platform.startswith("ms"):
		stderrPlataform = '2> nul'

	print("Primeira população...")
	population = randomPopulation(populationSize)

	# Avalia a precisao de cada individuo da populacao
	weightedPopulation = []
	for individual in population:
		weightedPopulation.append( (individual, objectiveFunction(individual)) ) # Adiciona um tupla que contem o individuo e sua respectiva precisao

	for g in range(numGenerations):
		print("Geração: {}".format(str(g + 1)))

		# SELECTION
		selectedIndividuals = selection(weightedPopulation, numSelected)

		weightedPopulation = [] # Esvazia a lista de individuos para a proxima geracao
		weightedChildren = [] # cria uma lista vazia para armazenar os novos individuos gerados

		for i in range(0, len(selectedIndividuals), 2):
			# CROSSOVER
			children = crossover(selectedIndividuals[i][0], selectedIndividuals[i+1][0]) # Retorna 6 individuos novos

			for child in children:
				# MUTATION
				if random.random() < mutationRate:
					child = mutation(child)

				weightedChildren.append( (child, objectiveFunction(child)) ) # Adiciona o novo individuo na lista

		# ELITISM
		weightedPopulation.extend( bestIndividuals(weightedChildren, populationSize - 1) ) # adiciona na populacao os melhores individuos gerados
		weightedPopulation.extend( bestIndividuals(selectedIndividuals, 1) ) # preserva o melhor individuo selecionado da geracao anterior
		
		print("População atual:")
		for ind, fit in weightedPopulation:
			print("indivíduo: {} Precisão: {}".format(ind, fit))

	print("Best individual: {}".format(bestIndividuals(weightedPopulation, 1)))