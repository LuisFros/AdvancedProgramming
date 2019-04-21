# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Version2.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
import data
from random import choice
import back_end
import funciones
import time
import sys
from clases import (MyThread, Label, MoveMyImageEvent)


class Edificio(MyThread):
    newid = next(funciones.counter())

    # El generado de id, lo encontre en este link:
    # https://stackoverflow.com/questions/1045344/
    #  how-do-you-create-an-incremental-id-in-a-python-class

    def __init__(self, parent, tipo, team, back):
        super().__init__()
        self.id = Edificio.newid
        self.tipo = tipo
        self.team = team
        self.parent = parent
        if tipo == "Torre":
            self.torre_init(parent, team, back)
        elif tipo == "Inhibidor":
            self.inhib_init(parent, team, back)
        else:
            self.nexo_init(parent, team, back)

    def nexo_init(self, parent, team, back):
        self.image = Label(parent)
        self.image.barra = QtWidgets.QProgressBar(parent)
        self.parent = parent
        self.image.brain = self
        if team == "blue":
            self.image.setPixmap(QtGui.QPixmap("IMGS/nexus.png"))
            self.image.setGeometry(QtCore.QRect(30, 30, 100, 100))
            self.image.barra.setGeometry(QtCore.QRect(30, 30 - 8, 100, 7))
            self.position = (30, 30)
        else:
            self.image.setPixmap(QtGui.QPixmap("IMGS/red_nexus.png"))
            self.image.setGeometry(QtCore.QRect(1120, 600, 150, 120))
            self.image.barra.setGeometry(QtCore.QRect(1140, 600 - 8, 100, 7))
            self.position = (1120, 600)

        self.image.setText("")
        self.image.brain = self
        self.image.setScaledContents(True)
        self.image.setMouseTracking(True)
        self.image.setVisible(True)
        self.image.setObjectName("image")
        self.image.barra.setProperty("value", 100)
        self.image.barra.setTextVisible(False)
        self.image.barra.setObjectName("barra")
        back.make_connection = self.image
        self.image.raise_()
        self.image.show()
        self.agregar_constantes("Nexo")
        self.image.barra.setMaximum(self.life)
        self.image.barra.setProperty("value", self.life)

    def torre_init(self, parent, team, back):

        if team == "blue":
            self.pos_inicial = (150, 130)
            self.position = (150, 130)

            blue = "IMGS/blue.png"
            pixmap = QtGui.QPixmap(blue)
            size = 151, 100
        else:
            self.pos_inicial = (1000, 500)
            self.position = (1000, 500)
            blue = "IMGS/t_purple.png"
            pixmap = QtGui.QPixmap(blue).transformed(QTransform().scale(-1, 1))
            size = 80, 120

        self.parent = parent
        self.image = Label(parent)
        self.image.brain = self
        self.image.setGeometry(QtCore.QRect(self.pos_inicial[0],
                                            self.pos_inicial[1], size[0],
                                            size[1]))
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)
        self.image.setVisible(True)
        self.image.barra = QtWidgets.QProgressBar(parent)
        self.image.barra.setGeometry(QtCore.QRect(self.pos_inicial[0] + 30,
                                                  self.pos_inicial[1] - 8,
                                                  100,
                                                  7))

        self.image.barra.setTextVisible(False)
        self.image.barra.show()
        self.image.barra.raise_()
        back.make_connection = self.image
        self.image.show()
        self.agregar_constantes("Torre")
        self.image.barra.setMaximum(self.life)
        self.image.barra.setProperty("value", self.life)

        # self.trigger.connect(parent.actualizar_imagen)

    def inhib_init(self, parent, team, back):
        self.team = team
        if team == "blue":
            self.pos_inicial = (90, 90)
            self.position = (90, 90)
        else:
            self.pos_inicial = (1050, 570)
            self.position = (1050, 570)
        self.parent = parent
        self.image = Label(parent)
        self.image.brain = self
        self.image.setGeometry(QtCore.QRect(self.pos_inicial[0],
                                            self.pos_inicial[1], 120,
                                            80))
        self.image.setPixmap(QtGui.QPixmap("IMGS/inhib.png"))
        self.image.setScaledContents(True)
        self.image.setObjectName("label_2")
        self.image.setVisible(True)
        self.image.barra = QtWidgets.QProgressBar(parent)
        self.image.barra.setGeometry(QtCore.QRect(self.pos_inicial[0] + 33,
                                                  self.pos_inicial[1] + 15,
                                                  50,
                                                  7))

        self.image.barra.setTextVisible(False)
        self.image.barra.setInvertedAppearance(False)
        self.image.barra.show()
        self.image.barra.raise_()
        back.make_connection = self.image
        self.image.raise_()
        self.image.show()
        self.agregar_constantes("Inhibidor")
        self.image.barra.setMaximum(self.life)
        self.image.barra.setProperty("value", self.life)

    def run(self):
        self.inital_life = self.life
        self.image.show()
        self.image.barra.show()
        self.image.raise_()
        self.image.barra.raise_()
        self.__position = self.position
        while True:
            time.sleep(0.05)
            if self.life <= 0:
                self.image.barra.hide()
                self.image.hide()
                break


class Minion(MyThread):
    newid = next(funciones.counter())

    def __init__(self, parent, tipo, team, back):
        super().__init__()
        self.id = Minion.newid
        self.parent = parent
        self.back = back
        self.team = team
        self.tipo = tipo
        self.agregar_constantes(tipo)

        self.image = Label(parent)
        self.image.thread = self
        self.image.setGeometry(QtCore.QRect(1000, 747, 50, 50))
        self.distance_down = 50
        self.distance_right = 50
        self.image.setPixmap(
            QPixmap("IMGS/Minions/{}_{}.png".format(tipo, team)))
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.barra = QtWidgets.QProgressBar(parent)
        self.image.brain = self
        self.image.barra.setTextVisible(False)
        self.image.barra.setGeometry(QtCore.QRect(1000, 747, 50, 10))
        self.image.barra.setProperty("value", 100)
        self.image.setMouseTracking(True)
        self.agregar_constantes(tipo)
        self._trigger.connect(parent.actualizar_imagen)
        back.make_connection = self.image

        if team == "blue":
            self.pos_inicial = (290, 241)
        else:
            self.pos_inicial = (914, 525)
        self.__position = (0, 0)
        self.position = (self.pos_inicial[0], self.pos_inicial[1])
        self.agregar_constantes(tipo)
        self.image.barra.setMaximum(self.life)
        self.image.barra.setProperty("value", self.life)
        self.rubberband = QtWidgets.QRubberBand(
            QtWidgets.QRubberBand.Rectangle, self.image)
        self.collided = False
        self.atacando = False

    def collision(self, tupla):
        self.collided = True

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):

        self.__position = value
        # El trigger emite su señal a la ventana cuando cambiamos la posición
        self._trigger.emit(MoveMyImageEvent(
            self.image, self.position[0], self.position[1], self
        ))
        self._trigger.emit(MoveMyImageEvent(
            self.image.barra, self.position[0], self.position[1], self
        ))

    def run(self):
        self.image.show()
        self.image.barra.show()
        self.image.raise_()
        self.image.barra.raise_()
        while not (self.is_dead):
            time.sleep(0.05)
            self.move()

        self.image.hide()
        self.image.barra.hide()
        self.image.deleteLater()
        self.image.barra.deleteLater()

    def move(self):
        brain.what_to_do(self, self.parent)
        new = brain.aim(self, self.parent)
        m = self.movement_speed
        teams = {"blue": (-1, 1), "purple": (1, -1)}
        if self.collided and not self.atacando:
            self.position = (
                self.position[0] + new[0] + teams[self.team][0],
                self.position[1] + new[1] + teams[self.team][1])
        elif not self.atacando:
            self.position = (
                self.position[0] + new[0],
                self.position[1] + new[1])
        self.collided = False

    def atacar(self, other):
        self.atacando = True
        while other.life >= 0 and self.life >= 0:
            other.disminuir_vida(self.attack_damage)
        self.atacando = False


class Character(MyThread):
    newid = next(funciones.counter())

    # click = pyqtSignal(tuple)

    # pyqtSignal recibe *args que le indican
    # cuales son los tipos de argumentos que seran enviados
    # en este caso, solo se enviara un argumento:
    #   objeto clase MoveMyImageEv

    def __init__(self, parent, x, y, nombre_champ, team):

        super().__init__()
        self.id = Character.newid
        self.tipo = nombre_champ
        self.team = team
        self.parent = parent
        self.image = QLabel(parent)
        self.image.setGeometry(QtCore.QRect(500, 400, 30, 50))
        self.image.setPixmap(QPixmap("IMGS/{}/0.png".format(nombre_champ)))
        self.image.setScaledContents(True)
        self.llave = None
        self.muertes, self.puntos, self.kills = [0] * 3
        self.image.setVisible(True)
        self.image.show()
        self.image.barra = QtWidgets.QProgressBar(parent)
        self.image.barra.setGeometry(QtCore.QRect(500, 500, 30, 7))
        self.image.barra.setTextVisible(False)
        self.image.barra.setInvertedAppearance(False)
        self.image.barra.show()
        self.image.brain = self
        self.down = funciones.generador_mov(0, 3)
        self.right = funciones.generador_mov(8, 11)
        self.left = funciones.generador_mov(4, 7)
        self.up = funciones.generador_mov(12, 15)
        self._trigger.connect(parent.actualizar_imagen)
        self.__position = (0, 0)
        self.agregar_constantes(nombre_champ)
        self.initial_life = self.life

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):

        self.__position = value
        # El trigger emite su señal a la ventana cuando cambiamos la posición

        self._trigger.emit(MoveMyImageEvent(
            self.image, self.position[0], self.position[1], self
        ))
        self._trigger.emit(MoveMyImageEvent(
            self.image.barra, self.position[0], self.position[1], self
        ))

    def run(self):
        self.initial_life = self.life
        self.image.barra.setMaximum(self.life)
        self.image.barra.setProperty("value", self.life)
        self.image.show()
        self.image.barra.show()
        self.image.raise_()
        self.image.barra.raise_()
        self.position = (self.initial_pos[self.team][0], self.initial_pos[
            self.team][1])
        while True:
            time.sleep(0.05)
            if self.life > 0:
                self.move()
            else:
                self.muertes += 1
                self.image.hide()
                self.image.barra.hide()
                self.image.barra.setProperty("value", self.initial_life)
                self.life = self.initial_life
                self.sleep(5)
                ## Agregar info de la vida maxima antes de
                self.position = (self.initial_pos[self.team][0],
                                 self.initial_pos[self.team][1])
                self.run()

    @property
    def puntos(self):
        return self._puntos

    @puntos.setter
    def puntos(self, value):
        self._puntos = value
        # self.shop

    def move(self):

        self.mouse = None
        nueva = None
        x = None
        self.mouse = LoP.direccion_mouse(self, self.parent)
        self.llave = LoP.direccion_key(self, self.parent)
        if self.mouse:
            tupla = (self.mouse.x(), self.mouse.y())
            # if tupla != self.position:
            #     self.position = (tupla[0], tupla[1])
            # else:
            #     self.position = (self.position[0], 0)
        if self.parent.key is not None:
            cambio = {"W": (0, -1), "D": (1, 0), "A": (-1, 0), "S": (0,
                                                                     1),
                      "-": (0, 0)}
            time.sleep(0.02)
            img = {"W": next(self.up), "D": next(self.right), "A": next(
                self.left), "S": next(
                self.down)}
            path = "IMGS/{}/{}.png".format(self.tipo, img[self.parent.key])
            self.image.setPixmap(QtGui.QPixmap(path))
            self.position = (
                cambio[self.llave][0] * self.movement_speed +
                self.position[
                    0],
                cambio[
                    self.llave][1] * self.movement_speed +
                self.position[1])
            self.parent.key = None

    @property
    def tiempo_revive(self):
        return 10 + (1.1) ** self.muertes


class LoP(QtWidgets.QMainWindow):
    movimiento = pyqtSignal()

    def __init__(self, brain):

        super().__init__()

        self.brain = brain
        self.key = None
        self.teclas_activas = {87: False, 68: False, 83: False, 65: False}
        self.label = Label(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 1300, 750))
        self.label.setPixmap(QtGui.QPixmap("IMGS/background.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label.setMouseTracking(True)
        self.label.setDisabled(False)
        self.label.show()
        self.label.raise_()

        self.minions_timer = QtCore.QTimer()
        self.minions_timer.start(10000)
        self.minions_timer.timeout.connect(self.minion_spawner)
        self.mouse = None
        self.instanciar_personajes()
        engine = back_end.ShopEngine(self.champ)
        self.shop = Shop(engine)

    @staticmethod
    def actualizar_imagen(myImageEvent):
        # Recibo el objeto con la información necesaria para mover a bastián
        # Hagamos un print para corroborar su posición?
        label = myImageEvent.image
        label.move(myImageEvent.x, myImageEvent.y)

    @staticmethod
    def direccion_mouse(objeto, other):
        if other.mouse:
            return other.mouse
        else:
            return None

    @staticmethod
    def direccion_key(objeto, other):
        if other.key:
            return other.key
        else:
            return None

    @staticmethod
    def crear_juego():
        pass

    def mouseMoveEvent(self, event):
        super(LoP, self).mouseMoveEvent(event)
        if event.buttons() == Qt.NoButton:
            self.mouse = event.pos()

    def keyPressEvent(self, event):
        llaves = {87: "W", 68: "D", 83: "S", 65: "A"}
        super(LoP, self).keyPressEvent(event)
        if event.key() in llaves:
            self.key = llaves[event.key()]
        elif event.key() == QtCore.Qt.Key_O:
            self.shop.show()
        elif event.key() == QtCore.Qt.Key_P:
            self.pausar()

    def iniciar(self):
        self.champ.start()
        self.inhibidor_blue.start()
        self.inhibidor_purple.start()
        self.torre_blue.start()
        self.torre_purple.start()
        self.nexo_blue.start()
        self.nexo_purple.start()


    def minion_spawner(self):
        colores = ("purple", "blue")
        for color in colores:
            self.minion_3 = Minion(self, "Subditos_fuertes", color,
                                   self.brain)
            self.minion_2 = Minion(self, "Subditos_debiles", color,
                                   self.brain)
            self.minion_1 = Minion(self, "Subditos_debiles", color,
                                   self.brain)
            self.minion_4 = Minion(self, "Subditos_debiles", color,
                                   self.brain)
            self.minion_5 = Minion(self, "Subditos_debiles", color,
                                   self.brain)
            minions = {1: self.minion_1, 2: self.minion_2,
                       3: self.minion_3, 4: self.minion_4, 5:
                           self.minion_5, }
            circulo = {1: (-1, 0), 3: (-1, -1), 2: (0, 1), 4: (1, 1), 5: (1, 0)}

            for i in minions:
                minions[i].position = (
                    minions[i].position[0] + circulo[i][0] * 100,
                    minions[i].position[1] + circulo[i][1] * 100)
                minions[i].start()

    def instanciar_personajes(self):
        lista_threads = []
        # Aca se instancian los objetos desde el archivo de constantes
        # Simplemente cambiar el nombre para probar los otros champions!,
        # Los nombres estan en constantes.json
        self.champ = Character(self, 0, 0, "Hechicera", "purple")
        self.inhibidor_blue = Edificio(self, "Inhibidor", "blue", self.brain)
        self.inhibidor_purple = Edificio(self, "Inhibidor", "purple",
                                         self.brain)
        self.torre_purple = Edificio(self, "Torre", "purple", self.brain)
        self.torre_blue = Edificio(self, "Torre", "blue", self.brain)
        self.nexo_blue = Edificio(self, "Nexo", "blue", self.brain)
        self.nexo_purple = Edificio(self, "Nexo", "purple", self.brain)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 750)
        MainWindow.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("IMGS/window_icon.jpg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(8.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(200, 200))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setMouseTracking(True)

        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(0, 0, 1300, 750))
        # self.label.setPixmap(QtGui.QPixmap("IMGS/background.png"))
        # self.label.setScaledContents(True)
        # self.label.setObjectName("label")
        # self.label.setMouseTracking(True)
        # self.label.setDisabled(False)
        # self.label.show()
        # self.label.raise_()


        # self.barra_nexus_purple.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 47))
        # self.menubar.setObjectName("menubar")
        # self.menuLeague_of_Progra = QtWidgets.QMenu(self.menubar)
        # self.menuLeague_of_Progra.setObjectName("menuLeague_of_Progra")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        # self.toolBar = QtWidgets.QToolBar(MainWindow)
        # self.toolBar.setObjectName("toolBar")
        # MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # self.menubar.addAction(self.menuLeague_of_Progra.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.menuLeague_of_Progra.setTitle(
        #     _translate("MainWindow", "League of Progra"))
        # self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))


class StartMenu(QtWidgets.QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.setObjectName("Dialog")
        self.resize(1256, 975)
        self.setStyleSheet("")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 580, 231, 61))
        self.pushButton_2.setAutoFillBackground(True)
        self.pushButton_2.setStyleSheet('background-color:lightblue')
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText("Continuar Partida")
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 450, 231, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Nueva Partida")
        # Conecciones:
        self.pushButton_3.clicked.connect(self.ocultar)
        # self.pushButton_3.clicked.connect(self.main.show)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(-10, 0, 1271, 371))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("IMGS/title_screen.jpg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(-10, 370, 1281, 601))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("IMGS/title_background.jpg"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_2.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.label.raise_()

    def ocultar(self):
        self.main.crear_juego
        self.hide()
        self.main.setFixedSize(self.main.size())
        self.main.iniciar()
        self.main.show()
        self.main.showNormal()
        self.main.raise_()


class Enemy:
    def __init__(self):
        self.personalidad = choice(["Noob", "RageQuitter", "Normal"])


class Shop(QtWidgets.QDialog):
    def __init__(self, brain):
        super(Shop, self).__init__()
        self.brain = brain
        self.setObjectName("Dialog")
        self.resize(500, 700)
        self.setMouseTracking(True)
        self.setStyleSheet("")
        self.setSizeGripEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("IMGS/window_icon.jpg"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 122, 661))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_7.setMouseTracking(True)
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("IMGS/Shop/arma_mano.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_7.setObjectName("label_7")
        self.verticalLayout.addWidget(self.label_7)
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("IMGS/Shop/arma_distancia.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("IMGS/Shop/botas.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("IMGS/Shop/baculo.png"))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("IMGS/Shop/armadura.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("IMGS/Shop/earthstone.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.pushButton_15 = QtWidgets.QPushButton(self)
        self.pushButton_15.setGeometry(QtCore.QRect(200, 40, 119, 28))
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self)
        self.pushButton_16.setGeometry(QtCore.QRect(200, 140, 119, 28))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self)
        self.pushButton_17.setGeometry(QtCore.QRect(200, 260, 119, 28))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self)
        self.pushButton_18.setGeometry(QtCore.QRect(200, 370, 119, 28))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self)
        self.pushButton_19.setGeometry(QtCore.QRect(200, 490, 119, 28))
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self)
        self.pushButton_20.setGeometry(QtCore.QRect(200, 600, 119, 28))
        self.pushButton_20.setObjectName("pushButton_20")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(360, 20, 51, 21))
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(360, 120, 51, 21))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(360, 230, 51, 21))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(360, 340, 51, 21))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(360, 470, 51, 21))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self)
        self.label_12.setGeometry(QtCore.QRect(360, 570, 51, 21))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self)
        self.label_13.setGeometry(QtCore.QRect(370, 40, 121, 31))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self)
        self.label_14.setGeometry(QtCore.QRect(370, 150, 121, 31))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self)
        self.label_15.setGeometry(QtCore.QRect(370, 260, 131, 31))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self)
        self.label_16.setGeometry(QtCore.QRect(370, 370, 131, 31))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self)
        self.label_17.setGeometry(QtCore.QRect(370, 490, 131, 31))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self)
        self.label_18.setGeometry(QtCore.QRect(360, 590, 131, 31))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self)
        self.label_19.setGeometry(QtCore.QRect(210, 660, 51, 21))
        self.label_19.setObjectName("label_19")
        self.verticalLayoutWidget.raise_()
        self.pushButton_15.raise_()
        self.pushButton_16.raise_()
        self.pushButton_17.raise_()
        self.pushButton_18.raise_()
        self.pushButton_19.raise_()
        self.pushButton_20.raise_()
        self.label.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.label_18.raise_()
        self.label_19.raise_()
        self.setWindowTitle("Tienda")
        self.pushButton_15.setText("Arma de Mano")
        self.label.setText("Precio:5")
        self.label_8.setText("Precio:5")
        self.label_9.setText("Precio:2")
        self.label_10.setText("Precio:7")
        self.label_11.setText("Precio:5")
        self.label_12.setText("Precio:10")
        self.label_13.setText("#daño+5")
        self.label_14.setText("#rango+2")
        self.label_15.setText("#velocidad+3")
        self.label_16.setText("#habilidad+2")
        self.label_17.setText("#vida+2")
        self.label_18.setText("#aleatorio+6")
        self.pushButton_15.kids = (self.label, self.label_13)
        self.pushButton_15.clicked.connect(self.fifteen)
        self.pushButton_16.kids = (self.label_8, self.label_14)
        self.pushButton_16.clicked.connect(self.sixteen)
        self.pushButton_17.kids = (self.label_9, self.label_15)
        self.pushButton_17.clicked.connect(self.seventeen)
        self.pushButton_18.kids = (self.label_10, self.label_16)

        self.pushButton_18.clicked.connect(self.eightteen)
        self.pushButton_19.kids = (self.label_11, self.label_17)
        self.pushButton_19.clicked.connect(self.nineteen)
        self.pushButton_20.kids = (self.label_12, self.label_18)
        self.pushButton_20.clicked.connect(self.twenty)
        self.pushButton_16.setText("Arma a distancia")
        self.pushButton_17.setText("Botas")
        self.pushButton_18.setText("Baculo")
        self.pushButton_19.setText("Aramdura")
        self.pushButton_20.setText("Earthstone")

    def fifteen(self):
        tupla = self.pushButton_15.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def sixteen(self):
        tupla = self.pushButton_16.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def seventeen(self):
        tupla = self.pushButton_17.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def eightteen(self):
        tupla = self.pushButton_18.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def nineteen(self):
        tupla = self.pushButton_19.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def twenty(self):
        tupla = self.pushButton_20.kids
        self.brain.Upgrade(tupla[0], tupla[1])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_O:
            self.hide()

    def feed(self, champion):
        self.brain.champion = champion

    @property
    def points(self):
        pass


if __name__ == "__main__":
    def catch_exceptions(t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "An exception was raised",
                                       "Exception type: {}".format(t))
        old_hook(t, val, tb)


    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions
    data.main()
    app = QtWidgets.QApplication(sys.argv)

    brain = back_end.GameEngine()
    MainWindow = LoP(brain)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    venta = StartMenu(MainWindow)
    venta.showNormal()

    sys.exit(app.exec_())
