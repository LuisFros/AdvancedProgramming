# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.Qt import QSound
from Room import Room
from Sala import Sala
import time


class MiVentana(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.song = "temp.wav"
        self.init_GUI()

    def init_GUI(self):
        """
        Este método inicializa la interfaz y todos sus elementos o Widgets
        una vez que es llamado el formulario.
        """

        # Podemos agrupar conjuntos de widgets en alguna estructura
        self.labels = {}
        self.labels['label1'] = QLabel('Texto:', self)
        self.labels['label1'].move(10, 15)
        self.labels['label2'] = QLabel('Aqui se escribe la respuesta', self)
        self.labels['label2'].move(10, 50)

        """
        El uso del caracter & al inicio del texto de algún botón o menú permite
        que la primera letra del mensaje mostrado esté destacada. La
        visualización depende de la plataforma utilizada.
        """
        self.boton1 = QPushButton('&Procesar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.clicked.connect(self.play)
        self.boton1.move(5, 70)

        """Agrega todos los elementos al formulario."""
        self.setGeometry(200, 100, 300, 300)
        self.setWindowTitle('Ventana con Boton')


class MyStart(QtWidgets.QDialog):
    def __init__(self):
        super(MyStart, self).__init__()
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(210, 220, 113, 22))
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")

        self.room = Room()
        self.get_button()

    def connect_func(self, func):
        self.cliente = func
        print(type(self.cliente))
        self.lineEdit.returnPressed.connect(self.sf)

    def sf(self):
        user = self.lineEdit.text().strip()
        self.room.show()
        if len(user) > 0:
            self.hide()
            sala = None
            self.cliente.send("{}&{}&{}".format(sala, True, user))

    def get_button(self):
        botton = self.room.findChild(QtWidgets.QPushButton)
        self.room.small_room = Sala()
        botton.clicked.connect(lambda: self.room.metodonuevo(
            self.room))


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(453, 413)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 220, 101, 20))
        self.label_2.setObjectName("label_2")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 50, 181, 131))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(90, 290, 111, 16))
        self.label_3.setProperty("isHidden", False)
        self.label_3.setObjectName("label_3")
        # self.lineEdit.returnPressed.connect(self.random_func)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Ingrese Ususario:"))
        self.label.setText(_translate("Dialog", "Song Pop"))
        self.label_3.setText(_translate("Dialog", "__fill__"))


def Start():
    Dialog = MyStart()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    # Dialog.__dict__.update({"func": start_session})
    # Dialog.connect_func()
    return Dialog
