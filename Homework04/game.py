import os
import random
import time

def hasWin(data):

	"""
	Checa se houve uma vitoria
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
	
	# checa se houve uma soma de modulo 3 que representa vitoria do X e do O
	if '3' in check:
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

def makeArff(tictactoe):
	
	"""
	Funcao usada para construir o arquivo ARFF de teste
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
	
	text = ','.join(str(pos) for pos in tictactoe) + ',0 \n'
	content = header + text
	f = open(arffFilename, 'w')
	f.write(content)
	f.close()
	
def predictClass(tictactoe):

	"""
	Funcao que coleta a resposta predita pelo classificador
	"""
	
	makeArff(tictactoe)
	#os.system('java -classpath weka.jar weka.classifiers.functions.SMO -l cl_smo.bin -T ' + arffFilename + ' -p 0 > saida.txt')
	os.system('java -classpath weka.jar weka.classifiers.trees.RandomForest -l clRandomForest.bin -T ' + arffFilename + ' -p 0 > saida.txt')
	f = open('saida.txt')
	linha = f.readlines()[5]
	return int(linha[30])

if __name__ == "__main__":

	arffFilename = 'test.arff'
	tictactoe = [0 for _ in range(9)] # Cria lista que seja responsavel por armazenar o tabuleiro
	firstMove = random.randint(0, 8) # posicao para inicio do jogo 
	move = 1 # variavel usada para registrar 1 e -1 no tabuleiro
	tictactoe[firstMove] = move

	for _ in range(4): # numero maximo de tentativas com duas jogadas por iteracao
		move = -move # na proxima jogada ser o movimento do oponente
		drawBoard(tictactoe)
		actualMove = int(input("Escolha uma posição:"))
		aux = list(tictactoe)
		aux[actualMove] = move

		if hasWin(aux): # Verifica se existe vencedor
			drawBoard(aux)
			print("Fim da partida")
			break

		tictactoe[actualMove] = aux[actualMove] # somente adiciona o movimento ao tabuleiro original em caso de nao vitoria


		move = -move # na proxima jogada ser o movimento do oponente
		actualMove = predictClass(tictactoe) # movimento do jogador X
		aux = list(tictactoe)
		aux[actualMove] = move

		if hasWin(aux): # Verifica se existe vencedor
			drawBoard(aux)
			print("Fim da partida")
			break

		tictactoe[actualMove] = aux[actualMove] # somente adiciona o movimento ao tabuleiro original em caso de nao vitoria