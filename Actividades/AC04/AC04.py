# PRIMERA PARTE: Estructura basica
class ListaLigada:

    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for arg in args:
            self.agregar_nodo(arg)

    def agregar_nodo(self, nombre):
        if not self.cabeza:
            # Revisamos si el nodo cabeza tiene un nodo asignado.
            # Si no tiene nodo, creamos un nodo
            self.cabeza = Isla(nombre)
            self.cola = self.cabeza
        else:
            # Si ya tiene un nodo
            self.cola.hijo = Isla(nombre)
            self.cola = self.cola.hijo

    def obtener(self, posicion):
        nodo = self.cabeza
        for i in range(posicion):
            if nodo:
                nodo = nodo
        if not nodo:
            return "posicion no encontrada"
        else:
            return nodo.nombre

    def __repr__(self):
        rep = ''
        nodo_actual = self.cabeza
        while nodo_actual:
            rep += '{0}->'.format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente

    def __getitem__(self, index):
        nodo = self.cabeza
        for i in range(index):
            if nodo:
                nodo.hijo
            else:
                raise IndexError
        if not nodo:
            raise IndexError
        else:
            nodo.nombre
    def __iter__(self):
        return self
    def __contains__(self, nombre):  # PARA VERIFICAR SI HAY UN ELEMENTO EN LA LISTA LIGADA
        for elemento in self:
            if elemento.nombre == nombre:
                return True
        return False


# SEGUNDA PARTE: Clase Isla


class Isla:

    def __init__(self, nombre):
        self.nombre = nombre
        self.hijo = None

    def __repr__(self):
        return 'nombre: {0}, siguiente: {1}'.format(self.nombre, self.hijo)

# TERCERA PARTE: Clase Archipielago


class Archipielago:

    def __init__(self,nombre_archivo,islas=ListaLigada()):
        self.nombre_archivo = nombre_archivo
        self.islas=islas
        self.construir(nombre_archivo)
       

    def __repr__(self):
        s=""
        for isla in self.islas:
            s+isla.nombre+"-"
        return s

    def agregar_isla(self, nombre):
    	self.islas.agregar_nodo(nombre)

    def conectadas(self, nombre_origen, nombre_destino):
        pass

    def agregar_conexion(self, padre, hijo):
        if padre not in self.islas:

            self.agregar_isla(padre)
        if hijo not in self.islas:
            self.agregar_isla(hijo)
        Isla(nombre_origen,nombre_destino)

    def construir(self, archivo):

    	with open("{}".format(self.nombre_archivo)) as archivo:
            for linea in archivo:
                padre,hijo = linea.strip().split(",")
                self.agregar_conexion(padre,hijo)

    def propagacion(self, nombre_origen):#Se asume que el nombre de origen esta en el archipielago
        if self.islas[0].nombre==nombre_origen:
            return self.islas[0].nombre
        else:
            return ""+self.islas


if __name__ == '__main__':
    
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")  # Instancia y construye
    # print(arch)  # Imprime el Archipielago de una forma que se pueda entender
    # print(arch.propagacion("Perresus"))
    # print(arch.propagacion("Pasesterot"))
    # print(arch.propagacion("Cartonat"))
    # print(arch.propagacion("Womeston"))
