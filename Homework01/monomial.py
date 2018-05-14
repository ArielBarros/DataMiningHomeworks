'''

Autor: Ariel Barros

'''

class Monomial(object):

    def __init__(self, attributes):

        '''
        Cria monômio a partir de um vetor de atributos dado.
        a variável valid refere-se a validade do monômio na hipótese
        '''

        self.attributes = attributes
        self.valid = True
    
    def checkMonomial(self, x):

        '''
        Computa a conjunção do monômio levando em conta os valores 
        atributos de um vetor dada
        '''

        result = 1
        for attribute in self.attributes:
            if attribute < 0:
                attribute = attribute + 1 
                if x[-attribute] == 0:
                    result *= 1
                else:
                    result *= 0
            else:
                attribute = attribute - 1 
                if x[attribute] == 0:
                    result *= 0
                else:
                    result *= 1
        return result

    def removeMonomial(self, d):

        '''
        Remove o monomio da hipótese setando valid como False se o 
        resultado do monomio for positivo para um vetor d
        '''

        if self.checkMonomial(d):
            self.valid = False

    def stringMonomial(self):

        '''
        Retorna o monomio em Human-readable
        '''

        text = ""
        for attribute in self.attributes:
            if attribute < 0:
                text += "~X{}".format(-attribute) 
            else:
                text += "X{}".format(attribute)
        return text

    def isValid(self):

        '''
        Retorna validade do monomio na hipótese
        '''

        return self.valid
