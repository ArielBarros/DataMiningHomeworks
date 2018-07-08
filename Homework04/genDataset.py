'''

Autor: Ariel Barros
Matrícula: 374918
Curso: Engenharia de Computação

Para executar esse script:
$ python3 genDataset.py

'''

import os
import random
import time

def hasWin(data):

	"""
	Checa se houve uma vitoria de X
	"""
	
	walk = []

	walk.append(str(data[0] + data[1] + data[2]))
	walk.append(str(data[3] + data[4] + data[5]))
	walk.append(str(data[6] + data[7] + data[8]))

	walk.append(str(data[0] + data[3] + data[6]))
	walk.append(str(data[1] + data[4] + data[7]))
	walk.append(str(data[2] + data[5] + data[8]))

	walk.append(str(data[0] + data[4] + data[8]))
	walk.append(str(data[2] + data[4] + data[6]))

	check = ''.join(walk)

	# checa se houve uma soma somente igual a 3 que representa vitoria do X
	if '3' in check and '-3' not in check:
		return True

	return False	

def drawBoard(board):

	"""
	Imprime um tabuleiro com os valores correntes do vetor que representa o jogo da velha
	"""
	
	# eh usado para mapear os valores armazenados nos caracteres X e O printaveis
	translation = {0: " ", 1: "X", -1: "O"} 

	print('   |   |')
	print(' ' + translation[board[0]] + ' | ' + translation[board[1]] + ' | ' + translation[board[2]])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + translation[board[3]] + ' | ' + translation[board[4]] + ' | ' + translation[board[5]])
	print('   |   |')
	print('-----------')
	print('   |   |')
	print(' ' + translation[board[6]] + ' | ' + translation[board[7]] + ' | ' + translation[board[8]])
	print('   |   |')

def makeArff(text):

	"""
	Funcao usada para construir o arquivo ARFF
	"""
	
	header  = "@relation tic-tac-toe \n"
	header += "@attribute 'pos0' {-1,0,1} \n"
	header += "@attribute 'pos1' {-1,0,1} \n"
	header += "@attribute 'pos2' {-1,0,1} \n"
	header += "@attribute 'pos3' {-1,0,1} \n"
	header += "@attribute 'pos4' {-1,0,1} \n"
	header += "@attribute 'pos5' {-1,0,1} \n"
	header += "@attribute 'pos6' {-1,0,1} \n"
	header += "@attribute 'pos7' {-1,0,1} \n"
	header += "@attribute 'pos8' {-1,0,1} \n"
	header += "@attribute 'class' { 0, 1, 2 ,3, 4, 5, 6, 7, 8} \n"
	header += "@data \n"

	content = header + text # Text representa todas as entradas de dados juntas
	f = open(arffFilename, 'w')
	f.write(content)
	f.close()

if __name__ == "__main__":

	# Parametros Globais
	arffFilename = 'tic-tac-toe.arff'
	numEntries = 700
	trainingSet = []

	while len(trainingSet) < numEntries: # Executa ate que o numero estipulado de entradas seja atingido
		tictactoe = [0 for _ in range(9)] # Cria lista que seja responsavel por armazenar o tabuleiro

		move = 1 # variavel usada para registrar 1 e -1 no tabuleiro
		passing = True # variavel de controle usada para permitir execucao enquanto nao existe vencedor
		for j in range(9):
			if passing:
				blankPosition = random.randint(0, 8-j) # posicao branco sorteada
				countBlankPositions = 0
				for idx, position in enumerate(tictactoe):
					if position == 0 and countBlankPositions == blankPosition: # verifica se eh a posicao a ser preenchida
						aux = list(tictactoe) # faz uma copia da lista do tabuleiro para verificar se existe vencedor
						aux[idx] = int(move) # o movimento na lista de copia eh feito
						if False: # verbose usado para um output interativo da confeccao do tabuleiro corrente 
							time.sleep(1)
							os.system('clear')
							print(blankPosition + 1)
							drawBoard(tictactoe)
						
						if hasWin(aux): # Verifica se existe vencedor
							pair = (tictactoe, idx) # registrar um par que eh o tabuleiro e o index de vitoria imediata
							trainingSet.append(pair) # adiciona a lista do conjunto de trainamento
							passing = False # desabilita o preenchimento restante
						else:
							tictactoe[idx] = int(move) # somente adiciona o movimento ao tabuleiro original

						move = -move # na proxima jogada ser o movimento do oponente
						break
					elif position == 0 and countBlankPositions != blankPosition: # ainda nao eh o espaco em branco atual
						countBlankPositions += 1

	text = ''
	for ttt, classe in trainingSet:
		if False: # verbose usado para imprimir o conjunto de treinamento pronto
			print("Classe: {}".format(classe))
			drawBoard(ttt)
			print('-'*100)

		text += ','.join(str(t) for t in ttt) + ',' + str(classe) + '\n' # concatena os dados de treinamento

	makeArff(text) # salva arquivo ARFF