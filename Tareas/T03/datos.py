from math import pi, e
from typing import Callable, Any, Union,get_type_hints,List
import time
from functools import reduce
from matplotlib import pyplot
from numpy import array
from errores import error_tipo

@error_tipo
def normal(mu:Union[int,float], sigma:Union[int,float])->Callable[...,Any]:
    a = 1 / ((2 * pi * sigma**2)**1 / 2)
    # e**((-1/2)*((x-mu)/sigma)**2)
    return (lambda x: a * e**((-1 / 2) * ((x - mu) / sigma)**2))
    

@error_tipo
def exponencial(v:Union[int,float])->Callable[...,Any]:
    return (lambda x:(v) * e**(-v * x))

@error_tipo
def gamma(v:Union[int,float], k:Union[int,float])->Callable[...,Any]:
    return (lambda x:e**(-v * x) * x**(k - 1) * (1 / (k - 1)) * (v)**k)

@error_tipo
def LEN(datos:List[float])->int:
    return len(datos)

@error_tipo
def PROM(datos:List[float])->float:
    if len(datos)==0:
        raise ZeroDivisionError()
    return sum(datos) / LEN(datos)

@error_tipo
def DESV(datos:List[float])->float:
    prom = PROM(datos)
    largo = LEN(datos)
    if largo==1:
        raise ZeroDivisionError
    return (sum(((i - prom)**2 for i in datos)) / (largo - 1))**1 / 2

@error_tipo
def VAR(datos:List[float])->float:
    return DESV(datos)**2

@error_tipo
def MEDIAN(datos:List[float])->float:  # REVISAR SI ES NECESIARIO HACER SORT()
    #datos.sort()
    if len(datos) % 2 == 0:
        par_i = -0.5 + (len(datos) / 2)
        par_r = 0.5 + (len(datos) / 2)
        return PROM([datos[int(par_r)], datos[int(par_i)]])
    impar = int(0.5 + (len(datos) / 2))
    return datos[impar]

@error_tipo
def extraer_columna(nombre_archivo: str, columna: str)-> List[float]:
    archivo = open(nombre_archivo   + ".csv", "r", encoding="utf-8")
    primera_linea = [i.split(":")[0]
                     for i in archivo.readline().strip().split(";")]
    return list(map(float, (linea.strip().split(";")[primera_linea.index(columna)] for linea in archivo)))

@error_tipo
def filtrar(columna: List[float], simbolo: str, valor: Union[int, float])->List[float]:
    operadores = {"<": (lambda x, y: x < y), ">": (lambda x, y: x > y), "<=": (
        lambda x, y: x <= y), ">=": (lambda x, y: x >= y), "==": (lambda x, y: x == y), "!=": (lambda x, y: x != y)}
    return list(filter(lambda x: operadores[simbolo](float(x), valor), columna))
    #filter(lambda x:columna)

@error_tipo
def operar(columna: List[float], simbolo: str, valor: Union[int, float])->List[float]:
    operaciones = {"+": (lambda x, y: x + y), "-": (lambda x, y: x - y), "/": (
        lambda x, y: x / y), "*": (lambda x, y: x * y), ">=<": lambda x, y: round(x, y)}
    return list(map(lambda x: operaciones[simbolo](float(x), valor), columna))

@error_tipo
def evaluar(funcion: Callable[..., Any], inicio: Union[int, float], final: Union[int, float], intervalo: Union[int, float]=1)->list:
    if inicio > final:
        inicio, final = final, inicio
    if (type(inicio) and type(final)) == type(1.55):
        decimales_inicio = len(str(inicio).split(".")[1])
        decimales_final = len(str(final).split(".")[1])
        if type(intervalo) == type(1.5):
            decimales_intervalo = len(str(intervalo).split(".")[1])
        else:
            decimales_intervalo = 0
        mayor = max([decimales_final, decimales_inicio, decimales_intervalo])
        return list(funcion(round(i * 10**(-mayor), mayor)) for i in range(int(inicio * 10**mayor), int(final * 10**mayor) + 1, int(intervalo * 10**mayor)))
    elif (type(inicio) and type(final) and type(intervalo)) == type(1):
        return list(funcion(i) for i in range(inicio, final + 1, intervalo))
    else:
        if type(inicio) == type(1.2):
            decimales_inicio = len(str(inicio).split(".")[1])
            mayor = decimales_inicio
        elif type(intervalo) != type(1.2) and type(final) == type(1.4):
            decimales_final = len(str(final).split(".")[1])
            mayor = decimales_final
        else:
            decimales_intervalo = len(str(intervalo).split(".")[1])
            mayor = decimales_intervalo
        return list(funcion(round(i * 10**(-mayor), mayor)) for i in range(int(inicio * 10**mayor), int(final * 10**mayor) + 1, int(intervalo * 10**mayor)))

@error_tipo
def comparar_columna(columna_1: List[float], simbolo: str, comando: str, columna_2: List[float])->Any:
    comandos = {"DESV": DESV, "PROM": PROM,
                "VAR": VAR, "MEDIAN": MEDIAN, "LEN": LEN}
    operadores = {"<": (lambda x, y: x < y), ">": (lambda x, y: x > y), "<=": (
        lambda x, y: x <= y), ">=": (lambda x, y: x >= y), "==": (lambda x, y: x == y), "!=": (lambda x, y: x != y)}
    return operadores[simbolo](comandos[comando](columna_1), comandos[comando](columna_2))

@error_tipo
def comparar(numero_1: Union[int, float], simbolo: str, numero_2: Union[int, float])-> Any:
    operadores = {"<": (lambda x, y: x < y), ">": (lambda x, y: x > y), "<=": (
        lambda x, y: x <= y), ">=": (lambda x, y: x >= y), "==": (lambda x, y: x == y), "!=": (lambda x, y: x != y)}
    return operadores[simbolo](numero_1, numero_2)


##Solo para consultas anidadas@#####
def do_if(consulta_a: Callable[..., Any], consulta_b: Callable[..., Any], consulta_c: Callable[..., Any])->Any:
    if consulta_b:
        consulta_a
    else:
        consulta_b
    # if inicio<final:
    #   for i in range()
    # (for i in range())
    # return [funcion(i) for i in range(inicio,final,intervalo)]


# col=extraer_columna("registros","tiempo_infectado")
# filtroo=filtrar(col,"<",50)
# print(operar(filtroo,">=<",1))

# print(comparar_columna([1,2,4,5],"==","DESV",[1,2,4,5,2,2]))
# print(evaluar(doble, 5.5, 1.2,0.5))
# print(comparar(1,"!=",2))
# print(crear_funcion("normal",0,1))



def crear_funcion(nombre_modelo: str, *parametros: Union[int, float])-> Callable[..., Any]:
    modelos = {"normal": normal, "exponencial": exponencial, "gamma": gamma}
    return modelos[nombre_modelo](*parametros)

def plotear(eje_x:List[float], eje_y:List[float], valores:List[float])->Any:
    pyplot.plot(array(eje_x), array(eje_y))
    pyplot.axis(array(valores))
    pyplot.show()

#@error_tipo
def graficar(eje_y:List[float], eje_x:Any)->Any:
    print("EJESS!!")
    print(eje_x)
    numerico = lambda x: (i for i in range(len(x)))
    normalizado = lambda x: (i / (sum(x)) for i in range(len(x)))
    opciones = {"numerico": numerico, "normalizado": normalizado}
    if ":" in eje_x and eje_x.split(":")[0] == "rango":
        print("#1")
        a, b, c = eje_x.split(":")[1].split(",")
        a, b, c = int(a), int(b), int(c)
        if ((a < b and c > 0) or (a > b and c < 0)):
            eje_x = [i for i in range(a, b, c)]
            if len(eje_x) >= len(columna):
                valores = [min(eje_x), max(eje_x)] + [min(eje_y), max(eje_y)]
                plotear(eje_x, eje_y, valores)
    elif type(eje_x) == type([]):
        print("#2")
        if len(eje_y) == len(eje_x):
            valores = [min(eje_x), max(eje_x)] + [min(eje_y), max(eje_y)]
            plotear(eje_x, eje_y, valores)
        raise Exception("Imposible Procesar")
    elif eje_x in opciones:
        print("#3")
        eje_x = opciones[eje_x](list(eje_y))
        
        plotear(eje_x, eje_y, [min(eje_x), max(eje_x)] +
                [min(eje_y), max(eje_y) + 0.04])

# promedio=PROM([i for i in range(-100,100)])
# desv=DESV([i for i in range(-100,100)])

# a=evaluar((lambda x:x), -6, 6,0.01)
# graficar([normal(0,1,i) for i in a],"normalizado")

def mega_dict():
    def funcion_type():
        return None
    return {i: globals()[i] for i in globals() if "__" not in i}
