import simpy

class Canal_vecinos():
    '''
    Clase que modela un canal para el algoritmo 1 de la practica
    '''
    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []
        self.canal_de_salida = None

    def envia(self, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.
        '''
        if not self.canales:
            raise RuntimeError('No hay canales de salida.')
        eventos = list()
        for i in range(len(self.canales)):
            if i in vecinos:
                eventos.append(self.canales[i].put(vecinos))
        return self.env.all_of(eventos)

    def crea_canal_de_entrada(self):
        '''
        Creamos un objeto Store en el cual recibiremos los mensajes.
        '''
        canal = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal)
        self.canal_de_salida = canal
        return canal

    def get_canal_de_salida(self):
        '''
        Regresa el objeto Store en el cual recibiremos los mensajes.
        '''
        return self.canal_de_salida