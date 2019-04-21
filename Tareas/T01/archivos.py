import os
import tkinter


newpath = r'C:\Users\luism\Desktop\Progra\LuisFros-iic2233-2017-1\Tareas\T01\Reportes Estrategias de Extincion'
if not os.path.exists(newpath):
    os.makedirs(newpath)
#open("Reportes Estrategias de Extincion\ {}+_.txt".format(ID,incendio,nombre,criterio))


class Recursos:

    def __init__(self, tipo="", lat="", lon="", velocidad="", autonomia="", delay="", tasa_extincion="", costo=""):
        self.tipo, self.lat, self.lon, self.velocidad, self.autonomia, self.delay, self.tasa_extincion, self.costo, self.id = tipo, float(
            lat), float(lon), int(velocidad), int(autonomia), int(delay), int(tasa_extincion), int(costo), id


class Incendios:

    def __init__(self, lat="", lon="", potencia="", fecha_inicio=""):
        self.lat, self.lon, self.potencia, self.fecha_inicio = float(
            lat), float(lon), int(potencia), fecha_inicio
        self._recursos_utilizados=list()

    def porcentaje_extincion(self):
        pass

    def agregar_recurso(self,id_recurso):
       self._recursos_utilizados.append(id_recurso)

    def return_recursos(self):
        return self._recursos_utilizados

class Metoerologia:

    def __init__(self, lat="", lon="", fecha_termino="", fecha_inicio="", tipo="", valor="", radio=""):
        self.lat, self.lon, self.fecha_termino, self.fecha_inicio, self.tipo, self.valor, self.radio = float(
            lat), float(lon), fecha_termino, fecha_inicio, tipo, float(valor), int(radio)


class Usuarios:

    def __init__(self, nombre="", constrasena="", recurso_id=""):
        self.nombre, self.constrasena, self.recurso_id = nombre, constrasena, recurso_id


class Archivo:

    def __init__(self, nombre):
        self.nombre = nombre

    def cerrar_archivo(self):
        return self.nombre.close()

    def crear_diccionario(self):
        lector = open("{}.csv".format(self.nombre), encoding="utf-8")
        texto = [i.strip().split(",") for i in lector]
        primera_fila = [i.split(":") for i in texto[0]]
        atributos = [(idx, i[0]) for idx, i in enumerate(primera_fila)]
        Diccionario_ID = {}
        for linea in texto:
            Diccionario_temp = {}
            if ":" not in linea[0]:  # Se omite la primera linea
                for tupla in atributos:
                    
                    # SE OMITE EL ATRIBUTO ID PORQUE EL NOMBRE "ID" ESTA TOMADO
                    # Y EL ID ES LA CLAVE DEL DICT!!!
                    if tupla[1] != "id":
                        if tupla[1][:3] == "con":
                            # Se omite el caracter especial, en este caso la
                            # "ñ"
                            Diccionario_temp["constrasena"] = linea[tupla[0]]
                        else:
                            Diccionario_temp[tupla[1]] = linea[tupla[0]]
                Diccionario_ID[int(linea[0])] = Diccionario_temp
        self.diccionario = Diccionario_ID
        # IMPORTANTE AL ESCRIBIR ARCHIVOS CERRARLOS


def instanciar_archivos():
    lista_archivos = ["recursos", "meteorologia", "usuarios", "incendios"]
    return [Archivo(i) for i in lista_archivos]


def convertir_id_objetos(objeto):
    for indice in objeto.diccionario:
        if objeto.nombre == "recursos":
            objeto.diccionario[indice] = Recursos(**objeto.diccionario[indice])
        elif objeto.nombre == "usuarios":
            objeto.diccionario[indice] = Usuarios(**objeto.diccionario[indice])
        elif objeto.nombre == "meteorologia":
            objeto.diccionario[indice] = Metoerologia(
                **objeto.diccionario[indice])
        elif objeto.nombre == "incendios":
            objeto.diccionario[indice] = Incendios(
                **objeto.diccionario[indice])
        # else:
        # 	objeto.diccionario[indice]=Incendios(**objeto.diccionario[indice])

def conectar_recursos_usuarios():
    for usuario in usuarios.diccionario:
        for recurso in recursos.diccionario:
            if str(recurso) == usuarios.diccionario[usuario].recurso_id:
                usuarios.diccionario[
                    usuario].recurso_asociado = recursos.diccionario[recurso]


def start_archivos():
    recursos, meteorologia, usuarios, incendios = instanciar_archivos()
    archivos = (recursos, meteorologia, usuarios, incendios)

    for obj in archivos:
        obj.crear_diccionario()
        convertir_id_objetos(obj)
    return recursos, meteorologia, usuarios, incendios


if __name__ == "__main__":
    recursos, meteorologia, usuarios, incendios = start_archivos()
    conectar_recursos_usuarios()
    anaf.menu_anaf()

# Ingreso de pruebas
