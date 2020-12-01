#Ejercicio 2
import simpy
from Nodo import *
from Canales.CanalGenerador import *

class NodoGenerador():
    '''
    Clase nodo para el algoritmo del arbol generador
    '''
    def __init__(self, id, neighbords, canal_entrada, canal_salida):
        '''Inicializa los atributos del nodo.'''
        self.id = id
        self.neighbords = neighbords
        self.expected_msg = 0
        self.parent = None
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.children = set()


    def genera_arbol(self, env):
        '''
        Función de principal para que los nodos corran el algoritmo.
        '''
        if self.id == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            yield env.timeout(1)
            #Definimos el padre como el mismo
            self.parent = self.id
            #Enviamos el mensaje Go() a todos los vecinos
            for i in self.neighbords:
                self.canal_salida.envia("Go", -1, i, self.id)

        while True:
            #Tomamos el mensaje
            mensaje = yield self.canal_entrada.get()
            
            #Condicion para salir del ciclo
            if not mensaje:
                break

            #Recibimos Go()
            if (mensaje[0] == "Go"):

                if self.parent == None:
                    #Definimos el padre como el nodo que envio el mensaje
                    self.parent = mensaje[2]
                    self.expected_msg = len(self.neighbords)-1

                    if self.expected_msg == 0:
                        #Enviamos el mensaje Back(i)
                        self.canal_salida.envia("Back", self.id, mensaje[2], self.id)
                    else:
                        temp = self.neighbords
                        temp.remove(mensaje[2])
                        for i in temp:
                            #Enviamos el mensaje Go()
                            self.canal_salida.envia("Go", -1, i, self.id)
                else:
                    #Enviamos el mensaje Back(empty)
                    self.canal_salida.envia("Back", -1, mensaje[2], self.id)

            #Recibimos Back(val_set)
            elif (mensaje[0] == "Back"):
                self.expected_msg -= 1
                #val_set is empty
                if mensaje[1] != -1:
                    self.children.add(mensaje[2])

                if self.expected_msg == 0:
                    if self.parent != mensaje[2]:
                        #enviamos Back(i)
                        self.canal_salida.envia("Back", self.id, self.parent, self.id)

if __name__ == "__main__":
    
    # Creamos los nodos
    adyacencias_arbol = [[1, 2], [3], [5], [4], [], []]
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]
    # Creamos la grafica
    grafica = []

    env = simpy.Environment()
    bc_pipe = Canal_generador(env)

    # La lista que representa la gráfica
    grafica = []

    # Creamos los nodos
    for i in range(0, len(adyacencias)):
        grafica.append(NodoGenerador(i, adyacencias[i],
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Le decimos al ambiente lo que va a procesar ...
    for nodo in grafica:
        env.process(nodo.genera_arbol(env))
    # ...y lo corremos
    env.run(until=150)

    # Y probamos que los padres y los hijos sean los correctos.
    padres = [0, 0, 0, 1, 3, 2]
    hijos = [[1, 2], [3], [5], [4], [], []]
    for i in range(0, len(grafica)):
        nodo = grafica[i]
        assert nodo.parent == padres[i], ('El nodo %d tiene un padre erróneo' % nodo.id)
        assert set(nodo.children) == set(hijos[i]), ('El nodo %d no tiene a los hijos correctos'
                                                    % nodo.id)