import json
import pickle
from random import choice
import os
from PyQt5.Qt import QSound
import time
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton)


def get_salas():
        return os.listdir(os.getcwd())


def retrieve_data():
    other, base = starting_values()
    print(base)
    with open(base) as file:
        return json.load(file)


def rewrite_data(data, base):
    with open(base, 'w') as file:
        json.dump(data, file)


def ingresar_usuario(nombre):
    current = retrieve_data()
    print("Ingresado", nombre)
    base_pickle, base_usuarios = starting_values()
    if nombre in current:
        return current[nombre]
    else:
        # Eventualmente agregar los desafios aca
        current.update({nombre: 0})
        rewrite_data(current, base_usuarios)
        return current[nombre]


def reset_data():
    with open("Data/user.json", 'w') as file:
        json.dump({}, file)
        # reset_data()


def get_bytes(direccion):
    with open(direccion, 'rb') as file:
        head = bytearray(file.read(44))
        other = bytearray(file.read())
    return head, other


def starting_values():
    base_usuarios = "{}\\Data\\users.json".format(os.getcwd())
    base_pickle = "{}\\Data\\musica".format(os.getcwd())

    if not (os.path.exists(base_usuarios)):
        with open(base_usuarios, 'w') as file:
            data = {}
            json.dump(data, file)
    return base_pickle, base_usuarios


def save_songs(sala_pedida):
    base_pickle, base_usuarios = starting_values()
    print("Se ha pedido la sala", sala_pedida)
    for sala in get_salas():
        string_sala = "{}\{}".format(os.getcwd(), sala)
        # Esta linea depende de la decision si se guardan los archivos o se
        # mandan de manera dinamica (ojala dinamica)
        # if not (os.path.exists("{}_{}".format(base_pickle, sala))):
        dic = {}
        if sala == sala_pedida:
            if sala != "Data" and sala != "__pycache__" and os.path.isdir(
                    string_sala):
                # with open("{}_{}".format(base_pickle, sala), 'wb') as file:
                for cancion in os.listdir(string_sala):
                    dic[cancion] = {}
                    header, body = get_bytes(
                        "{}\{}".format(string_sala, cancion))
                    dic[cancion]["header"] = header
                    dic[cancion]["body"] = body
                return dic


def reproducir(parent, cancion_1='Bruno Mars - 24K Magic.wav'):
    with open("resultado.wav", "wb") as result:
        for sala in get_salas():
            string_sala = "{}\{}".format(os.getcwd(), sala)
            if sala != "Data" and sala != "__pycache__" and os.path.isdir(
                    string_sala):
                lista = os.listdir(string_sala)
                if cancion_1 in lista:
                    pos = lista.index(cancion_1)
                    cancion = lista[pos]
                    file = open("{}_{}".format(base_pickle, sala), "rb")
                    data = pickle.load(file)
                    head = data[cancion]["header"]
                    body = data[cancion]["body"]
                    largo = len(body)
                    largo_en_bytes = largo.to_bytes(4, byteorder='little')
                    result.write(head[0:4])
                    byterate = int.from_bytes(head[28:32], byteorder="little")
                    distancia = byterate * 20
                    largo_en_bytes_con_header = (
                        distancia + 36).to_bytes(4, byteorder='little')

                    result.write(largo_en_bytes_con_header)
                    result.write(head[8:40])
                    inicio = choice(range(0, largo - distancia, 2))
                    final = inicio + distancia
                    result.write(distancia.to_bytes(4, byteorder='little'))
                    result.write(body[inicio:final])
                    result.close()
                    break
    aux = QSound("resultado.wav", parent)
    aux.play()


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    save_songs()
    cancion = reproducir(form)
    sys.exit(app.exec_())
