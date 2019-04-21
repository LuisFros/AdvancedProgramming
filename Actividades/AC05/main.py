import test

class CustomException(Exception):
    def __init__(self, lista=None):
        for caracter in lista:
            if caracter=="a":
                indice=lista.index("a")
                lista_invertida=lista[indice:][::-1]
                lista_final=lista[:indice]+lista_invertida[:-1]
                self.lista=lista_final
        super().__init__()
    
        
class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                self.codigo += caracter

            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            if len(i) < 6 or len(i) > 7:
                pass
                #raise CustomException
            else:
                self.codigo+=' '+i
       
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto


    def limpiador(self, lista):
        i = -1
        string = ''
        while i < len(lista):
            i += 1
            if '$' != lista[i]:
                raise CustomException(lista)
                string += lista[i]
        return string

if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        codigo= des.lectura_archivo()
        codigo=des.elimina_incorrectos()
        lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
    except CustomException as err:
        nueva=err.lista
    # texto = des.limpiador(nueva)
    
    test.main()


