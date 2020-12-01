#Ejercicio 1
import simpy
from Nodo import *
from Canales.CanalVecinos import *

class NodoVecinos():
    '''
    Clase nodo para el algoritmo que optiene los vecinos de sus vecinos.
    '''
    def __init__(self, id, neighbords, canal_entrada, canal_salida):
        '''Inicializa los atributos del nodo.'''
        self.id = id
        self.neighbords = neighbords
        self.identifiers = set()
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

    def conoceVecinos(self, env):
        '''
        Funcion principal para poder correr el algoritmo.
        '''
        #Eviamos la lista de nuestros vecinos a cada uno de los vecinos
        for self.id, self.neighbord in enumerate(self.neighbords):
            self.canal_salida.envia(self.neighbords)
            yield env.timeout(1)

        while True:
            # Esperamos a que nos llegue el mensaje
            mensaje = yield self.canal_entrada.get()
            yield env.timeout(1)
            if not mensaje:
                break
            else:
                #Unimos a nuestros vecinos los vecinos del mensaje recibido
                for item in mensaje:
                    self.identifiers.add(item)
            


if __name__ == "__main__":
    # Inicializamos ambiente y canal
    env = simpy.Environment()
    bc_pipe = Canal_vecinos(env)
    
    # Creamos la grafica
    grafica = []
    # Creamos los nodos
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]

    for i in range(0, len(adyacencias)):
        grafica.append(NodoVecinos(i, adyacencias[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

    for nodo in grafica:
        env.process(nodo.conoceVecinos(env))

    env.run(until=1500)

    identifiers_esperados = [[0, 3, 5], [1, 2, 4], [1, 2, 4], [0, 3, 5], [1, 2, 4], [0, 3, 5]]
    # Para cada nodo verificamos que su lista de identifiers sea la esperada.

    for nodo in grafica:
        print(nodo.identifiers)
    print("identifiers_esperados:")
    print(identifiers_esperados)