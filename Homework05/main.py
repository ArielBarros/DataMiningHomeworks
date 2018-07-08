# -*- coding: utf-8 -*-
'''

Autor: Ariel Barros
Matrícula: 374918
Curso: Engenharia de Computação

Para executar esse script:
$ python3 main.py

'''

import numpy as np
import matplotlib.pyplot as plt
import random

def loadDataset(name):
    dataset = np.genfromtxt(name, delimiter=',')
    dataset = np.delete(dataset, dataset.shape[1] - 1, 1) # elimina a coluna contendo os rotulos das classes
    return dataset

def distance(x, y):
    return np.linalg.norm(x - y) # distancia euclidiana

def initCentroids(data, k):
    numInstances, _ = data.shape
    centroids = np.array([data[np.random.randint(numInstances)]]) # Seleciona o primeiro centroide aleatorio
    while len(centroids) < k:
        # Distancia de cada ponto ao centroide escolhido
        distances = np.array([min([ distance(x,c) for c in centroids]) for x in data])
        
        # Probabilidade para cada distancia
        probabilities = distances / distances.sum()
        cumulativeProbabilities = probabilities.cumsum()
        
        # Escolha aleatoria
        choice = random.random() #  retorna uma numero uniforme entre [0.0, 1.0)
        
        # Escolhe proximo centroide caso o numero aleatorio caia em seu intervalo com base em sua probabilidade
        idx = np.where(cumulativeProbabilities >= choice)[0][0] 
        centroids = np.vstack((centroids, data[idx])) # concatena o escolhido ao conjunto de centroides
    
    return centroids

def consensus(data, partitions, k):
    # Constroe a matriz de consenso
    m = len(partitions[0])
    S = np.zeros((m, m))
    for t in partitions:
        for i in range(m):
            for j in range(i+1, m):
                if t[i] == t[j]:
                    S[i][j] += 1
                    S[j][i] += 1
    
    # Processo de consenso
    l = m
    stringsClusters = [ str(i) for i in range(m)] # lista com strings representando os clusters
    while l > k:
        # Escolhe as duas entradas de maior similaridade
        idx1, idx2 = np.unravel_index(np.argmax(S, axis=None), S.shape)
        lower = min(idx1, idx2)
        higher = max(idx1, idx2)

        # Mesclar clusters
        stringsClusters[lower] += ', ' + stringsClusters[higher] 
        stringsClusters[higher] = ''
        
        # Mesclar linha e coluna
        S[lower,:] = np.minimum(S[idx1,:], S[idx2,:]) #linha
        S[:,lower] = np.minimum(S[:,idx1], S[:,idx2]) #coluna
        
        # Retira linha e coluna
        S[:,higher] = S[higher,:] = np.full(S[:,higher].shape, -1)
        S[lower, lower] = 0
        
        l = l - 1;

    # Calcula os centroides do consenso        
    listIdxs = [ x for x in stringsClusters if x]
    finalCentroids = np.array([np.mean(data[np.array(eval(group))], axis=0) for group in listIdxs])
    
    # Classifica cada entrada a um cluster especifico
    finalBelongsTo = np.zeros((data.shape[0], 1))
    for label, group in enumerate(listIdxs): 
        for idx in eval(group):
            finalBelongsTo[idx] = label
    
    return finalCentroids, finalBelongsTo
                
def kmeansPlusPlus(data, k, epsilon):
    centroids = initCentroids(data, k) # init centroids
    
    centroidsOld = np.zeros(centroids.shape)
    norm = np.array([distance(centroids[i], centroidsOld[i]) for i in range(len(centroids))]).sum()
    
    iteration = 0
    while norm > epsilon:
        # Classifica cada entrada a um cluster especifico
        belongsTo = np.array([np.argmin([distance(x, c) for c in centroids]) for x in data])
        
        # Recalcula os centroides
        centroidsOld = centroids
        centroids = np.array([np.mean(data[np.where(belongsTo == cluster)], axis=0) for cluster in range(len(centroids))])

        # Calcula as alteracoes dos centroides entre uma iteracao e sua anterior
        norm = np.array([distance(centroids[i], centroidsOld[i]) for i in range(len(centroids))]).sum()
        
        iteration += 1

    return centroids, belongsTo

def draw(dataset, centroids, belongsTo):
    # Plot clusters
    k = len(centroids)
    colors = 'bgcmyk'
    numColors = len(colors)
    for i in range(k):
        plt.plot(dataset[np.where(belongsTo == i),0], 
                 dataset[np.where(belongsTo == i),1], 
                 '{}*'.format(colors[i % numColors]))
        
    # Plot Centroids
    plt.plot(centroids[:,0], centroids[:,1], 'ro', markersize=12)
    
    plt.show()

def main():
    # Parametros Globais
    datasetName = 'iris.2D.arff' # Conjunto de dados
    numClusters = 3 # Numero de clusters
    numPartitions = 10 # Numero de particoes
    epsilon = 0.001
    
    # Importa dataset
    dataset = loadDataset(datasetName)
    
    # Calcula o numero especificado de particoes
    partitions = []
    for _ in range(numPartitions):
        centroids, belongsTo = kmeansPlusPlus(dataset, numClusters, epsilon)
        partitions.append(belongsTo) # Armazena cada particao gerada 
    
    finalCentroids, finalbelongsTo = consensus(dataset, partitions, numClusters)
        
    if False:
        draw(dataset, finalCentroids, finalbelongsTo)
        
    print('Centroids finais: ')
    print(finalCentroids)
    
if __name__ == "__main__":
    main()