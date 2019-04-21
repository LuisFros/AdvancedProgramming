import main as main
import csv
from functools import reduce
from connections_generator import generate_connections



generate_connections()
archivos = main.ListaLigada("random_airports.csv", "borders.csv")
# Tambien toma en cuenta "Population.csv" Se crea el mundo :O
Base = main.Mundo(archivos)

def menu_inicial():
    exit_loop = False
    functions = main.ListaLigada(main.ListaLigada(
        "1", juego_viejo), main.ListaLigada("2", juego_nuevo))
    while not exit_loop:
        print(""" Hola, Bienvenido a Pandemic!
	    	Elegir una de las suguientes opciones:
	        1. Continuar partida
	        2. Empezar partida nueva
	         """)

        user_entry = input("Ingrese su opcion: ").strip()
        count = 0
        for funcion in functions:

            if funcion[0] == user_entry:
                pais, infeccion = funcion[1]()
                menu_principal(pais, infeccion)

                exit_loop = True

        if count == len(functions):
            exit_loop = True
            # quit()


def juego_viejo():
	with open("dias.csv",r) as archivo:
		lector=csv.reader(archivo)
		valido=lector[-1]
		menu_principal(valido[0],valido[1])


def juego_nuevo():

    # Se crea el archivo de informacion por dia, si ya existia se sobre-escribe
    with open("dias.csv", "w") as entrada:
        pass
    lista_paises = main.ListaLigada(
        *map(lambda x: x.nombre.lower(), Base.paises_conectados))
    while True:
        pais = input(
            "Por favor ingrese pais para iniciar la infeccion: (ej: Colombia)\n").strip().lower()
        if pais in lista_paises:
            break
        else:
            print("Ingrese un pais valido por favor")
    exit_loop = False
    while not exit_loop:

        print(""" Elegir una de las suguientes opciones:
	        1. Virus
	        2. Bacteria
	        3. Parasito
	         """)

        user_entry = input("Ingrese su opcion: ").strip()
        if user_entry == "1":
            infeccion = "Virus"
            Pasar_dia(pais, infeccion)
            return pais, infeccion
            exit_loop = True

        elif user_entry == "2":
            infeccion = "Bacteria"
            Pasar_dia(pais, infeccion)
            return pais, infeccion
            exit_loop = True

        elif user_entry == "3":
            infeccion = "Parasito"
            Pasar_dia(pais, infeccion)
            return pais, infeccion
            exit_loop = True

        else:
            print("Por favor ingrese un numero valido")


def Pasar_dia(pais, infeccion):
    if main.Mundo.dias == 0:
        print("(Pais Origen infectado----->Pais infectado)")
        main.Mundo.dias += 1
        Infeccion = main.Infeccion(infeccion)
        main.Mundo.infeccion = Infeccion
        pais_objeto = main.ListaLigada(
            *filter(lambda x: x.nombre.lower() == pais, Base.paises_conectados))[0]
        main.Master.contagiar_vecinos(pais_objeto, Base.paises_conectados)
        linea = main.ListaLigada(*repr(Base).strip().split())
        with open("dias.csv", "a") as salida:
            escritor = csv.writer(salida)
            escritor.writerow(linea)

    else:
        print("Pais Origen infectado----->Pais infectado")
        main.Mundo.dias += 1
        pais_objeto = main.ListaLigada(
            *filter(lambda x: x.nombre.lower() == pais, Base.paises_conectados))[0]
        main.Master.contagiar_pais(pais_objeto)
        if not main.Cura.descubierta:
            main.Master.descubrir_infeccion()
        else:
            main.Cura.progreso += main.Master.progreso_cura()
        main.Master.acciones_gobierno(
            pais_objeto, Base.paises_conectados, main.Cura.progreso)
        main.Master.contagiar_vecinos(pais_objeto, Base.paises_conectados)
        linea = main.ListaLigada(*repr(Base).strip().split())
        with open("dias.csv", "a") as salida:
            escritor = csv.writer(salida)
            escritor.writerow(linea)
            # print(Base,file=salida)


def Estadisticas(pais, infeccion):
    exit_loop = False
    while not exit_loop:

        print(""" Elegir una de las suguientes opciones:
	        1. Resumen del dia
	        2. Por pais
	        3. Global
	        4. Muertes e infeccions por dia
	        5. Promedio muertes e infecciones
	        6. Volver
	         """)

        user_entry = input("Ingrese su opcion: ").strip()
        if user_entry == "1":

            exit_loop = True

        elif user_entry == "2":
            lista_paises = main.ListaLigada(
                *map(lambda x: x.nombre.lower(), Base.paises_conectados))
            while True:
                pais = input("Eliga un pais:").lower()
                if pais in lista_paises:
                    break
                print("Por favor ingrese un pais valido")
            pais_1 = main.ListaLigada(
                *filter(lambda x: x.nombre.lower() == pais, Base.paises_conectados))
            print(pais_1[0])  # Se aprovecha sobre-escribir __repr__
            print(pais_1[0].prioridades)  # lo mismo que lo anterior
            exit_loop = True

        elif user_entry == "3":  # Global
            limpios = main.ListaLigada(
                *filter(lambda x: x.dias_infectado == 0, Base.paises_conectados))
            infectados = main.ListaLigada(
                *filter(lambda x: x.dias_infectado > 0, Base.paises_conectados))
            muertos = main.ListaLigada(
                *filter(lambda x: x.poblacion_infectada == 0 and x.poblacion_infectada == 0, Base.paises_conectados))
            print("Limpios: ")
            for pais in limpios:
                print(pais)
            print("Infectados: ")
            for pais in infectados:
                print(pais)
            print("Muertos: ")
            for pais in muertos:
                print(pais)
            print(Base)
            exit_loop = True

        elif user_entry == "4":  # Muertes infecciones por dia
            with open("dias.csv", "r") as archivo:
                lector = csv.reader(archivo)
                habilitado = main.ListaLigada(
                    *map(lambda x: x[0].split(","), main.ListaLigada(*filter(lambda x: len(x) > 0, lector))))
                for dia in habilitado:
                    print("Dia:{} ,Infectados:{} ,Muertos:{}".format(
                        dia[0], dia[3], dia[4]))
            exit_loop = True
        elif user_entry == "5":  # Proemdio muertes e infecciones
            with open("dias.csv", "r") as archivo:
                lector = csv.reader(archivo)
                habilitado = main.ListaLigada(
                    *map(lambda x: x[0].strip(","), main.ListaLigada(*filter(lambda x: len(x) > 0, lector))))
                tasa_vida = int(Base.poblacion_infectada) / \
                    int(habilitado[-1][0])
                tasa_muerte = int(Base.poblacion_muerta) / \
                    int(habilitado[-1][0])
                print("Tasa vida: {},Tasa muerte:{}".format(
                    tasa_vida, tasa_muerte))
                # Se asume que la del dia es la misma que la acumulada(dia
                # actual)


def Guardar_Estado(pais, infeccion):
	#Estado ya se guarda en "dias.csv"
    pass


def menu_principal(pais, infeccion):
    exit_loop = False
    functions = main.ListaLigada(main.ListaLigada("1", Pasar_dia), main.ListaLigada(
        "2", Estadisticas), main.ListaLigada("3", Guardar_Estado))
    numeros = main.ListaLigada(*map(lambda x: x[0], functions))
    while not exit_loop:
        print(""" Elegir una de las suguientes opciones:
	        1. Pasar un dia
	        2. Estadisticas
	        3. Guardar estado de partida
	        4. Salir del juego
	         """)

        user_entry = input("Ingrese su opcion: ").strip()
        if user_entry in numeros:
            functions[numeros.index(user_entry)][1](pais, infeccion)
        elif user_entry == "4":
            exit_loop = True
            # quit()

	

if __name__ == '__main__':
	menu_inicial()