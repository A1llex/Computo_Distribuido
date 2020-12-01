import simpy

class Canal_generador():
    '''
    Clase que modela un canal para el algorimo del arbol generador.
    '''
    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []
        self.canal_de_salida = None

    def envia(self, mensaje, parametro, paraElNodo, delNodo):
        '''
        Envia un arrelgo a u vecino en especifico.
        los siguientes elementos son:
        .mensaje: es el identificador para saber si se manda el metodo Go o el metodo Back.
        .parametro: nos indica si enviamos back con vacio (representado con -1) o no.
        .paraElNodo: Entero que nos indica el indice en nuestra lista de canales que representa
        el nodo al cual se quiere enviar el mensaje
        .delNodo: Entero que nos indica de que nodo viene el mensaje
        '''
        eventos = list()
        eventos.append(self.canales[paraElNodo].put([mensaje, parametro, delNodo]))
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