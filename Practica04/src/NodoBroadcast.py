"""
======================================================================
>> Autores: Johann Gordillo [jgordillo@ciencias.unam.mx]
            Alex Fernández  [alex@ciencias.unam.mx]

>> Fecha:   01/12/2020
======================================================================
Universidad Nacional Autónoma de México
Facultad de Ciencias

Computación Distribuida [2021-1]

Ejercicio 1.
Broadcast Asíncrono con relojes lógicos de Lamport.
======================================================================
"""

import simpy
from random import randint

from Nodo import Nodo
from Canales.CanalRecorridos import CanalRecorridos


class NodoBroadcast(Nodo):
    """Implementa la interfaz de Nodo para el algoritmo para conocer a
    los vecinos de mis vecinos."""
    def __init__(self, id_nodo: int, vecinos: list,
                 canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        """Constructor para el nodo."""
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.reloj = 0  # Reloj de Lamport.
        self.eventos = list()  # Lista de eventos

    def broadcast(self, env: simpy.Environment):
        """Función para que un nodo colabore en la construcción
        de un árbol generador."""
        # Solo el nodo raiz (id = 0) envía el primer mensaje.
        if self.id_nodo == 0:
            # Mensaje que se quiere difundir.
            self.mensaje = "Hello, Graph"

            # Tenemos que enviar el valor de nuestro reloj para el reloj de Lamport.
            msg = [self.mensaje, self.id_nodo, self.reloj]
            self.canal_salida.envia(msg, self.vecinos)

            # Agregamos los eventos necesarios.
            self.agrega_eventos('E', self.mensaje, self.id_nodo, self.vecinos, env)

        # Para los nodos no distinguidos data será nula.
        else:
            self.data = None

        while True:
            # Esperamos a que nos llegue el mensaje.
            self.mensaje, emisor, reloj_emisor = yield self.canal_entrada.get()

            # Actualizamos el reloj.
            self.reloj = max(reloj_emisor, self.reloj) + 1

            # Agregamos el evento de recepción.
            self.agrega_eventos('R', self.mensaje, emisor, [self.id_nodo], env)
            
            # Reenvíamos el mensaje a nuestros hijos.
            if len(self.vecinos) > 0:
                msg = [self.mensaje, self.id_nodo, self.reloj]
                self.canal_salida.envia(msg, self.vecinos)
                self.agrega_eventos('E', self.mensaje, self.id_nodo, self.vecinos, env)

    def agrega_eventos(self, tipo, mensaje, emisor, receptores, env):
        """Función auxiliar para agregar los eventos a la lista correspondiente."""
        for receptor in receptores:
            if tipo == 'E':
                yield env.timeout(randint(0, 10))
            self.eventos.append([self.reloj, tipo, mensaje, emisor, receptor])


if __name__ == "__main__":
    print("Ejercicio 1.")
