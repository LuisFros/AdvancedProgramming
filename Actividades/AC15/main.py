import re
import requests
import json
import os

if not (os.path.exists("busquedas.json")):
    with open("busquedas.json", "w") as file:
        json.dump({}, file)


def revisar_datos(keyword):
    with open("busquedas.json") as file:
        data = json.load(file)
    if keyword in data:
        return data[keyword]
    return pedir_info(keyword)


def pedir_info(keyword):
    d = {"action": "query", "prop": "extracts", "explaintext": "True", "titles":
        keyword, \
         "format": \
             "json"}

    r = requests.get("https://es.wikipedia.org/w/api.php", params=d)
    info = r.json()
    id = list(info["query"]["pages"].keys())[0]
    extracto = info["query"]["pages"][id]["extract"]
    with open("busquedas.json") as file:
        data = json.load(file)
    data[keyword] = extracto
    with open("busquedas.json", "w") as file:
        json.dump(data, file)
    return extracto


def limpiar():
    data = []
    with open("AC15.txt", encoding="utf-8") as file:
        for line in file:
            data.append(line.strip())
    string = "".join(data)
    lista = re.split("@", string)

    nueva = []
    for el in lista:
        if not (bool(re.search('[0-9]', el))):
            nueva.append(el)

    new = []
    for el in range(len(nueva)):
        if not (bool(re.search('\.incorrecta', nueva[el]))):
            if bool(re.search('\.correcta', nueva[el])):
                nueva[el] = re.sub(".correcta", "", nueva[el])
        new.append(nueva[el])
    pos = new.index('De.be')
    aux = []
    for el in range(pos, len(new)):
        if bool(re.search('[a-z]+\.{1}', new[el])):
            new[el] = re.sub("\.", "", new[el])
            aux.append(new[el])
    new = new[:pos] + aux
    return " ".join(new)


if __name__ == '__main__':
    print(limpiar())
    print()
    print()
    # Solo no podemos limpiar las palabras que tienen "correcta" mal escrito y
    # dos puntos

    while True:
        print("PrograPedia:")
        try:
            a = input("Eliga una palabra para hacer busqueda (exit para salir)"
                      ":").strip(

            ).lower()
            if a=="exit":
                break
            print(revisar_datos(a))
        except Exception as err:
            print("Ingresar palabra valida")
