import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = self.id_nodo
        self.hijos = list()

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        if self.id_nodo == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            #Se vuelve su propio padre
            self.padre = self.id_nodo
            self.hijos = [self.vecinos[0]]
            #envia un mensaje con la tupla del id que sera su padre su distancia a la raiz
            yield env.timeout(1)
            self.canal_salida.envia(("Go",self.id_nodo,{self.id_nodo}),self.hijos)
            #print("nodo 0 ok")
        while True:
            # Esperamos a que nos llegue el mensajee
            (mensaje,j,visited) = yield self.canal_entrada.get()
            if (mensaje == "Go"):    
                self.padre = j
                if(contenido(self.vecinos, visited)):
                    yield env.timeout(1)
                    self.canal_salida.envia( ("Back",self.id_nodo, union(visited,[self.id_nodo]) ), [self.padre])
                    self.hijos = []
                else:
                    self.hijos =  [(diferencia(self.vecinos,visited))[0]]
                    yield env.timeout(1)
                    self.canal_salida.envia( ("Go", self.id_nodo, union(visited,[self.id_nodo]) ) ,self.hijos)
            elif (mensaje == "Back"):
                if(contenido(self.vecinos, visited)):
                    if self.padre == self.id_nodo:
                        #Termino
                        return
                    else:
                        yield env.timeout(1)
                        self.canal_salida.envia( ("Back",self.id_nodo, visited), [self.padre])
                else:
                    k = [(diferencia(self.vecinos,visited))[0]]
                    yield env.timeout(1)
                    self.canal_salida.envia( ("Go", self.id_nodo, visited), k)
                    self.hijos = union(self.hijos,k)


diferencia = lambda l1,l2: [x for x in l1 if x not in l2]
union = lambda l1,l2: [x for x in l1 if x not in l2]+l2
def  contenido(a,b):
    for x in a:
        if (x not in b):
            return False
    return True