from estructuras import Nodo, ListaLigada, ColaPrioridades
from random import randint


def buscar_entero(decimal, x=0):
    if decimal >= 1:
        return round(decimal, 0) * 10**(3)
    if decimal <= 0.001:
        return 1
    else:
        x += 1
        return buscar_entero(decimal * 10**x, x) * 10**-x


def evento_ocurra(prob):
    eventos_posibles = buscar_entero(prob)
    lista_imposible = ListaLigada()
    for vacio in range(1000):
        lista_imposible.append(None)
    for evento in range(int(eventos_posibles)):
        pos = randint(0, 999)
        lista_imposible[pos] = True
    if lista_imposible[randint(0, 999)]:
        return True
    else:
        return False
# Estas 2 primeras funciones estaran explicadas en el README, pero
# basicamente es una simulacion de probabilidad


def promedio_fronteras(grafo):  # recibe el grafo de conexiones terrestres
    promedio = 0
    for conexion in grafo.camino:
        promedio += conexion.cabeza.poblacion_infectada / \
            (conexion.cabeza.poblacion_viva + conexion.cabeza.poblacion_infectada)
    return promedio / 100
