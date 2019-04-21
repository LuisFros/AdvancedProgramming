from gui.Gui import MyWindow
from PyQt5 import QtWidgets
from itertools import chain
import sys
from datos import mega_dict
import os
import datetime

funciones = mega_dict()
# generan el numero de consultas
consultas = (el for el in range(9999999999))


class T03Window(MyWindow):

    def __init__(self):
        self.variables = {}
        super().__init__()

    def process_consult(self, querry_array):
        try:
            def asignar(variable, otro):
                if variable not in self.variables.keys():
                    self.variables.update({variable: otro})
            funciones.update({"asignar": asignar})

            def evaluar_comando(evento):
                if evento[0] == "evaluar":
                    self.variables.update(
                        {"aux": [evento[0], evento[2], evento[3], evento[4]]})
                if (type(evento) == type([]) or type(evento) == type((lambda x: x))) and type(evento[0]) != type(1.5):
                    otro_nivel = list(
                        filter(lambda x: type(x) == type([]), evento))
                    if len(otro_nivel) == 0:
                        variables_instanciadas = {idx: self.variables[
                            valor] for idx, valor in enumerate(evento) if valor in self.variables}
                        todo_menos_variables = {idx: valor for idx, valor in enumerate(
                            evento) if valor not in self.variables}
                        variables_instanciadas.update(todo_menos_variables)
                        lista = list(variables_instanciadas.values())
                        # No es neseario ordenar la lista de valores, porque
                        # por default los indices se ordenan en el dict !
                        return funciones[lista[0]](*lista[1:])
                    else:
                        return evaluar_comando(otro_nivel[0])
                else:
                    return evento

            def evaluar_comando_limpio(evento):
                if evento[0] != "asignar" and (type(evento[1]) == type("string") or type(evento[1]) == type((lambda x: x))):
                    variables_instanciadas = {idx: self.variables[
                        valor] for idx, valor in enumerate(evento) if valor in self.variables}
                    todo_menos_variables = {idx: valor for idx, valor in enumerate(
                        evento) if valor not in self.variables}
                    variables_instanciadas.update(todo_menos_variables)
                    lista = list(variables_instanciadas.values())

                    # No es neseario ordenar la lista de valores, porque por
                    # default los indices se ordenan en el dict !
                    return funciones[lista[0]](*lista[1:])
                if evento[0] == "asignar" and type(evento[2]) == type((lambda x: x)):
                    temp = self.variables["aux"]
                    a_evaluar = [evento[2], temp[1], temp[2], temp[3]]
                    evento[2] = funciones["evaluar"](*(a_evaluar))
                return funciones[evento[0]](*evento[1:])

          

            start = datetime.datetime.now()
            a = [list(map(evaluar_comando, el)) for el in querry_array]
            solucion = [evaluar_comando_limpio(i) for i in a]
            if solucion[0] is not None and len(solucion) > 1:
                mensaje = str(a[0]) + str(solucion[0][0]) + "\n"
            elif str(a[0][0]) == "asignar":
                mensaje = str(a[0][1]) + "-->Asignado exitosamente" + "\n"
            else:
                mensaje = str(a[0][0]) + "-->" + str(solucion[0]) + "\n"
            self.add_answer(mensaje)
            if not os.path.exists("resultados.txt"):
                typo = "w"
            else:
                typo = 'a'
            with open("resultados.txt", typo, encoding="utf-8") as archivo:
                archivo.write(
                    "---------------Consulta{}---------------\n".format(next(consultas)))
                archivo.write("".join(map(str, querry_array)) + "\n")
                archivo.write(mensaje + "\n")
                archivo.write(
                    "[" + str(((datetime.datetime.now() - start).microseconds) / 1000000) + "s" + "]" + "\n")
        except Exception as err:
            print(err)
            if not os.path.exists("resultados.txt"):
                typo = "w"
            else:
                typo = 'a'
            with open("resultados.txt", typo, encoding="utf-8") as archivo:
                archivo.write(err + "\n")

    def save_file(self, querry_array):
        print(querry_array)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
