import numpy as np

def generador_mov(start, end):
    i = start
    while True:
        if i > end:
            i = start
        else:
            yield i
            i += 1

def direction(a, b):
    x = b[0] - a[0]
    y = b[1] - a[1]
    vect = np.array((x, y))
    norm = np.linalg.norm(vect)
    return (x / norm, y / norm)


def counter(start=0, step=1):
    n = start
    while True:
        yield n
        n += step



def distancia(origen, destino):
    x = destino[0] - origen[0]
    y = destino[1] - origen[1]
    vect = np.array((x, y))
    return np.linalg.norm(vect)
