'''

Autor: Ariel Barros

'''
class Node(object):

    def __init__(self, entropy, name, attribute, leaf, label):

        '''
        Cria um no para ser usado em uma arvore de decisão
        '''
        self.entropy = entropy
        self.name = name
        self.attribute = "X{}".format(attribute + 1)
        self.leaf = leaf
        self.label = label

    def getClass(self):
        '''
        Retorna a Classe mais frequente do nó
        '''
        return self.label

    def isLeaf(self):
        '''
        Retorna se o no eh folha ou nao
        '''
        return self.leaf

    def getName(self):
        '''
        Retorna o nome do no
        '''
        return self.name

    def getAttribute(self):
        '''
        Retorna o atributo de maior ganho do no
        '''
        return self.attribute

    def getEntropy(self):
        '''
        Retorna entropia do no
        '''
        return self.entropy