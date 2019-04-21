from archivos import start_archivos

recursos, meteorologia, usuarios, incendios = start_archivos()


def menu_usuario():
    exit_loop = False
    functions = {"1": incendios_activos, "2": incendios_apagados, "3": recursos_mas_utilizados,
                 "4": recusos_mas_efectivos, "5": estrategia_extincion, "6": cambiar_hora}
    while not exit_loop:
        print(""" Elegir una de las suguientes opciones:
            1. Incendios asignados
            2. Incendios Apagados
            3. Recursos mas utilizados
            4. Recursos mas efectivos
            5. Crear estrageia de incendio
            6. Cambiar de hora
            7. Cerrar sesion
             """)

        user_entry = input("Ingrese su opcion: ")

        if user_entry in functions:
            functions[user_entry]()
        elif user_entry == "7":
            exit_loop = True
            quit()


def menu_anaf():
    exit_loop = False
    functions = {"1": incendios_activos, "2": incendios_apagados, "3": recursos_mas_utilizados,
                 "4": recusos_mas_efectivos, "5": estrategia_extincion, "6": cambiar_hora}
    while not exit_loop:
        print(""" Elegir una de las suguientes opciones:
            1. Incendios Activos
            2. Incendios Apagados
            3. Recursos mas utilizados
            4. Recursos mas efectivos
            5. Crear estrageia de incendio
            6. Cambiar de hora
            7. Cerrar sesion
             """)

        user_entry = input("Ingrese su opcion: ")

        if user_entry in functions:
            functions[user_entry]()
        elif user_entry == "7":
            exit_loop = True


def incendios_activos():
    for ID in incendios.diccionario:
        if incendios.diccionario[ID].potencia > 0:
            print(incendios.diccionario[ID].fecha_inicio, "porcenaje de extincion",
                  "-".join(map(str, incendios.diccionario[ID].return_recursos())))


def incendios_apagados():
    for ID in incendios.diccionario:
        if incendios.diccionario[ID].potencia == 0:
            print(incendios.diccionario[ID].fecha_inicio, incendios.diccionario[ID].fecha_termino, "-".join(map(str, incendios.diccionario[ID].return_recursos())))


def cambiar_hora():
    Menu.cambiar_hora = True
    menu = Menu()
    menu.start()


def recursos_mas_utilizados():
    pass


def recusos_mas_efectivos():
    pass


def estrategia_extincion():
    pass


class Tiempo:

    def __init__(self, minutos=0, hora=0, dia=1, mes=1, ano=0):
        self.minutos, self.hora, self.dia, self.mes, self.ano = minutos, hora, dia, mes, ano

    # Acotacion, se verifica primero el año porque para verificar
    def cambiar(self, minutos_nuevos, hora_nueva, dia_nuevo, mes_nuevo, ano_nuevo):
        # el dia se necesita el mes, y si el año es biciesto febrero cambia
        if self.verificar_minutos(minutos_nuevos) and self.verificar_hora(hora_nueva) and self.verificar_ano(ano_nuevo) and self.verificar_dia_mes(dia_nuevo, mes_nuevo):
            self.minutos, self.hora, self.dia, self.mes, self.ano = minutos_nuevos, hora_nueva, dia_nuevo, mes_nuevo, ano_nuevo

            return True
        else:
            return False

    def verificar_numero(self, numero):
        largo = 0
        for character in numero:
            if character in "0123456789":
                largo += 1
        if largo == len(numero):
            return True
        return False

    def verificar_minutos(self, minutos_nuevos):
        if len(minutos_nuevos) == 2 and self.verificar_numero(minutos_nuevos):
            minutos_nuevos = int(minutos_nuevos)
            if minutos_nuevos < 60 and minutos_nuevos >= 0:
                return True
            return False
        return False

    def verificar_hora(self, hora_nueva):
        if len(hora_nueva) == 2 and self.verificar_numero(hora_nueva):
            hora_nueva = int(hora_nueva)
            if hora_nueva < 24 and hora_nueva >= 0:
                return True
            return False
        return False

    def verificar_ano(self, ano_nuevo):
        self.bisiesto = False
        # Se asume que el ano ingresado esta entre (1000y9999)
        if len(ano_nuevo) == 4 and self.verificar_numero(ano_nuevo):
            ano_nuevo = int(ano_nuevo)
            # Verificar si es bisiesto
            if ano_nuevo >= 1000 and ano_nuevo <= 9999 and ano_nuevo % 4 == 0 and (ano_nuevo % 100 != 0 or ano_nuevo % 400 == 0):
                self.bisiesto = True
                return True
            elif ano_nuevo >= 1000 and ano_nuevo <= 9999:
                return True
            return False
        return False

    def verificar_dia_mes(self, dia_nuevo, mes_nuevo):
        meses_posibles = {"01": 31, "02": (28, 29), "03": 31, "04": 30, "05": 31,
                          "06": 30, "07": 31, "08": 31, "09": 30, "10": 31, "11": 30, "12": 31}
        if len(dia_nuevo) == 2 and len(mes_nuevo) == 2 and self.verificar_numero(mes_nuevo) and self.verificar_numero(dia_nuevo):
            if mes_nuevo != "02" and mes_nuevo in meses_posibles and int(dia_nuevo) <= meses_posibles[mes_nuevo] and int(dia_nuevo) > 0:
                if self.bisiesto:
                    meses = ["01-31", "02-29", "03-31", "04-30", "05-31", "06-30",
                             "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
                else:
                    meses = ["01-31", "02-28", "03-31", "04-30", "05-31", "06-30",
                             "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
                self.numero_dias = regresion_dias(mes_nuevo, meses)
                self.mes_nuevo = int(mes_nuevo)
                self.dia_nuevo = dia_nuevo
                return True
            elif mes_nuevo == "02":
                if self.bisiesto:
                    meses = ["01-31", "02-29", "03-31", "04-30", "05-31", "06-30",
                             "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
                    self.numero_dias = regresion_dias(mes_nuevo, meses)
                    self.mes_nuevo = mes_nuevo
                    self.dia_nuevo = meses_posibles[mes_nuevo][1]  # dia 29
                    return True
                else:
                    meses = ["01-31", "02-28", "03-31", "04-30", "05-31", "06-30",
                             "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
                    self.numero_dias = regresion_dias(mes_nuevo, meses)
                    self.mes_nuevo = mes_nuevo
                    self.dia_nuevo = meses_posibles[mes_nuevo][0]  # dia 28
                    return True
            return False
        return False


def regresion_dias(string_mes, lista_meses):
    if lista_meses[0].split("-")[0] == string_mes:
        return int(lista_meses[0].split("-")[1])
    else:
        return int(lista_meses[0].split("-")[1]) + regresion_dias(string_mes, lista_meses[1:])


class Menu:
    cambiar_hora = False

    def __init__(self, user="", password="", tiempo=None):
        self.user = user
        self.password = password
        self.anaf = False
        self.encontrado = False
        self.error_usuario = False
        self.error_tiempo = False
        self.cambiar = False
        self.tiempo = tiempo

    def start(self):
        if not self.error_usuario and not Menu.cambiar_hora:
            print("*" * 20)
            print("Bienvenido a SuperLuchin!")
            self.user = input("Ingrese usuario: ")
            self.password = input("Ingrese constrasena: ")
            self.verificar_informacion()
            hora = input("Ingrese hora (hh:mm ej: 03:21): ").split(":")
            fecha = input(
                "Ingrese fecha (aaaa-mm-dd ej: 2016-03-01): ").split("-")
            self.tiempo = crear_tiempo(hora, fecha)  # Crear el objeto tiempo
            if self.anaf:
                menu_anaf()
        elif self.error_usuario:
            print("*" * 20)
            print("Ususario  y/o constrasena incorrectos")
            self.user = input("Ingrese usuario: ")
            self.password = input("Ingrese constrasena: ")
            self.verificar_informacion()
        elif self.error_tiempo:
            print("*" * 20)
            print("Fecha y/o hora incorrecta")
            hora = input("Ingrese hora (hh:mm ej: 03:21): ").split(":")
            fecha = input(
                "Ingrese fecha (aaaa-mm-dd ej: 2016-03-01): ").split("-")
            self.tiempo = crear_tiempo(hora, fecha)  # Crear el objeto tiempo
        elif Menu.cambiar_hora:
            hora = input("Ingrese nueva hora (hh:mm ej: 03:21): ").split(":")
            fecha = input(
                "Ingrese nueva fecha (aaaa-mm-dd ej: 2016-03-01): ").split("-")
            self.tiempo = crear_tiempo(hora, fecha)  # Crear el objeto tiempo
            Menu.cambiar_hora = False  # Si se desea cambiar al hora otra, vez se puede

    def verificar_informacion(self):
        for indice in usuarios.diccionario:
            if self.user == usuarios.diccionario[indice].nombre and self.password == usuarios.diccionario[indice].constrasena:
                self.encontrado = True
                if len(usuarios.diccionario[indice].recurso_id) == 0:
                    self.anaf = True
        if self.encontrado and not self.anaf:
            print("Hola {}".format(self.user))  # Pilotos y Jefes
            return self.encontrado, self.anaf
        elif self.anaf:  # ANAF
            print("Hola {} de la ANAF!".format(self.user))
            return self.encontrado, self.anaf
        elif not self.anaf and not self.encontrado:
            self.error_usuario = True
            self.start()


def crear_tiempo(hora=[], fecha=[]):
    if len(hora) == 2 and len(fecha) == 3:
        dict_temporal = {}
        dict_temporal["hora_nueva"] = hora[0]
        dict_temporal["minutos_nuevos"] = hora[1]
        dict_temporal["ano_nuevo"] = fecha[0]
        dict_temporal["mes_nuevo"] = fecha[1]
        dict_temporal["dia_nuevo"] = fecha[2]
        objeto_tiempo = Tiempo()
        objeto_tiempo.cambiar(**dict_temporal)
        return objeto_tiempo
    else:
        dict_temporal = {}
        dict_temporal["hora_nueva"] = "25"
        dict_temporal["minutos_nuevos"] = "61"
        dict_temporal["ano_nuevo"] = "100000"
        dict_temporal["mes_nuevo"] = "13"
        dict_temporal["dia_nuevo"] = "31"
        objeto_tiempo = Tiempo()
        objeto_tiempo.cambiar(**dict_temporal)


def crear_menu():

    menu = Menu()
    menu.start()
    return menu

    # Se verifica en el diccionario si el mes ingresado es correcto, tambien
    # relacionando el nuemero de dias por mes


if __name__ == '__main__':
    menu = crear_menu()
