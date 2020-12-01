import simpy
import random
from Nodo import *
from Canales.CanalRecorridos import *

class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast asíncrono.
        Usa el reloj de Lamport para asignar a cada evento una timestamp que respeta
        el orden causal.
    '''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS usando el
            reloj de Lamport.
        '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = id_nodo
        self.distancia = float('inf') if id_nodo != 0 else 0
        self.reloj = 0 # Reloj de lamport
        self.eventos = [] # Lista de eventos

    def bfs(self, env):
        ''' Algoritmo BFS asíncrono. '''
        if self.distancia == 0:
            yield env.timeout(random.randint(0, 10)) # Tenemos sistema asíncrono
            self.reloj = self.reloj + 1 # Actualizamos el reloj
            # Tenemos que enviar el valor de nuestro reloj para el reloj de Lamport
            self.canal_salida.envia([self.distancia, self.id_nodo, self.reloj], self.vecinos)
            # Agregamos los eventos necesarios
            self.agrega_eventos(self.distancia, 'E', self.id_nodo, self.vecinos)

        while True:
            yield env.timeout(random.randint(0, 10)) # Tenemos sistema asíncrono
            mensaje = yield self.canal_entrada.get() # Esperamos a que nos llegue un mensaje
            d = mensaje[0] # La distancia que nos enviaron
            p = mensaje[1] # El nodo que nos la envío
            reloj_recibido = mensaje[2]
            self.reloj = max(reloj_recibido, self.reloj) + 1 #Actualizamos el reloj
            self.agrega_eventos(d, 'R', p, [self.id_nodo]) # Agregamos el evento de recepción.
            if d + 1 < self.distancia:
                self.distancia = d + 1
                self.padre = p
                yield env.timeout(random.randint(0, 10))
                self.canal_salida.envia([self.distancia, self.id_nodo, self.reloj], self.vecinos)
                self.agrega_eventos(self.distancia, 'E', self.id_nodo, self.vecinos)

    def agrega_eventos(self, tipo, mensaje, emisor, receptores):
        ''' Función auxiliar para agregar los eventos a la lista correspondiente. '''
        for receptor in receptores:
            self.eventos.append([self.reloj, tipo, mensaje, emisor, receptor])



a = [[3], [2, 3, 4], [1, 3], [0, 1, 2], [1]]
env = simpy.Environment()
bc_pipe = CanalRecorridos(env)
grafica = []
for i in range(0, len(a)):
    grafica.append(NodoBFS(i, a[i], bc_pipe.crea_canal_de_entrada(), bc_pipe))

for n in grafica:
    env.process(n.bfs(env))
