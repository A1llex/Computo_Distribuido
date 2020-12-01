import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = None
        #iniciamos todos los nodos con distancia -10 que representa infinito
        self.distancia = -10;

    def bfs(self,env):
        if self.id_nodo == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            #distancia a la raiz =0 y su propio padre
            self.distancia = 0
            self.padre = self.id_nodo
            #envia un mensaje con la tupla del id que sera su padre su distancia a la raiz
            self.canal_salida.envia((self.id_nodo,self.distancia),self.vecinos)
            yield env.timeout(1)
        else:
            while True:
                # Esperamos a que nos llegue el mensajee
                mensaje = yield self.canal_entrada.get()
                yield env.timeout(1)
                if not mensaje:
                    break
                else:
                    #Solo si la distancia es mayor a la actual +1
                    if(self.distancia +1 < mensaje[1]):
                        self.padre = mensaje[0]
                        self.distancia = mensaje[1]+1
                        self.canal_salida.envia((self.id_nodo,self.distancia),self.vecinos)
                        yield env.timeout(1)


