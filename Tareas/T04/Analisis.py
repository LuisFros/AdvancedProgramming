from csv import reader
import numpy as np

a = np.array([["a", "b"], ["c", "d"]])

print(a)


class Escenario:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def instanciar_escenerarios():
    escenarios = {}
    with open("escenarios.csv", "r") as archivo:
        lista = list(reader(archivo))
        # Se hace una version transpuesta de escenarios.csv para instanciar los
        # objetos de manera mas sencilla
        transpuesta = list(zip(*lista))
        header = [col.split(":")[0] for col in transpuesta[0]]
        for i in range(1, len(transpuesta)):
            esc = Escenario(**{header[j]: transpuesta[i][j] for j in range(len(
                transpuesta[0]))})
            escenarios[i] = esc
    return escenarios
