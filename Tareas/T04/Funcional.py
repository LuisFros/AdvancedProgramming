from random import choice, uniform, triangular, shuffle, random
import numpy as np
from statistics import mean
from math import ceil


class DiccRango(dict):
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
        else:
            return super().__getitem__(item)


def nota_esperada_horas(contenido, horas):
    # 0 #
    dic_oop = {range(0, 3): uniform(1.1, 3.9), range(3, 5): uniform(4.0, 5.9),
               range(5, 7): uniform(6.0, 6.9), range(7, 99): 7.0}
    oop = DiccRango(dic_oop)
    # 1 #
    dic_her = {range(0, 4): uniform(1.1, 3.9), range(4, 7): uniform(4.0, 5.9),
               range(7, 8): uniform(6.0, 6.9), range(8, 99): 7.0}
    her = DiccRango(dic_her)
    # 2 #
    dic_listas = {range(0, 2): uniform(1.1, 3.9), range(2, 5): uniform(4.0,
                                                                       5.9),
                  range(5, 7): uniform(6.0, 6.9), range(7, 99): 7.0}
    listas = DiccRango(dic_listas)
    # 3 #
    dic_grafos = {range(0, 3): uniform(1.1, 3.9), range(3, 6): uniform(4.0,
                                                                       5.9),
                  range(6, 8): uniform(6.0, 6.9), range(8, 99): 7.0}
    grafos = DiccRango(dic_grafos)
    # 4 #
    dic_funcional = {range(0, 4): uniform(1.1, 3.9), range(4, 8): uniform(4.0,
                                                                          5.9),
                     range(8, 9): uniform(6.0, 6.9), range(9, 99): 7.0}
    funcional = DiccRango(dic_funcional)
    # 5 #
    dic_metaclases = {range(0, 5): uniform(1.1, 3.9), range(5, 8): uniform(4.0,
                                                                           5.9),
                      range(8, 10): uniform(6.0, 6.9), range(10, 99): 7.0}
    metaclases = DiccRango(dic_metaclases)
    # 6 #
    dic_simulacion = {range(0, 4): uniform(1.1, 3.9), range(4, 7): uniform(4.0,
                                                                           5.9),
                      range(7, 9): uniform(6.0, 6.9), range(9, 99): 7.0}
    simulacion = DiccRango(dic_simulacion)
    # 7 #
    dic_threading = {range(0, 3): uniform(1.1, 3.9), range(3, 6): uniform(4.0,
                                                                          5.9),
                     range(6, 8): uniform(6.0, 6.9), range(8, 99): 7.0}
    threading = DiccRango(dic_threading)
    # 8 #
    dic_gui = {range(0, 2): uniform(1.1, 3.9), range(2, 5): uniform(4.0,
                                                                    5.9),
               range(5, 7): uniform(6.0, 6.9), range(7, 99): 7.0}
    gui = DiccRango(dic_gui)
    # 9 #
    dic_bytes = {range(0, 5): uniform(1.1, 3.9), range(5, 8): uniform(4.0,
                                                                      5.9),
                 range(8, 10): uniform(6.0, 6.9), range(10, 99): 7.0}
    bytes_1 = DiccRango(dic_bytes)
    # 10 #
    dic_net = {range(0, 3): uniform(1.1, 3.9), range(3, 6): uniform(4.0,
                                                                    5.9),
               range(6, 8): uniform(6.0, 6.9), range(8, 99): 7.0}
    net = DiccRango(dic_net)
    # 11 #
    dic_web = {range(0, 3): uniform(1.1, 3.9), range(3, 8): uniform(4.0,
                                                                    5.9),
               range(8, 9): uniform(6.0, 6.9), range(9, 99): 7.0}
    web = DiccRango(dic_web)
    # Se instancio el objeto antes para que el codigo sea mas legible
    nota_esperada = {0: oop, 1: her, 2: listas, 3: grafos,
                     4: funcional, 5: metaclases, 6: simulacion,
                     7: threading, 8: gui, 9: bytes_1, 10: net,
                     11: web}
    aproximado = round(horas)

    if nota_esperada[contenido][aproximado] == None:
        return 7.0
    else:
        return nota_esperada[contenido][aproximado]


def moneda(alumno):
    alumno.tip_semanal = choice([True, False])
    return alumno


def dudas(alumno):
    numero = triangular(1, 10, 3)
    alumno.dudas = numero
    return alumno


def formula(x, y, z, manejo_contenido, nivel_programacion,
            confianza):
    main_f = x * manejo_contenido + y * nivel_programacion + z * confianza
    return main_f


def actividad(alumno, semana, exigencia):
    contenido = semana - 1
    alumno.confianza = semana
    alumno.nivel_programacion = semana
    pep_8 = formula(0.7, 0.2, 0.1, alumno.manejo_contenidos[contenido],
                    alumno.nivel_programacion, alumno.confianza)
    func = formula(0.3, 0.6, 0.1, alumno.manejo_contenidos[contenido],
                   alumno.nivel_programacion, alumno.confianza)
    contenidos = pep_8
    progreso_total = (0.4 * func + 0.4 * contenidos +
                      0.2 * pep_8)
    alumno.notas_actividades[contenido] = max([progreso_total / exigencia, 1])
    alumno.notas_esperadas_act[contenido] = nota_esperada_horas(contenido,
                                                                alumno.horas_catedra(
                                                                    semana))
    if contenido == 3:
        # Se revisa si debe botar el ramo
        alumno.se_bota_ramo()
        # Se revisa si adquiere bonus

    elif (contenido == 4 or contenido == 7) and alumno.personalidad == \
            "Eficiente":
        alumno.notas_actividades[contenido] += 1

    elif (contenido == 11 or contenido == 8) and \
                    alumno.personalidad == "Artistico":
        alumno.notas_actividades[contenido] += 1
    elif contenido == 5 and alumno.personalidad == "Teorico":
        alumno.notas_actividades[contenido] += 1

    return alumno


def catedra(simulacion):
    semana = simulacion.semana
    contenido = semana - 1
    # Se simula los que escuchan el tip en la catedra
    simulacion.alumnos = list(map(lambda x: moneda(x), simulacion.alumnos))
    # Se simula el numero de dudas que tendra cada alumno en la catadra
    simulacion.alumnos = list(map(lambda x: dudas(x),
                                  simulacion.alumnos))
    for seccion in simulacion.profesores.keys():  # Recorrer el numero de
        # secciones ya que pueden ser mas de 3! (Issue)
        temp = list(
            filter(lambda x: x.Tipo == "Docencia", simulacion.ayudantes))
        revuelto_main = list(filter(lambda x: x.Seccion == seccion,
                                    simulacion.alumnos))
        shuffle(revuelto_main)
        for i in range(3):
            total = 0
            revuelto = revuelto_main
            while total <= 200 and len(revuelto) > 0:
                revuelto[0].manejo_contenidos[semana] *= 1.01
                total += revuelto[0].dudas
                revuelto = revuelto[1:]

    # Se simula el progreso de cada alumno en la actividad
    simulacion.alumnos = list(map(lambda x: actividad(x, semana,
                                                      simulacion.exigencias_c[
                                                          contenido]),
                                  simulacion.alumnos))
    a = list(map(lambda x: x.notas_actividades[contenido], simulacion.alumnos))
    print("Se entrego la actividad {} con nota promedio {}".format(contenido,
                                                                   mean(a)))


def reunion_c(simulacion):
    dificultad = {0: 2, 1: 2, 2: 3, 3: 5, 4: 7, 5: 10, 6: 7, 7: 9, 8: 1,
                  9: 6,
                  10: 6,
                  11: 5}
    actividad_nro = simulacion.semana - 1
    # El numero de semanas y contenidos esta desfazado por 1
    exigencia = 7 + (uniform(1, 5)) / (dificultad[actividad_nro])
    simulacion.exigencias_c[actividad_nro] = exigencia


def tareas(alumno, semana, exigencia):
    contenido = semana - 1
    alumno.nivel_programacion = semana
    pep_8 = 0.5 * alumno.horas_tareas(semana) + 0.5 * alumno.nivel_programacion
    con = 0.7 * alumno.manejo_contenidos[
        contenido] + 0.1 * alumno.nivel_programacion + 0.2 * alumno.horas_tareas(
        semana)
    func = 0.5 * alumno.manejo_contenidos[
        contenido] + 0.1 * alumno.nivel_programacion + 0.4 * alumno.horas_tareas(
        semana)

    progreso_total = (0.4 * func + 0.4 * con +
                      0.2 * pep_8)
    alumno.progreso_tarea = progreso_total / exigencia
    alumno.notas_actividades[contenido] = max([progreso_total / exigencia, 1])
    return alumno


def entrega_tarea(simulacion):
    tarea = ceil((simulacion.semana) * 7 / 14) - 1
    simulacion.alumnos = list(map(lambda x: tareas(x, simulacion.semana,
                                                   simulacion.exigencias_t[
                                                       tarea]),
                                  simulacion.alumnos))
    print("{} alumnos entregaron la tarea {} en la semana {}".format(len(
        simulacion.alumnos), tarea, simulacion.semana))

    menor_50 = list(
        filter(lambda x: x.progreso_tarea <= 0.5, simulacion.alumnos))
    if len(menor_50) / len(simulacion.alumnos) >= 0.8 and random() <= 0.2:
        print("Se decide dar dos dias mas de plazo en la tarea {}".format(
            tarea))
        simulacion.lista_eventos.append((simulacion.dia + 2, "Entrega Tarea"))
        simulacion.lista_eventos.append((simulacion.dia + 16, "Reunion Tarea"))
    else:
        tupla = ((simulacion.semana + 2) * 7, "Reunion Tarea")
        simulacion.lista_eventos.append(tupla)


def reunion_t(simulacion):
    bool = (ceil(simulacion.dia / 7) > ceil((simulacion.semana) * 7 / 14))
    if bool:
        dificultad = {0: 2, 1: 2, 2: 3, 3: 5, 4: 7, 5: 10, 6: 7, 7: 9, 8: 1,
                      9: 6,
                      10: 6,
                      11: 5}
        tarea = ceil((simulacion.semana) * 7 / 14)
        # El numero de semanas y contenidos esta desfazado por 1
        actual = (simulacion.semana - 1)
        anterior = actual - 1
        exigencia_actual = 7 + (uniform(1, 5) / dificultad[actual])
        exigencia_anterior = 7 + (uniform(1, 5) / dificultad[anterior])
        exigencia = mean([exigencia_actual, exigencia_anterior])
        simulacion.exigencias_t[tarea] = exigencia
        simulacion.lista_eventos.append(((simulacion.semana + 2) * 7,
                                         "Entrega Tarea"))


def corte_agua(simulacion):
    pass


def fiesta(simulacion):
    if len(simulacion.alumnos) > 0:
        van_fiesta = list(np.random.choice(simulacion.alumnos, 50))
        for alumno in van_fiesta:
            alumno.fiestas.append(simulacion.semana)


def bonus_ayudantia(alumno, semana):
    alumno.manejo_contenidos[semana] *= 1.1
    return alumno


def ayudantia(simulacion):
    ayudantes = list(
        filter(lambda x: x.Tipo is "Docencia", simulacion.ayudantes))
    primero = choice(ayudantes)
    semana = simulacion.semana
    # Se elige 2 ayudantes de docencia la azar
    while True:
        segundo = choice(ayudantes)
        if segundo != primero:
            break
    contenidos = primero.contenidos + segundo.contenidos
    print("{} y {} dictan ayudantia # {}".format(primero.Nombre, segundo.Nombre,
                                                 semana))
    if semana in contenidos:  # Si los ayudantes manejan los contenidos
        simulacion.alumnos = list(map(lambda x: bonus_ayudantia(x, semana),
                                      simulacion.alumnos))


def futbol(simulacion):
    pass


def fin_semana(dia):
    dias_restantes = 7 - dia
    dias_pasados = dia - 1
    return dias_pasados, dias_restantes


def progreso_control(alumno, semana, exigencias):
    contenido = semana - 1
    alumno.nivel_programacion = semana
    alumno.confianza = semana
    con = 0.7 * alumno.manejo_contenidos[
        contenido] + 0.05 * alumno.nivel_programacion + 0.25 * alumno.confianza
    func = 0.3 * alumno.manejo_contenidos[
        contenido] + 0.2 * alumno.nivel_programacion + 0.5 * alumno.confianza
    progreso_total = 0.7 * con + 0.3 * func
    numero = len(alumno.notas_controles) + 1
    alumno.notas_esperadas_con[numero] = nota_esperada_horas(contenido,
                                                             alumno.horas_catedra(
                                                                 semana))
    alumno.notas_controles[numero] = max([
        progreso_total / exigencias[contenido], 1])

    return alumno


def control(simulacion):
    simulacion.alumnos = list(map(lambda x: progreso_control(x,
                                                             simulacion.semana,
                                                             simulacion.exigencias_c),
                                  simulacion.alumnos))


def evaluar_evento(evento, simulacion):
    # Eliminar esta condicion, es una prueba!
    eventos = {"Catedra": catedra, "Reunion Catedra": reunion_c,
               "Reunion Tarea": reunion_t,
               "Ayudantia": ayudantia, "Fiesta": fiesta,
               "Futbol": futbol,
               "Corte Agua": corte_agua, "Tarea": futbol, "Entrega Tarea":
                   entrega_tarea, "Control": control}
    return eventos[evento](simulacion)
