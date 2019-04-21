from functools import reduce

with open("chatayudantes.iic2233", "rb") as archivo_1:
    data_1 = archivo_1.read()
lista_bytes = []
largo = len(data_1)
i = 0
while True:
    if i + 4 > largo:
        break

    lista_bytes.append(reduce(lambda x, y: x + y, data_1[i:i + 4]))
    # lista_bytes += [sum(bytearray(data_1[i:i + 4]))]
    i += 4


def invertir(numero):
    numero = str(numero)
    if len(numero) < 3:
        if len(numero) == 2:
            num = "0" + numero
        else:
            num = "00" + numero
    else:
        num = numero
    new = ""
    for digito in num:
        if digito != "5" and digito != "0":
            new += str(10 - int(digito))
        elif digito == "0":
            new += "5"
        elif digito == "5":
            new += "0"

    aux = list(new)
    return "".join(aux[::-1])


lista_bytes = list(map(lambda x: invertir(x), lista_bytes))


def generador_primos():
    n = 1
    while True:
        con = True
        n += 1
        for i in range(2, n):
            if n % i == 0:
                con = False
        if con == True:
            yield n


def generador_malvados():
    n = 1
    while True:
        con = 0
        a = bin(n)
        for i in a:
            if i == "1":
                con += 1
        if con % 2 == 0 and con != 0:
            yield n
        n += 1


largo_bytes = len(lista_bytes)
lista_wav = []
lista_gif = []
malvados = generador_malvados()
primos = generador_primos()
i = 0
contador = 0
val = True
while True:
    j = next(malvados) + i
    if len(lista_bytes[i:j]) == 0:
        break
    lista_gif += [lista_bytes[i:j]]

    i = j
    if val:
        j = next(primos) + i
    if contador + j < 9783:
        aux = [lista_bytes[i:j]]
        contador += len(aux)
        lista_wav += aux
        i = j
    else:
        if val:
            falta = 9783 - contador
            lista_wav += lista_bytes[i:i + falta]
            i = i + falta
            val = False
temp = []
for fila in lista_wav:
    temp += list(map(int, fila))

lista_wav = temp

for fila in lista_gif:
    temp += list(map(int, fila))
lista_gif = temp


def escritura(lista, nombre):
    with open(nombre, "wb") as file:
        bien_escrito = []
        for chunk in lista:
            for el in chunk:
                bytes([int(el)])
    