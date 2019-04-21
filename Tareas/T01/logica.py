from math import pi


def convertir_tiempo_clima():
    for evento in meteorologia.diccionario:
        fecha, hora = meteorologia.diccionario[evento].fecha_inicio.split(" ")
        fecha, hora = fecha.split("-"), hora.split(":")
        meteorologia.diccionario[evento].fecha_inicio = crear_tiempo(
            fecha=fecha, hora=hora)
        fecha, hora = meteorologia.diccionario[evento].fecha_termino.split(" ")
        fecha, hora = fecha.split("-"), hora.split(":")
        meteorologia.diccionario[evento].fecha_termino = crear_tiempo(
            fecha=fecha, hora=hora)


def convertir_tiempo_incendios():
    for evento in incendios.diccionario:
        fecha, hora = incendios.diccionario[evento].fecha_inicio.split(" ")
        fecha, hora = fecha.split("-"), hora.split(":")
        incendios.diccionario[evento].fecha_inicio = crear_tiempo(
            fecha=fecha, hora=hora)


def estado_actual_incendio(menu, id_incendio):
    minutos = (menu.tiempo.minutos, incendios.diccionario[
               id_incendio].fecha_inicio.minutos)
    horas = (menu.tiempo.hora, incendios.diccionario[
             id_incendio].fecha_inicio.hora)
    dias = (menu.tiempo.dia, incendios.diccionario[
            id_incendio].fecha_inicio.dia)
    meses = (menu.tiempo.mes, incendios.diccionario[
             id_incendio].fecha_inicio.mes)
    anos = (menu.tiempo.ano, incendios.diccionario[
            id_incendio].fecha_inicio.ano)
    print(minutos, horas, dias, meses, anos)
    if anos[0] > anos[1]:
        incendios.diccionario[
            id_incendio].superficie_afectada = calcular_area(id_incendio)
    elif anos[0] == anos[1] and meses[0] > meses[1]:
        incendios.diccionario[
            id_incendio].superficie_afectada = calcular_area(id_incendio)
    elif anos[0] == anos[1] and meses[0] == meses[1] and dias[0] > dias[1]:
        incendios.diccionario[
            id_incendio].superficie_afectada = calcular_area(id_incendio)
    elif anos[0] == anos[1] and meses[0] == meses[1] and dias[0] == dias[1] and horas[0] > horas[1]:
        incendios.diccionario[
            id_incendio].superficie_afectada = calcular_area(id_incendio)
    elif anos[0] == anos[1] and meses[0] == meses[1] and dias[0] == dias[1] and horas[0] == horas[1] and minutos[0] > minutos[1]:
        incendios.diccionario[
            id_incendio].superficie_afectada = calcular_area(id_incendio)
    elif anos[0] == anos[1] and meses[0] == meses[1] and dias[0] == dias[1] and anos[0] == anos[1] and minutos[0] == minutos[1]:
        print("Igual al estado en la fecha inicial")
    else:
        print("Este incendio no existe en esta fecha")


def calcular_horas_totales(id_incendio):
    meses_posibles = ["01-31", "02-28", "03-31", "04-30", "05-31",
                      "06-30", "07-31", "08-31", "09-30", "10-31", "11-30", "12-31"]
    tiempo_incendio = incendios.diccionario[id_incendio].fecha_inicio
    tiempo_consulta = menu.tiempo
    delta_anos = int(tiempo_consulta.ano) - int(tiempo_incendio.ano)
    delta_dias = int(tiempo_consulta.numero_dias) - \
        int(tiempo_incendio.numero_dias)
    delta_meses = int(tiempo_consulta.mes) - int(tiempo_incendio.mes)

    print(int(tiempo_consulta.dia) > int(tiempo_incendio.dia))
    if int(tiempo_consulta.dia) > int(tiempo_incendio.dia) or int(tiempo_consulta.mes) - int(tiempo_incendio.mes) > 0:
        if int(tiempo_consulta.dia) - int(tiempo_incendio.dia) == 1:
            delta_horas = (24 - int(tiempo_incendio.hora) + int(tiempo_incendio.minutos) /
                           60) + int(tiempo_consulta.hora) + int(tiempo_consulta.minutos) / 60
        else:
            delta_horas = (24 - int(tiempo_incendio.hora) + int(tiempo_incendio.minutos) / 60) + (int(tiempo_consulta.hora) +
                                                                                                  int(tiempo_consulta.minutos) / 60) + 24 * (int(tiempo_consulta.dia) - int(tiempo_incendio.dia))
    else:
        delta_horas = int(tiempo_consulta.hora) + (int(tiempo_consulta.minutos)) / 60 \
            - int(tiempo_incendio.hora) + (int(tiempo_incendio.minutos)) / 60
    if tiempo_consulta.bisiesto:
        horas_totales = delta_horas + delta_anos * 365 + delta_dias * 24
    else:
        horas_totales = delta_horas + delta_anos * 364 + delta_dias * 24
    return horas_totales


def calcular_area(id_incendio,incendios_obj,meteorologia_obj):
    incendios=incendios_obj
    meteorologia=meteorologia_obj
    horas = calcular_horas_totales(id_incendio)
    area = (horas * 500) * (horas * 500) * pi
    area_km = area / 1000
    incendios.diccionario[id_incendio].puntos_podes=calcular_puntos_ponder(id_incendio)

def distancia(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)


def hay_climas(area_km,id_incendio):
    x1=incendios.diccionario[id_incendio].lon
    y1=incendios.diccionario[id_incendio].lat
    radio_km=horas*0.5
    radio_grado=radio_km/110 #radio en grados, 110km=1grado
    temp=[]
    for clima in meteorologia.diccionario:
        x2=meteorologia.diccionario[clima].lon
        y2=meteorologia.diccionario[clima].lat
        if radio_grado<=distancia(x1,y1,x2,y2):
            if len(temp)==0:
                temp.append(True) #Se agrega un boolean para poder verificar si la lista no esta vacia al calcular los puntos de poder
            temp.append((meteorologia.diccionario[clima].tipo,meteorologia.diccionario[clima].valor))
    return temp

def calcular_nueva_area(climas):
    viento=0 #Acumulado de vientos km/h
    temperatura=0 #Acumulado de temperaturas grados
    lluvia=0 #Acumilado de ml de lluvia 
    for tipo in climas:
        if tipo[0]=="VIENTO":
            viento+=tipo[1]
        elif tipo[0]=="TEMPERATURA":
            if tipo[1]>30: #Si la tempera es mayor a 30 afecta
                temperatura+=tipo[1]
        elif tipo[0]=="lluvia":
            temperatura+=tipo[1]
    return (viento*100+temperatura*25/1000-lluvia*50/1000) #Se divide por mil porque el radio esta en kilometros


def calcular_puntos_ponder(area_km,id_incendio):
    resultado=hay_climas(area_km,id_incendio)
    if resultado[0]:
        delta_radio=calcular_area_nueva(resultado[1:])
    radio_actual=float(radio_km)+float(delta_radio)
    pp=((pi*radio_actual*500)**2)*incendios.diccionario[id_incendio].potencia
    return pp





