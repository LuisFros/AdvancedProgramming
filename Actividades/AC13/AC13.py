import os
from json import load, dump, JSONEncoder
import pickle
import datetime
from random import randint

# Bonus: Se crea el directorio si este no existe
if not os.path.exists('secure_db'):
    os.makedirs('secure_db')
if not os.path.exists('secure_db/msg'):
    os.makedirs('secure_db/msg')
if not os.path.exists('secure_db/usr'):
    os.makedirs('secure_db/usr')


class Usuario:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class Mensaje:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


def conversion():
    usuarios = os.listdir("db/usr/")
    mensajes = os.listdir("db/msg/")
    diccionario_contactos = {}
    diccionario_mensajes = {}
    for user in usuarios:
        with open("db/usr/{}".format(user), "r") as file:
            temp = load(file, object_hook=lambda dict: Usuario(**dict))
            diccionario_contactos[temp.phone_number] = temp
    for msg in mensajes:
        with open("db/msg/{}".format(msg), "r") as file:
            temp = load(file, object_hook=lambda dict: Mensaje(**dict))
            # temp = Mensaje(**load(file))
            diccionario_mensajes[(temp.send_by, temp.send_to)] = temp

    return diccionario_contactos, diccionario_mensajes


def relacionar(dic_numeros, dic_mensajes):
    for numero in dic_numeros:
        for tupla in dic_mensajes:
            if numero in tupla:
                if tupla.index(numero) == 0 and tupla[1] not in dic_numeros[
                    numero].contacts:
                    dic_numeros[numero].contacts.append(tupla[1])


def escribir_user_json(dict):
    for number in dict:
        with open('secure_db/usr/{}.json'.format(dict[number].name), "w") as \
                user:
            dump(dict[number].__dict__, user)

            # Retorna un diccionario, pero hacer dict.values() es una lista de los objetos!
            # Como el enunciado decia lista, no busco descuentos


class EncodedMesage:
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __getstate__(self):
        nueva = self.__dict__.copy()
        # Se omiten los characteres que no son del alfabeto
        old = nueva["content"]
        sent_by = nueva["send_by"]
        limpia = ""
        for string in old:
            if string.isalpha():
                limpia += string

        def ceaser(string, n):
            new = ""
            for i in string:
                y = (ord(i.lower()) - 97 + n) % 26
                new += chr(y + 97)
            return new

        nueva.update({"content": ceaser(limpia, sent_by)})
        return nueva

    def __setstate__(self, state):
        time = datetime.datetime.now()
        state.update(
            {"last_view_date": "{0.hour}:{0.minute} {0.day}/{0.month}/{"
                               "0.year}".format(time)})
        self.__dict__ = state

    def __repr__(self):
        return self.content


def get_name(obj):#Se creo un id unico con el largo del mensaje
    return obj.send_by*len(obj.content)


def escribir_msg_pickle(dict):
    for message in dict:
        name = get_name(dict[message])
        with open("secure_db/msg/{}".format(name), "wb") as dumped:
            diccionario = dict[message].__dict__
            obj = EncodedMesage(**diccionario)
            pickle.dump(obj, dumped)


def main():
    diccionario_numeros, diccionario_mensajes = conversion()
    relacionar(diccionario_numeros, diccionario_mensajes)
    escribir_user_json(diccionario_numeros)
    escribir_msg_pickle(diccionario_mensajes)


def extra_comprobar():
    mensajes = os.listdir("secure_db/msg/")
    for mensaje in mensajes:
        with open("secure_db/msg/{}".format(mensaje), "rb") as file:
            objeto_final = pickle.load(file)
            print(objeto_final.last_view_date)
            print(objeto_final.content)



if __name__ == '__main__':
    main()
    # extra_comprobar() Esta funcion esta para que se puedan leer los
    # mensajes! (extra)
