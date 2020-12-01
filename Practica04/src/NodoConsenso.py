import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nones
        self.V[id_nodo] = id_nodo
        self.New = [id_nodo]
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.

    def consenso(self, env, fallas):
        '''El algoritmo de consenso.'''
        #determinamos si este nodo fallara
        if(self.id_nodo +1> fallas):
            ronda = 1
            # numero de rondas
            while ronda < fallas+1:
                #a
                if  self.New :
                    yield env.timeout(1)
                    self.canal_salida.envia((self.New,self.id_nodo), self.vecinos)
                #letcev
                yield env.timeout(1)
                mensaje = yield self.canal_entrada.get()
                #si hay mensaje haremos
                if mensaje :
                    a = mensaje[0]
                    b = mensaje[1]
                    #si en la posicion del mensaje hay un none la llenamos
                    if self.V[b] == None:
                        self.V[b] = a[0]
                        self.New = union(self.New,a)
                else:
                    #si no hay mensaje vaciamos el New
                    self.New = []
                #end round
                ronda += 1
            for v in self.V :
                if v != None:
                    self.lider = v
                    return v
        else:
            self.fallare = True

#Lambda para ayudarnos a trabajar con arreglos o listas            
union = lambda l1,l2: [x for x in l1 if x not in l2]+l2