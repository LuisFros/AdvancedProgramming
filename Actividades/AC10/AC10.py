from threading import Thread, Lock
from random import randint, expovariate
import time


class Persona(Thread):
    def __init__(self, pieza_actual=None):
        super().__init__()
        self._vida_actual = randint(80, 120)
        self.vida = randint(80, 120)
        resistance = randint(1, 3)
        self.resistance = resistance
        self.pieza_actual = pieza_actual
        self.tiempo_inicio = time.time()
        self.tiempo_termino = 0

    def mover(self, proxima):
        with proxima.lock:
            print("{} Se mueva a {}".format(self.name,proxima._id))
            self.pieza_actual = proxima
            time.sleep(randint(1, 3))

    @property
    def vida_actual(self):
        return self._vida_actual

    @vida_actual.setter
    def vida_actual(self, tiempo):
        if not self.muerto:
            self._vida_actual = self._vida_actual - (6 - self.resistance) * (
                tiempo - self.tiempo_inicio)
            if self.vida_actual > 0:
                self.muerto = False
            else:
                print("Se ha muerto una persona en la pieza {}".format(
                    self.pieza_actual))
                self.muerto = True

    @property
    def vivo(self):
        if self.vida_actual <= 0:
            self.tiempo_termino=-self.tiempo_inicio+time.time()
            return False
        else:
            return True

    def run(self):
        while not self.vivo:
            pass

    def __repr__(self):
        return "{}-{}-{}".format(self.name, self.tiempo_termino,
                                 self.tiempo_inicio)


# Agregar Spawner a Laberithn (Thread)



class Pieza:
    primera = None
    ultima = None

    def __init__(self, id):
        self._id = id
        self.ocupada = False
        self.ultima = False
        self.primera = False
        self.siguientes = list()
        self.lock = Lock()


class Laberinth(Thread):
    def __init__(self):
        super().__init__()
        self.conections = dict()
        self.piezas = list()
        self.personas = list()
        self.ganadores=[]
        with open("laberinto.txt", "r") as file:
            self.inicio = Pieza(file.readline().strip())
            self.meta = Pieza(file.readline().strip())
            self.piezas.append(self.inicio)
            self.piezas.append(self.meta)
            self.conections[self.inicio._id] = []
            self.conections[self.meta._id] = []

            Pieza.primera = self.inicio
            Pieza.ultima = self.meta

            for i in file:
                a, b = tuple(i.strip().split(","))

                if a not in [pieza._id for pieza in
                             self.piezas]:
                    pieza_a = Pieza(a)
                    self.piezas.append(pieza_a)
                    self.conections[a] = []

                else:
                    pieza_a = self.get_pieza(a)

                if b not in [pieza._id for pieza in
                             self.piezas]:
                    pieza_b = Pieza(b)
                    self.piezas.append(pieza_b)
                    self.conections[b] = []

                else:
                    pieza_b = self.get_pieza(b)

                pieza_a.siguientes.append(b)
                self.conections[a].append(pieza_b)

    def run(self):
        spawner = Thread(target=self.spawn, daemon=True)
        limpiador = Thread(target=self.limpiador, daemon=True)
        spawner.start()
        limpiador.start()
        while len(self.ganadores) < 3:
            actual = time.time()
            for persona in self.personas:
                if persona not in self.ganadores:
                    persona.mover(self.inicio)
                    if persona.pieza_actual == self.meta:
                        self.ganadores.append(persona)


    def get_pieza(self, id):
        return list(filter(lambda x: x._id == id, self.piezas))[
            0]

    def spawn(self):
        while True:
           
            a = expovariate(1 / 5)
            time.sleep(a)
            persona = Persona(self.inicio)
            self.personas.append(persona)
            print("Se creo la persona {} en {}".format(persona.name,
                                                       a+time.time()))

            persona.start()

    def limpiador(self):
        muertos = 0
        self.muertos = []
        while True:
            time.sleep(1)
            for persona in self.personas:
                if not persona.isAlive:
                    self.muertos.append(persona)
            for persona in self.muertos:
                if persona in self.personas:
                    self.personas.pop(self.personas.index(persona))

if __name__ == '__main__':
    Lab = Laberinth()
    print(Lab.conections["1"])
    Lab.start()
