from csv import reader
from random import random, expovariate, uniform, randint, choice
from statistics import mean
from math import ceil
from Funcional import nota_esperada_horas, evaluar_evento
import numpy as np
from Analisis import instanciar_escenerarios


class DiccNotas(dict):
    @property
    def promedio(self):
        if len(self.values()) > 0:
            return mean(self.values())
        return 0


class Alumno:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.botar_ramo = False
        Alumno.creditos(self)
        self.calcular_horas_dedicadas()
        self.personalidad = choice(["Eficiente", "Artistico", "Teorico"])
        self.tip_semanal = False
        self.bonus_profesor = False
        self.notas_tareas = DiccNotas()
        self.notas_esperadas_tareas = DiccNotas()
        self.notas_controles = DiccNotas()
        self.notas_esperadas_con = DiccNotas()
        self.notas_actividades = DiccNotas()
        self.notas_esperadas_act = DiccNotas()
        self.reuniones_profe = list()
        self.fiestas = []
        dificultad = {0: 2, 1: 2, 2: 3, 3: 5, 4: 7, 5: 10, 6: 7, 7: 9, 8: 1,
                      9: 6,
                      10: 6,
                      11: 5}
        self.manejo_contenidos = {i: 1 / dificultad[i] * self.horas_catedra(
            i + 1) for i in range(12)}
        # Formato diccionarios->{dia:(Nota final,Nota Esperada)}

    def __repr__(self):
        return "Alumno: {}, Secion: {}".format(self.Nombre, self.Seccion)

    @property
    def nivel_programacion(self):
        return self._nivel_programacion

    @nivel_programacion.setter
    def nivel_programacion(self, semana):
        if semana <= 1:
            self._nivel_programacion = uniform(2, 12)
        else:
            if semana in self.fiestas:
                fiesta = 0.15
            else:
                fiesta = 0

            if semana in self.reuniones_profe:
                reunion = 0.08
            else:
                reunion = 0
            factor = (1 + reunion - fiesta)
            self._nivel_programacion = self.nivel_programacion * (1.05) * \
                                       factor

    @staticmethod
    def creditos(self):
        prob = uniform(0, 1)
        if prob <= 0.1:
            self.creditos = 40
        elif 0.8 >= prob > 0.1:
            self.creditos = 50
        elif 0.8 < prob <= 0.95:
            self.creditos = 55
        else:
            self.creditos = 60

    @property
    def confianza(self):
        return abs(self._confianza)

    @confianza.setter
    def confianza(self, dia):
        if dia <= 1:
            self._confianza = uniform(2, 12)
        else:
            self._confianza = self._confianza + self.confianza_notas(dia)

    def confianza_notas(self, dia):
        dia -= 1
        # Formula= 3x+5y+z
        x, y, z = (0, 0, 0)
        if dia in self.notas_actividades:
            # Se asuma una tupla tipo (nota final,nota esperada)
            x = (
                self.notas_actividades[dia] -
                self.notas_esperadas_act[dia])
        if dia in self.notas_tareas:
            y = (self.notas_tareas[dia] - self.notas_esperadas_tareas[dia])
        if dia in self.notas_controles:
            z = (self.notas_controles[dia] - self.notas_esperadas_con[dia])

        return 3 * x + 5 * y + z

    def calcular_horas_dedicadas(self):
        horas = {40: (10, 25), 50: (10, 15), 55: (5, 15), 60: (5, 10)}
        self.horas_dedicadas = uniform(horas[self.creditos][0], horas[
            self.creditos][1]) * 15  # 15 por el numero de semanas maximo

    def horas_tareas(self, semana):
        return 0.7 * self.horas_dedicadas * semana / 15

    def horas_catedra(self, semana):
        return 0.7 * self.horas_dedicadas * semana / 15

    @property
    def promedio(self):
        return (self.notas_actividades.promedio + self.notas_controles.promedio
                + self.notas_tareas.promedio) / 3

    @property
    def necesita_consulta(self):
        if self.promedio <= 5.0 or random() <= 0.2:
            return True
        return False


    def resetear_booleanos(self):
        for atributo in self.__dict__:
            if isinstance(self.__dict__[atributo], bool):
                self.__dict__.update({str(atributo): False})

    # Posiblemente un properry que cuando tenga 4 actividades que calcule
    def se_bota_ramo(self):
        if (self.confianza * 0.8 + self.promedio * 0.2) < 2:
            # print("{} ha decidido botar el ramo :( ".format(self))
            self.botar_ramo = True

    def actualizar_reuniones(self, semana):
        # print('El alumno {},se reune con su profesor en la semana {}'.format(
        #     self.Nombre, semana))
        self.reuniones_profe.append(semana)


class Ayudante:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.contenidos = list()
        for i in range(3):
            self.contenidos.append(randint(0, 12))

    def entregar_notas(self):
        print(" {}(Ayudante) ha entregado las notas".format(self.Nombre))


class Profesor:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.alumnos = []
        self.agenda = {i: [] for i in range(1, 100)}
        self.elegidos = {i: [] for i in range(1, 100)}
        self.capacidad = 10
        self.cortes_agua = {}

    def llenar_agenda(self, alumno, semana):
        self.agenda[semana].append(alumno)

    def elegir(self, semana, lista_eventos):
        capacidad = self.capacidad
        if (semana, "Corte Agua") in lista_eventos:
            capacidad = 6
        if semana in self.agenda:
            if len(self.agenda[semana]) >= capacidad:
                elegidos = np.random.choice(self.agenda[semana], capacidad)
            else:
                elegidos = self.agenda[semana]
            return elegidos
        else:
            return None

    def __repr__(self):
        return "Profesor: {} ,Seccion: {}".format(self.Nombre, self.Seccion)


class Simulacion:
    def __init__(self,escenario=None):
        self.lista_eventos = []
        self.ayudantes = []
        self.alumnos = []
        self.profesores = {}
        self.instanciar_ramo()
        self.semana = 1
        self.exigencias_c = {}
        self.exigencias_t = {}

    def instanciar_ramo(self):
        with open("integrantes.csv", "r", encoding="utf-8") as archivo:
            lector = [i for i in reader(archivo)]
            # Nombre:string,Rol:string,Sección:string
            lector[0][0] = lector[0][0].split(":")[0]
            lector[0][2] = lector[0][2].split(":")[0]
            for i in range(1, len(lector)):
                if lector[i][1] == "Docencia":
                    ay = Ayudante(
                        **{lector[0][0]: lector[i][0], "Tipo": "Docencia"})
                    self.ayudantes.append(ay)
                elif lector[i][1] == "Tareas":
                    ay = Ayudante(
                        **{lector[0][0]: lector[i][0], "Tipo": "Tareas"})
                    self.ayudantes.append(ay)
                elif lector[i][1] == "Profesor":
                    prof = Profesor(**{lector[0][0]: lector[i][0],
                                       "Seccion": lector[i][2]})
                    self.profesores[lector[i][2]] = prof
                elif lector[i][1] == "Alumno":
                    al = Alumno(**{lector[0][0]: lector[i][0], "Seccion":
                        lector[i][2]})
                    # Se inician los setter
                    al.nivel_programacion = 1
                    al.confianza = 1
                    self.alumnos.append(al)
                else:
                    # Instanciar Dr.Mavrakis!
                    pass

    def agregar_evento(self, tupla):
        self.lista_eventos.append(tupla)

    def run(self):
        tiempo = 0
        self.todos = []
        self.llenar_catedra()
        self.llenar_ayudantia()
        self.iniciar_tareas()
        self.dia = 0
        self.no_programados()
        self.lista_eventos.sort(key=lambda x: x[0])
        while len(self.lista_eventos) > 0:
            if len(self.alumnos) == 0:
                print("Curso esta vacio")
                break
            self.dia, evento = self.lista_eventos[0]
            evaluar_evento(evento, self)
            print("Evento: {} - Dia: {}".format(evento, self.dia))
            if ceil(self.dia / 7) > self.semana:
                # Decisiones semanales
                self.decisiones_profesores(self.semana)

                self.decisiones_alumnos(self.semana)

                self.actualizar_alumnos(self.semana)
                self.semana = ceil(self.dia / 7)
                # self.estadisticas()
            # Revisar los que botaron el ramo
            if self.semana == 6:
                self.sweep()
            self.lista_eventos = self.lista_eventos[1:]
            if self.semana >= 15:
                break

            self.lista_eventos.sort()

    def estadisticas_finales(self):

        pass

    def sweep(self):
        self.todos += list(filter(lambda x: x.botar_ramo == True,
                                  self.alumnos))
        self.alumnos = list(filter(lambda x: x.botar_ramo == False,
                                   self.alumnos))

    def iniciar_tareas(self):
        self.lista_eventos.append((13, "Reunion Tarea"))
        self.lista_eventos.append((14, "Tarea"))

    def actualizar_alumnos(self, semana):
        for alumno in self.alumnos:
            alumno.calcular_horas_dedicadas()
            alumno.confianza = semana
            alumno.nivel_programacion = semana

    def llenar_catedra(self):
        controles = []
        for i in range(4, 81, 7):
            self.agregar_evento((i, "Catedra"))
            controles.append(i)

        dias_controles = [4, 11, 25, 32, 60]
        for dia in dias_controles:
            self.agregar_evento((dia, "Control"))
        for i in range(3, 80, 7):
            self.agregar_evento((i, "Reunion Catedra"))
            # Para hacerlo mas realista, se supone que la reunion de la catedra
            # Se realiza un dia antes

    def llenar_ayudantia(self):
        for i in range(2, 79, 7):
            self.agregar_evento((i, "Ayudantia"))

    def no_programados(self):
        for i in range(3):
            self.agregar_evento((round(expovariate(1 / 30)), "Fiesta"))  # Dias
            self.agregar_evento((round(expovariate(1 / 70)), "Futbol"))
            self.agregar_evento((round(expovariate(1 / 21)), "Corte Agua"))

    def decisiones_alumnos(self, semana):
        for alumno in self.alumnos:
            if alumno.necesita_consulta:
                self.profesores[alumno.Seccion].llenar_agenda(alumno, semana)

    def decisiones_profesores(self, semana):
        for profesor in self.profesores:
            favoritos = list(self.profesores[profesor].elegir(semana,
                                                              self.lista_eventos))
            if len(favoritos) > 0:
                for al in favoritos:
                    al.actualizar_reuniones(semana)


if __name__ == '__main__':
    # start=time()
    a = Simulacion()
    a.run()
    # Con los valores por default del enunciado, los alumnos terminan botando
    # el ramo por lo que se deben acceder de esta manera
    alumnos = a.todos
    while True:
        a = input("Ingrese nombre alumno a analizar o escriba 'salir' para " \
                  "recibir " \
                  "estadisticas finales" \
                  ": ")
        if a != "salir":
            buscado = tuple(filter(lambda x: x.Nombre == a, alumnos))[0]
            print(buscado)
            print("Nivel Programacion: ", buscado.nivel_programacion)
            print("Confianza: ", buscado.confianza)
            print("Manejo Contenidos: ", buscado.manejo_contenidos)
            print("Promedio :", buscado.promedio)
        break
    print("Alumnos que botaron el ramo: ", len(alumnos))
    print("Promedio Confianza: ",
          mean(list(map(lambda x: x.confianza, alumnos))))
    print("")
    while True:
        a = input("'Y' para hacer analisis de resultados, 'N' para terminar")
        if a != "N":
            escenarios = instanciar_escenerarios()
            for numero in escenarios:
                a=Simulacion(escenarios[numero])
                a.run()
# TO DO
