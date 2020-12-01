#ejercicio 3
import simpy
from Nodo import *
from Canales.CanalBroadcast import *

class NodoBroadcast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, hijos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.hijos = hijos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = ""

    def broadcast(self, env):
        '''Función de broadcast para nodos. Resuelto por el algoritmo de flooding.'''
        if self.id_nodo == 0: # Solo el nodo raiz (representado con id = 0) envia el primer msj
            # Esperamos la siguiente transmisión
            self.mensaje = "informacion"
            self.canal_salida.envia(self.mensaje,self.hijos)
            yield env.timeout(1)

        else:
            while True:
                mensaj = yield self.canal_entrada.get()
                # Esperamos a que nos llegue el mensaje
                yield env.timeout(1)
                if not mensaj:
                    break
                else: 
                    #cuando nos llegue un mensaje lo enviaremos a nuestros hijos
                    self.mensaje = mensaj
                    self.canal_salida.envia(self.mensaje,self.hijos)
                    yield env.timeout(1)

if __name__ == "__main__":
    # Inicializamos ambiente y canal
    env = simpy.Environment()
    bc_pipe = CanalBroadcast(env)
    # La lista que representa la gráfica
    grafica = []
    adyacencias = [[1, 2], [0, 3], [0, 3, 5], [1, 2, 4], [3, 5], [2, 4]]
    adyacencias_arbol = [[1, 2], [3], [5], [4], [], []]
    
    # Creamos los nodos
    for i in range(0, len(adyacencias)):
        grafica.append(NodoBroadcast(i, adyacencias_arbol[i],
                                    bc_pipe.crea_canal_de_entrada(), bc_pipe))

    # Le decimos al ambiente lo que va a procesar ...
    for nodo in grafica:
        env.process(nodo.broadcast(env))
    # ...y lo corremos
    #env.run(until=150)

    # Probamos que todos los nodos tengan ya el mensaje
    mensaje_enviado = grafica[0].mensaje
    for nodo in grafica:
        assert mensaje_enviado == nodo.mensaje, ('El nodo %d no tiene el mensaje correcto' % nodo.id_nodo)
    print("ya que no salio ningun mensaje de error funciono")
