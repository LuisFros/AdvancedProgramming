    
class Nodo:

    def __init__(self, valor=None):
        self.siguiente = None
        self.valor = valor


class ListaLigada:

    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for arg in args:
            self.append(arg)

    def __len__(self):
        largo = 0
        for i in self:
            largo += 1
        return largo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __repr__(self):
        nodo = self.cabeza
        s = "["
        if nodo:
            s += str(nodo.valor) + ", "
        else:
            return "[]"
        while nodo.siguiente:
            nodo = nodo.siguiente
            s += str(nodo.valor) + ", "
        return s.strip(", ") + "]"

    def __getitem__(self, index):
        nodo = self.cabeza
        if isinstance(index, slice):
            pass
            # temp=ListaLigada()
            # for i in range(index.start):
            #     temp.append(self[i])
            # return temp
        else:
            if index < 0:  # Condicion para recorrer la lista con indices negativos
                # Coincide que el largo mas el indice negativo es su posicion
                # de manera positiva!
                index = len(self) + index
            for i in range(index):
                if nodo:
                    nodo = nodo.siguiente
                else:
                    raise IndexError
            if nodo == None:
                raise IndexError
            else:
                return nodo.valor

    def __setitem__(self, idx, valor):
        Nodo_actual = self.cabeza
        if idx >= len(self):
            raise IndexError
        for i in range(idx):
            Nodo_actual = Nodo_actual.siguiente
        Nodo_actual.valor = valor

    def __gt__(self, other):
        return self[1] > other[1]

    def __eq__(self, other):
        return self.cabeza.valor == other.cabeza.valor

    def index(self, valor):
        contador = 0
        for i in self:
            if i == valor:
                return contador
            contador += 1

    def __siguiente__(self):
        return self.cabeza.siguiente

    def __contains__(self, valor):
        for elemento in self:
            if elemento == valor:
                return True
        return False

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor)
            self.cola = self.cola.siguiente

    def clear(self):
        self = ListaLigada()

    def count(self, valor):
        contador = 0
        for elemento in self:
            if elemento == valor:
                contador += 1
        return contado

    def delete(self, valor):
        actual = self.cabeza
        anterior = None
        encontrado = False
        while actual and encontrado is False:
            if actual.valor == valor:
                encontrado = True
            else:
                anterior = actual
                actual = actual.siguiente
        if actual is None:
            raise ValueError("valor not in list")
        if anterior is None:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente


class ColaPrioridades(ListaLigada):

    def __init__(self, *args):
        super().__init__(*args)

    def crear_cola(self, Pais, paises_conectados, progreso_cura):
        total = Pais.poblacion_viva + Pais.poblacion_infectada + Pais.poblacion_muerta
        prioridad = Pais.poblacion_infectada / \
            (Pais.poblacion_infectada + Pais.poblacion_viva)
        if Pais.poblacion_infectada / total >= 0.5 or Pais.poblacion_muerta / total >= 0.25 and Pais.fronteras_abiertas:
            self.insert(ListaLigada("Cerrar fronteras", promedio_fronteras(
                Pais, paises_conectados) * prioridad))  # Para poder usar la funcion,hay que crear
            # MUNDO!!
        elif Pais.poblacion_infectada / total >= 0.8 or Pais.poblacion_muerta / total >= 0.2 and Pais.aeropuertos_abiertos:
            self.insert(ListaLigada("Cerrar aeropuertos", 0.8 * prioridad))
        elif Pais.poblacion_infectada / total < 0.8 and Pais.poblacion_infectada / total < 0.5 and not Pais.aeropuertos_abiertos and not Pais.fronteras_abiertas:
            if progreso_cura != 1:
                self.insert(ListaLigada("Abrir todo", 0.7 * prioridad))
            else:
                self.insert(ListaLigada("Abrir todo", 1 * prioridad))
        if Pais.poblacion_infectada / total >= 1 / 3:
            self.insert(ListaLigada("Entregar mascarillas", 0.5 * prioridad))

    # Este retorna las primeras tres prioridades en la cola y se eliminan de
    # si mismo
    def primeros_tres(self):
        if len(self) > 3:
            temp1 = self
            temp = ListaLigada(self[-1], self[-2], self[-3])
            self.delete(self[-1])
            self.delete(self[-1])
            self.delete(self[-1])
            return temp
        else:
            temp = ListaLigada()
            for i in reversed(self):
                temp.append(i)
            self.clear()
            return temp

    # Este metodo inserta los valores ordenados en la cola de prioridades!, esto se pueden comparar gracias a un Override
    # de __gt__ en ListaLigada(), el cual compara el segundo elemento de cada
    # lista insertada (la prioridad) :D

    def insert(self, valor):
        actual = self.cabeza
        if actual == None:
            n = Nodo()
            n.valor = valor
            self.cabeza = n
            return

        if actual.valor > valor:
            n = Nodo()
            n.valor = valor
            n.siguiente = actual
            self.cabeza = n
            return

        while actual.siguiente != None:
            if actual.siguiente.valor > valor:
                break
            actual = actual.siguiente
        n = Nodo()
        n.valor = valor
        n.siguiente = actual.siguiente
        actual.siguiente = n
        return

    def pop(self):
        if len(self) > 0:
            ultimo = self[-1]
            return ultimo
        else:
            raise IndexError

    def __repr__(self):
        s = ""
        for i in self:
            s += "Accion: {},Prioridad: {}\n".format(i[0], i[1])
        return s.rstrip()
        