"""
======================================================================
>> Autores: Johann Gordillo [jgordillo@ciencias.unam.mx]
            Alex Fernández  [alex@ciencias.unam.mx]

>> Fecha:   01/12/2020
======================================================================
Universidad Nacional Autónoma de México
Facultad de Ciencias

Computación Distribuida [2021-1]

Ejercicio 2.
Algoritmo DFS asíncrono con relojes vectoriales.
======================================================================
"""

import simpy
from random import randint

from Nodo import Nodo
from Canales.CanalRecorridos import CanalRecorridos


class NodoDFS(Nodo):
    """Implementa la interfaz de Nodo para el algoritmo de Broadcast
    asíncrono. Usa el reloj de Lamport para asignar a cada evento
    una timestamp que respeta el orden causal."""
    def __init__(self, id_nodo: int, vecinos: set,
                 canal_entrada: simpy.Store,
                 canal_salida: simpy.Store,
                 order: int):
        """Constructor para el nodo."""
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.padre = id_nodo
        self.order = order  # Orden de la gráfica.
        self.eventos = list()  # Lista de eventos
        self.reloj = [0] * self.order  # Reloj vectorial

    def dfs(self, env):
        """Implementación del algoritmo DFS."""
        # Nodo distinguido (id = 0).
        if self.id_nodo == 0:
            # El nodo distinguido es su propio padre.
            self.padre = self.id_nodo

            # La estructura es (msg_type, sender, visited).
            data = ("GO", self.id_nodo, {self.id_nodo})

            # Enviamos el mensaje a un vecino k.
            # Por convención, tomamos el vecino con menor id.
            k = min(self.vecinos)
            self.hijos = {k}

            # Aumentamos nuestra entrada en el reloj vectorial.
            self.reloj[self.id_nodo] += 1

            # Agregamos los eventos de envío.
            msg = [data, self.id_nodo, self.reloj]
            self.canal_salida.envia(msg, [k])
            self.agrega_eventos('E', msg, self.id_nodo, [k], env)

        while True:
            # Esperamos a que nos llegue el mensaje.
            data, emisor, reloj_emisor = yield self.canal_entrada.get()
            msg_type, _, visited = data

            # Actualizamos el reloj vectorial.
            self.actualiza_reloj(reloj_emisor)

            # Agregamos el evento de recepción.
            self.agrega_eventos('R', [data, emisor, reloj_emisor], emisor, [self.id_nodo], env)

            # Cuando recibimos un mensaje GO(visited).
            if msg_type == "GO":
                # Su padre será el nodo del que recibió el mensaje.
                self.padre = emisor

                if self.vecinos.issubset(visited):
                    data = ("BACK", self.id_nodo, visited.union({self.id_nodo}))
                    self.hijos = set()

                    # Agregamos los eventos de envío.
                    msg = [data, self.id_nodo, self.reloj]
                    self.canal_salida.envia(msg, [emisor])
                    self.agrega_eventos('E', msg, self.id_nodo, [emisor], env)

                else:
                    k = min(self.vecinos.difference(visited))
                    data = ("GO", self.id_nodo, visited.union({self.id_nodo}))
                    self.hijos = {k}

                    # Agregamos los eventos de envío.
                    msg = [data, self.id_nodo, self.reloj]
                    self.canal_salida.envia(msg, [k])
                    self.agrega_eventos('E', msg, self.id_nodo, [k], env)

            # Cuando recibimos un mensaje BACK(visited).
            elif msg_type == "BACK":
                if self.vecinos.issubset(visited):
                    # Terminación global.
                    if self.padre == self.id_nodo:
                        print("Ha terminado la ejecución del algoritmo.")
                        return
                    # Terminación local.
                    else:
                        data = ("BACK", self.id_nodo, visited)
                        msg = [data, self.id_nodo, self.reloj]
                        self.canal_salida.envia(msg, [self.padre])
                        self.agrega_eventos('E', msg, self.id_nodo, [self.padre], env)

                else:
                    k = min(self.vecinos.difference(visited))
                    data = ("GO", self.id_nodo, visited)
                    self.hijos = self.hijos.union({k})

                    # Agregamos los eventos de envío.
                    msg = [data, self.id_nodo, self.reloj]
                    self.canal_salida.envia(msg, [k])
                    self.agrega_eventos('E', msg, self.id_nodo, [k], env)

            # Si el tipo de mensaje no existe, lanzamos excepción.
            else:
                raise Exception("El tipo de mensaje no existe.")

    def agrega_eventos(self, tipo, mensaje, emisor, receptores, env):
        """Función auxiliar para agregar los eventos a la lista correspondiente."""
        for receptor in receptores:
            if tipo == 'E':
                yield env.timeout(randint(0, 10))
            self.eventos.append([self.reloj, tipo, mensaje, emisor, receptor])

    def actualiza_reloj(self, reloj_emisor):
        """Función auxiliar para actualizar el reloj vectorial."""
        for i in range(self.order):
            if i == self.id_nodo:
                self.reloj[i] += 1
            else:
                self.reloj[i] = max(reloj_emisor[i], self.reloj[i])


if __name__ == "__main__":
    print("Ejercicio 2.")
