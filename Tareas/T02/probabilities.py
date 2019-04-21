from random import randint


class Probabilidades:
    """docstring for (Probabilidaes)"""

    def __init__(self):
        pass

    @staticmethod
    def prob_contagio_propio(Pais):
        infectadas = (randint(0, 6)) / 6
        return infectadas

    @staticmethod
    def prob_muerte(Pais):
        tiempo = ((Pais.dias_infectado**2) / 100000)
        if tiempo > 0.2:  # Se cambio el enunciado
            if tiempo * Pais.infeccion.mortalidad < 1:
                prob = tiempo * Pais.infeccion.mortalidad
            else:
                prob = 1
        elif 0.2 * Pais.infeccion.mortalidad < 1:
            prob = 0.2 * Pais.infeccion.mortalidad
        else:
            prob = 1
        return prob

    @staticmethod
    def prob_contagio_paises(Pais):
        if Pais.fronteras_abiertas:
            conexiones_tierra = Pais.conexiones_terrestres
        else:
            conexiones_tierra = []
        if Pais.aeropuertos_abiertos:
            conexiones_aereas = Pais.conexiones_aereas
        else:
            conexiones_aereas = []
        if Pais.poblacion_viva == 0:
            valor = 1
        else:
            valor = ((Pais.poblacion_infectada + Pais.poblacion_muerta) * 0.07) / ((Pais.poblacion_viva +
                                                                                    Pais.poblacion_infectada) * (len(conexiones_aereas) + len(conexiones_tierra)))
        if valor < 1:
            prob = valor
        else:
            prob = 1
        return prob

    @staticmethod
    def se_puede_tierra(Pais):
        total = Pais.poblacion_viva + Pais.poblacion_infectada + Pais.poblacion_muerta
        tasa_infectados = (Pais.poblacion_infectada +
                           Pais.poblacion_muerta) / total
        if tasa_infectados >= 0.2:
            return True
        else:
            return False

    @staticmethod
    def se_puede_aire(Pais):
        total = Pais.poblacion_viva + Pais.poblacion_infectada + Pais.poblacion_muerta
        tasa_infectados = (Pais.poblacion_infectada +
                           Pais.poblacion_muerta) / total
        if tasa_infectados >= 0.04:
            return True
        else:
            return False

    @staticmethod
    def prob_descubrimiento(poblacion_infectada, visibilidad, poblacion_muerta, poblacion_incial):
        a = (Mundo.poblacion_infectada * Mundo.infeccion.visibilidad) * \
            (Mundo.poblacion_muerta)**2 / (Mundo.poblacion_incial)
        return a

    @staticmethod
    def progreso_cura(Mundo):

        pass

    @staticmethod
    def prob_curarse(Infeccion):
        pass
