from PyQt5.QtCore import QThread,pyqtSignal,Qt
from PyQt5.QtWidgets import QLabel
from json import load


class MoveMyImageEvent:
    """
    Las instancias de esta clase
    contienen la informacion necesaria
    para que la ventana actualice
    la posicion de la imagen
    """

    def __init__(self, image, x, y, thread):
        self.image = image
        self.thread = thread
        self.x = x
        self.y = y


def generador_senales(tipo):
    a = pyqtSignal(tipo)
    while True:
        yield a
        a = pyqtSignal(tipo)


gen_senales = generador_senales(dict)
gen_senales_2 = generador_senales(MoveMyImageEvent)


class MyThread(QThread):
    _trigger = next(gen_senales_2)

    @classmethod
    def click(cls):
        Label._trigger = next(gen_senales_2)
        return cls._trigger

    def __init__(self):
        super().__init__()

    @property
    def is_dead(self):
        return self.life <= 0

    def agregar_constantes(self, nombre):
        with open("constantes.json", "r") as data:
            json_data = load(data)
        self.__dict__.update(**json_data[nombre])

    def disminuir_vida(self, damage):
        self.life -= damage
        actual = self.image.barra.value() - damage
        self.image.barra.setValue(actual)


class Label(QLabel):
    _click = next(gen_senales)

    @classmethod
    def click(cls):
        Label._click = next(gen_senales)
        return cls._click

    def __init__(self, *args):
        super().__init__(*args)
        self.parent = args[0]
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.buttons() == Qt.LeftButton:
            destino = self.mapToParent(event.pos())
            destino = (destino.x() - 49, destino.y() - 41) # correccion de pos
            origen = self.parent.champ.position
            aux = {"user": self.parent.champ, "destino": destino,
                   "origen": origen, "target": self.brain}
            self._click.emit(aux)
