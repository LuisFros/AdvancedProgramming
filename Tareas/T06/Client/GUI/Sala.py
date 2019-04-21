# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sala.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QTableView, QTableWidget, QTableWidgetItem
import time


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(874, 805)
        self.Timer = QtWidgets.QLCDNumber(Form)
        self.Timer.setGeometry(QtCore.QRect(20, 20, 191, 111))
        self.Timer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Timer.setSmallDecimalPoint(False)
        self.Timer.setDigitCount(2)
        self.Timer.setProperty("intValue", 20)
        self.Timer.setObjectName("Timer")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 190, 200, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        # data = {'Sala': ["A", "B", "C"], 'Usuarios': ['4',
        #                                               '5',
        #                                               '6'],
        #         'Tiempo': ['20', '20', '20']}
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "P1"))
        self.pushButton_2.setText(_translate("Form", "P2"))
        self.pushButton_3.setText(_translate("Form", "P3"))
        self.pushButton_4.setText(_translate("Form", "P4"))


def Sala():
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    data = {'1-Usuario': ['A', 'B', 'C'],
            '3-Tiempo': ['20', '20', '20'], '2-Resultado': ['', '', '']}
    Form.table = MyTable(data, 5, 3, Form)
    return Form


class MyTable(QTableWidget):
    def __init__(self, data, a, b, parent):
        QTableWidget.__init__(self, a, b, parent)
        self.data = data
        self.setGeometry(QtCore.QRect(300, 50, 380, 250))
        self.setmydata()
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def setmydata(self, data=None):
        if data is not (None):
            self.data = data
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

    def play(self):
        aux = Qt.QSound("temp.wav", self)
        aux.play()
        if aux.isFinished():
            time.sleep(1)

# if __name__ == '__main__':
#     import sys
#
#     app = QtWidgets.QApplication([])
#     a = Sala()
#     a.show()
#     a.table.data = {}
#     sys.exit(app.exec_())
