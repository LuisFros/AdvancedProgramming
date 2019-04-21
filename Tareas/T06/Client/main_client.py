import threading
import socket
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QMainWindow
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QCoreApplication
import pickle
from random import choice
import sys


class Client(QObject):
    def __init__(self, port, host):
        super(Client, self).__init__()
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connect_to_server()
            self.listen()
        except:
            print("Conexión terminada")
            self.socket_cliente.close()
            exit()

    # El método connnect_to_server() creará la conexión al servidor.
    def connect_to_server(self):
        self.socket_cliente.connect((self.host, self.port))
        print("Cliente conectado exitosamente al servidor...")

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def send(self, msg):
        msg_bytes = msg.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder="little")
        self.socket_cliente.send(msg_length)
        self.socket_cliente.send(msg_bytes)

    # Se recibe del servidor la cancion, se uso un mezcla de pickle +
    # manejo de bytes
    def listen_thread(self):
        file = open("test.wav", "wb")
        while True:
            # Se recibe el largo
            response_bytes_length = self.socket_cliente.recv(4)
            largo_mensaje = int.from_bytes(response_bytes_length,
                                           byteorder="little")
            response = bytearray()
            # Se exiende el array con los bytes que contiene el mensaje
            while len(response) < largo_mensaje:
                response.extend(self.socket_cliente.recv(256))
            mensaje = pickle.loads(response)
            # Se carga el diccionario de pyckle con las 2 partes:
            # Indicando el largo de cada uno de los bytes
            largo_body = mensaje['body']
            largo_head = mensaje['header']  # (Para el de wav es 44)
            # Se recibe el encabezado
            recibir_head = self.socket_cliente.recv(largo_head)
            body = bytearray()
            # Se recibe la cancion restante
            while len(body) < largo_body:
                body.extend(self.socket_cliente.recv(16834))
            self.write_song(recibir_head, body)

    def write_song(self, head, body):
        # Dada el header y el body, se escribe en un archivo temporal
        # la cancion que se reproducera
        with open('temp.wav', 'wb') as result:
            result.write(head[0:4])
            byterate = int.from_bytes(head[28:32], byteorder="little")
            distancia = byterate * 20
            largo_en_bytes_con_header = (
                distancia + 36).to_bytes(4, byteorder='little')

            result.write(largo_en_bytes_con_header)
            result.write(head[8:40])
            # Se hace un aleatorio de los 20s que se reproduceran
            # Importante indicar que estos tiene que ser pares, por eso el 2
            inicio = choice(range(0, len(body) - distancia, 2))
            final = inicio + distancia
            result.write(distancia.to_bytes(4, byteorder='little'))
            result.write(body[inicio:final])


if __name__ == "__main__":
    app = QApplication(sys.argv)


    def catch_exceptions(t, val, tb):
        QMessageBox.critical(None,
                             "An exception was raised",
                             "Exception type: {}".format(t))
        print(t, val)
        old_hook(t, val, tb)


    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions
    sys.exit(app.exec_())
