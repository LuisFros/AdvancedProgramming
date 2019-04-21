from Client.main_client import Client
from PyQt5 import QtWidgets
import sys
from Start import Start


def start_session(usuario=None):
    PORT = 8080
    HOST = "localhost"
    aux = Client(PORT, HOST)
    return aux


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    def catch_exceptions(t, val, tb):
        print(t, val)
        old_hook(t, val, tb)


    old_hook = sys.excepthook
    sys.excepthook = catch_exceptions

    a = Start()
    # a.cliente = start_session()
    a.connect_func(start_session())
    a.show()

    sys.exit(app.exec_())
