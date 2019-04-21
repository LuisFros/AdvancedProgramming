__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime

"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def log(clase, archivo=False):
    if not archivo:  # Se hace este paso para no sobreescribir el txt
        tipo = "w"
    else:
        tipo = "a"
    with open("logs.txt", tipo, encoding="utf-8") as salida:
        archivo = True
        metodos = [getattr(clase, el) for el in dir(clase) if "_" not in el]
        for metodo in metodos:
            def imprimir_log(args, kwargs):
                titulo = datetime.now() + "-" + str(metodo) + " :"
                a = ""
                print(args)
                a = map(str, args).split(",")
                k = ""
                kw = list(map(lambda key: str(key) - str(kwargs[key]), kwargs))
                for i in kw:
                    k += i
                print(titulo + a + k, file=salida)

            setattr("clase", imprimir_log)
    return clase


def verificar_transferencia(clase):
    transferir_error = getattr(clase, "transferir")

    def metodo_nuevo(self, origen, destino, monto, clave):
        if (
            origen.numero and destino.numero) in self.cuentas.keys():  # Verificar que las cuentas existen
            if origen.clave == clave:
                if origen.saldo <= monto:
                    transferir_error(origen, destino, monto, clave)
                raise ("Saldo insuficiente")
            raise ("Clave invalida")
        elif origen.numero not in self.cuentas.keys():
            raise AssertionError("Cuenta origen no existe")
        else:
            raise AssertionError("Cuenta destino no existe")

    setattr(clase, "transferir", nuevo_metodo)
    return clase


def verificar_inversion(clase):
    inversion_error = getattr(clase, "invertir")

    def nuevo_metodo(self, cuenta, monto, clave):
        if cuenta in self.cuentas.keys():
            if self.cuentas[cuenta].clave == clave:
                if self.cuentas[cuenta].saldo >= monto:
                    if self.cuentas[cuenta].inversiones < 10000000:
                        inversion_error(self, cuenta, monto, clave)
                    raise AssertionError(
                        "Tus inversiones excede los 10,000,000")
                raise AssertionError("Saldo insuficiente")
            raise AssertionError("Clave invalida")

    setattr(clase, "invertir", nuevo_metodo)
    return clase


def verificar_saldo(clase):
    saldo_error = getattr(clase, "saldo")

    def nuevo_metodo(self, numero_cuenta):
        if numero_cuenta in self.cuentas.keys():
            return self.cuentas[numero_cuenta].saldo
        else:
            raise AssertionError("Cuenta destino no existe")

    setattr(clase, "saldo", nuevo_metodo)
    return clase


def verificar_cuenta(clase):
    crear_error = getattr(clase, "crear_cuenta")

    def nuevo_metodo(self, nombre, rut, clave, numero, saldo_inicial=0):
        if numero not in self.cuentas.keys():
            if len(clave) == 4:
                temp = rut
                sin_guion = temp.replace("-", "")
                copia = [
                    caracter for caracter in sin_guion if
                    caracter in "0123456789"]
                # Se verifca si son numeros
                if rut.count("-") == 1 and sin_guion == "".join(copia):
                    print("Cuenta creada correctamente")
                    crear_error(self, nombre, rut, clave,
                                numero, saldo_inicial)
                else:
                    raise AssertionError("Rut invalido, tiene mas de un guion")
        else:
            while True:
                nueva_cuenta = Banco.crear_cuenta()
                if nueva_cuenta not in self.cuentas.keys():
                    nuevo_metodo(self, nombre, rut, clave,
                                 nueva_cuenta, saldo_inicial)
                    break

    setattr(clase, "crear_cuenta", nuevo_metodo)
    return clase


"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""


@log
@verificar_inversion
@verificar_saldo
@verificar_cuenta
class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    try:
        bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())
    except AssertionError as error:
        print("Error", error)

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")

    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")

    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")

    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
