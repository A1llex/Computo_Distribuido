#Ejercicio Extra
from Nodo import *
import Canales.CanalConvergecast

class NodoConvergecast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    #se usara en el constructor que a cada nodo se le añada su padre
    def __init__(self, id_nodo, padre, hijos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.padre = padre
        self.hijos = hijos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = ""
        self.val_set = set()

    def broadcast(self, env):
        '''Función de broadcast para nodos. Resuelto por el algoritmo de flooding.'''
        #iniciamos el mensaje
        self.mensaje = "informacion"
        if self.hijos == [] : # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            self.canal_salida.envia("Back",(self.id_nodo,self.mensaje),self.padre)
            yield env.timeout(1)

        else:
            while True:
                mensaj = yield self.canal_entrada.get()
                # Esperamos a que nos llegue el mensaje
                yield env.timeout(1)
                if not mensaj:
                    break
                elif (mensaj[0] == "Back"):
                    self.val_set.add((self.id_nodo,self.mensaje))
                    self.val_set.add(mensaj[1])
                    yield env.timeout(1)
                    if(not self.padre == self.id_nodo):
                        self.canal_salida.envia("Back",(self.id_nodo,self.mensaje),self.padre)
                    else :
                        print("Se ha Terminado el computo")
                        print(self.val_set)