import csv
from estructuras import Nodo, ListaLigada, ColaPrioridades
#from probabilities import Probabilidades, randint
from probabilities2 import Probabilidades, randint
from funciones import promedio_fronteras, evento_ocurra, buscar_entero


class Pais:

    def __init__(self, nombre, conexiones_aereas, conexiones_terrestres, poblacion_viva=0, poblacion_infectada=0, poblacion_muerta=0, aeropuertos_abiertos=True, fronteras_abiertas=True):
        self.nombre = nombre
        self.conexiones_aereas = conexiones_aereas
        self.conexiones_terrestres = conexiones_terrestres
        self.poblacion_viva, self.poblacion_infectada, self.poblacion_muerta, self.aeropuertos_abiertos, self.fronteras_abiertas = poblacion_viva, poblacion_infectada, poblacion_muerta, aeropuertos_abiertos, fronteras_abiertas
        self.infeccion = None
        self.dias_infectado = 0
        self.prioridades=ColaPrioridades()
        self.existencia()

    def existencia(self):
        if len(self.conexiones_aereas) == 0:
            self.cerrar_aeropuerto()
        if len(self.conexiones_terrestres) == 0:
            self.cerrar_frontera()

    def entregar_mascarillas(self):
        self.con_mascarillas = True

    def abrir_aeropuerto(self):
        self.aeropuertos_abiertos = True

    def cerrar_aeropuerto(self):
        self.aeropuertos_abiertos = False

    def abrir_frontera(self):
        self.fronteras_abiertas = True

    def cerrar_frontera(self):
        self.fronteras_abiertas = False

    def actualizar_cola(self):
        pass

    @property
    def status(self):
        if self.poblacion_viva == 0 and self.poblacion_infectada == 0:
            return "Muerto"
        elif self.poblacion_infectada > 0:
            return "Infectado"
        else:
            return "Limpio"

    def __repr__(self):
        return "Pais:{}, Dias Infectado:{}, Vivos:{}, Infectados:{}, Muertos:{} ,Status:{}".format(self.nombre, self.dias_infectado, self.poblacion_viva, self.poblacion_infectada, self.poblacion_muerta, self.status)


class Mundo:
    poblacion_incial = 0
    poblacion_viva = 0
    poblacion_infectada = 0
    poblacion_muerta = 0
    dias = 0
    infeccion = None

    def __init__(self, archivo, lista_paises=ListaLigada()):
        self.lista_paises = lista_paises
        self.archivo = archivo
        self.iniciar_mundo()  # Se hace este paso intermedio para no utilizar las estructuras
        # prohibidas de Python
        self.paises_conectados()
        self.poblar_mundo()

    def paises_conectados(self):
        temp = ListaLigada()
        for pais in self.paises:
            conexiones_aire = ListaLigada()
            for pareja in self.lista_paises:
                if pais[0] == pareja[0] and pareja[1] not in conexiones_aire:
                    conexiones_aire.append(pareja[1])
                if pais[0] == pareja[1] and pareja[0] not in conexiones_aire:
                    conexiones_aire.append(pareja[0])
            conexiones_tierra = ListaLigada()
            for pareja in self.paises_terrestres:
                if pais[0] == pareja[0] and pareja[1] not in conexiones_tierra:
                    conexiones_tierra.append(pareja[1])
                if pais[0] == pareja[1] and pareja[0] not in conexiones_tierra:
                    conexiones_tierra.append(pareja[0])
            pais = Pais(pais[0], conexiones_aire,
                        conexiones_tierra, int(pais[1]))
            temp.append(pais)
        self.paises_conectados = temp

    def poblar_mundo(self):
        for pais in self.paises_conectados:
            Mundo.poblacion_incial += pais.poblacion_viva
        Mundo.poblacion_viva = Mundo.poblacion_incial

    def iniciar_mundo(self):
        with open("{}".format(self.archivo[0]), encoding="utf-8") as archivo:
            next(archivo)  # Se omite la primera linea
            lector = csv.reader(archivo)
            self.lista_paises = ListaLigada(*lector)  # *args
        with open("{}".format(self.archivo[1]), encoding="utf-8") as archivo2:
            next(archivo2)  # Se omite la primera linea
            lector = csv.reader(archivo2, delimiter=";")
            self.paises_terrestres = ListaLigada(*lector)  # *args
        with open("population.csv", encoding="utf-8") as poblaciones:
            next(poblaciones)
            poblaciones = ListaLigada(*csv.reader(poblaciones))
            paises = ListaLigada()
            for info in poblaciones:  # Se hace este paso intermedio para obtener los indices en poblacion por pais
                paises.append(info)
            self.paises = paises



    def __repr__(self):
        if Mundo.dias>0:
            return str(Mundo.dias)+","+str(Mundo.poblacion_incial)+"," \
            +str(Mundo.poblacion_viva)+","+str(int(Mundo.poblacion_infectada))+","+str(Mundo.poblacion_muerta)
        else:
            return "Dias,Poblacion_inicial,Poblacion_viva,Poblacion_infectada,Poblacion_muerta" 
 


class Grafo:

    instanciados_nombre = ListaLigada()
    instanciados_clase = ListaLigada()

    # Se entregan los paises como objetos ya instanciados para ocupar el mismo
    # espacio de memoria
    def __init__(self, tipo, cabeza, paises_conectados=Mundo.paises_conectados):

        self.tipo = tipo
        self.cabeza = cabeza
        self.nombre = cabeza.nombre
        self.paises = paises_conectados
        self.camino = ListaLigada()
        Grafo.instanciados_nombre.append(self.nombre)
        Grafo.instanciados_clase.append(self)
        self.iniciar_tipo()
        self.terminado=False

    def iniciar_tipo(self):

        if self.tipo == "Terrestre":

            self.instanciar_grafo_T()
        elif self.tipo == "Aereo":
            self.instanciar_grafo_A()
        else:
            raise TypeError("Por favor ingrese un tipo valido")

    def __repr__(self):
        return self.nombre

    def instanciar_grafo_T(self):
        pais = self.cabeza
        if len(pais.conexiones_terrestres) > 0:
            conexiones = pais.conexiones_terrestres
            for conexion in self.paises:
                    # if not isinstance(conexion,Grafo) and conexion.nombre not
                    # in Grafo.instanciado:
                if conexion.nombre in conexiones and conexion.nombre not in self.camino and conexion.nombre not in Grafo.instanciados_nombre:
                    conexion.infectado = True
                    aux = Grafo("Terrestre", conexion, self.paises)
                    self.camino.append(aux)
                elif conexion.nombre in conexiones and conexion.nombre not in self.camino and conexion.nombre in Grafo.instanciados_nombre:
                    idx = Grafo.instanciados_nombre.index(conexion.nombre)
                    self.camino.append(Grafo.instanciados_clase[idx])

                # else:
                    # break

    def instanciar_grafo_A(self):
        pais = self.cabeza
        if len(pais.conexiones_aereas) > 0:
            conexiones = pais.conexiones_aereas
            for conexion in self.paises:
                if conexion.nombre in conexiones and conexion.nombre not in self.camino and conexion.nombre not in Grafo.instanciados_nombre:
                    aux = Grafo("Terrestre", conexion, self.paises)
                    self.camino.append(aux)
                elif conexion.nombre in conexiones and conexion.nombre not in self.camino and conexion.nombre in Grafo.instanciados_nombre:
                    idx = Grafo.instanciados_nombre.index(conexion.nombre)
                    self.camino.append(Grafo.instanciados_clase[idx])


class Infeccion:

    def __init__(self, nombre):
        self.nombre = nombre

        if self.nombre == ("Virus" or "virus"):
            self.contagiosidad, self.mortalidad, self.resistencia_medicina, self.visibilidad = ListaLigada(
                1.5, 1.2, 1.5, 0.5)

        elif self.nombre == ("Bacteria" or "bacteria"):
            self.contagiosidad, self.mortalidad, self.resistencia_medicina, self.visibilidad = ListaLigada(
                1.0, 1.0, 0.5, 0.7)

        else: #Gracias al chequeo inicial en el menu, se puede asumir que sera de tipo "Parasito"
            self.contagiosidad, self.mortalidad, self.resistencia_medicina, self.visibilidad = ListaLigada(
                0.5, 1.5, 1.0, 0.45)


class Cura:
    progreso=0
    descubierta=False
    def __init__(self):
        pass


class Master:
    grafo_aereo = None
    grafo_terrestre = None
    aire=False
    tierra=False

    def __init__(self):
        pass

    @staticmethod
    def contagiar_pais(Pais):
        prob=Probabilidades.prob_contagio_propio(Pais)           #NOA
        # OLVIDAR!!!
        #prob = 5 / 6
        if Pais.infeccion==None:
            Pais.poblacion_infectada=1 #Poblacion infectada inicial porque el virus comienza ahi
            Pais.infeccion = Mundo.infeccion
        if evento_ocurra(prob):
            Pais.poblacion_infectada += round((prob) * 6,0)
            Pais.poblacion_viva -= round((prob) * 6,0)
            Mundo.poblacion_infectada+=round((prob) * 6,0)
            Mundo.poblacion_viva-=round((prob) * 6,0)
            Pais.dias_infectado += 1
        prob2=Probabilidades.prob_muerte(Pais)
        if evento_ocurra(prob):
            Pais.poblacion_muerta+=1
            Pais.poblacion_infectada-=1
            Mundo.poblacion_muerta+=1
            Mundo.poblacion_infectada+=1



    @staticmethod
    def contagiar_vecinos(Pais, paises_conectados):
        prob=Probabilidades.prob_contagio_paises(Pais)  
        if Master.aire and not Master.tierra:
            Inicio = Grafo("Terrestre", Pais, paises_conectados)
            if Pais.fronteras_abiertas and Probabilidades.se_puede_tierra and not Master.tierra:
                for grafo in Inicio.camino:
                    if grafo.cabeza.infeccion == None and evento_ocurra(prob):
                        print(Pais.nombre+"----->"+grafo.cabeza.nombre)
                        if not Cura.descubierta:
                            Master.descubrir_infeccion()
                        else:
                            Cura.progreso+=main.Master.progreso_cura()
                        Master.contagiar_pais(grafo.cabeza)
                        Master.descubrir_infeccion()
                        Master.acciones_gobierno(grafo.cabeza,paises_conectados,Cura.progreso)
                        Master.contagiar_vecinos("Terrestre",
                            grafo.cabeza, paises_conectados)
            Master.tierra=True
        elif not Master.aire and Master.tierra and Mundo.poblacion_infectada/Mundo.poblacion_incial>=0.04:
            Inicio = Grafo("Aereo", Pais, paises_conectados)
            if Pais.aeropuertos_abiertos and Probabilidades.se_puede_aire and not Master.aire:
                for grafo in Inicio.camino:
                    if grafo.cabeza.infeccion == None and evento_ocurra(prob):
                        print(Pais.nombre+"----->"+grafo.cabeza.nombre)
                        Master.contagiar_pais(grafo.cabeza)
                        Master.descubrir_infeccion()
                        Master.acciones_gobierno(grafo.cabeza,paises_conectados,Cura.progreso)
                        Master.contagiar_vecinos(
                            grafo.cabeza, paises_conectados)
            Master.aire=True
        else:
            Inicio = Grafo("Terrestre", Pais, paises_conectados)
            if Pais.fronteras_abiertas and Probabilidades.se_puede_tierra and not Master.tierra:
                for grafo in Inicio.camino:
                    if grafo.cabeza.infeccion == None and evento_ocurra(prob):
                        print(Pais.nombre+"----->"+grafo.cabeza.nombre)
                        Master.contagiar_pais(grafo.cabeza)
                        Master.descubrir_infeccion()
                        Master.acciones_gobierno(grafo.cabeza,paises_conectados,Cura.progreso)
                        Master.contagiar_vecinos(
                            grafo.cabeza, paises_conectados)
            Master.tierra=True



    @staticmethod
    def descubrir_infeccion():
        a = (Mundo.poblacion_infectada * Mundo.infeccion.visibilidad) * \
            (Mundo.poblacion_muerta)**2 / (Mundo.poblacion_incial)
        if evento_ocurra(a):
            Cura.descubierta=True
            Cura.progreso += Master.progreso_cura()

    @staticmethod
    def progreso_cura():
        return Mundo.poblacion_viva / (2 * Mundo.poblacion_incial)

    @staticmethod
    def acciones_gobierno(Pais,paises_conectados,progreso_cura):
        cola= Pais.prioridades
        cola.crear_cola(Pais,paises_conectados,progreso_cura)
        if len(cola)>0:
            decisiones_dia=cola.primeros_tres()
            for decision in decisiones_dia:
                if decision[0] == "Cerrar aeropuertos":
                    Pais.cerrar_aeropuerto()
                elif decision[0] == "Cerrar fronteras":
                    Pais.cerrar_fronteras()
                elif decision[0] == "Entregar mascarillas":
                    Pais.entregar_mascarillas()
                else:
                    Pais.abrir_frontera()
                    Pais.abrir_aeropuerto()


