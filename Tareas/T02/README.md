# <README> Tarea 02
Para el Ayudante:
Primero que todo, espero que se divierta probando el juego que programe! Estuvo muy entretenida la tarea.

Lets get serious:

Este es el README de la tarea 02, en la cual se llevo a cabo la programacion del juego "Pandemic".Para el lector, estos fueron los puntos que no se puedieron implementar:
  - Poder recuperar la informacion completa de la partida anterior (no se guardan quienes fueron los paises infectados, solo la poblacion infectada/muerta y los dias trascurridos.
  - El avance de la infeccion no funcionaba bien siguiendo las probabilidades del enunciado (incluyendo los cambios de enunciado min/max). Pero si se implementaron todas la probabilidades
 
-----------------------------------------------------------------------------------
# Codigos Relevantes

##### Modulo funciones.py

```sh
>def buscar_entero(decimal, x=0):
>return buscar_entero(decimal * 10**x, x) * 10**-x
```
Explicacion:
- Esta funcion, lo que busca es encontrar una representacion de un decimal como entero a partir de un probabilidad.
- Estos con base 10**3, 

Por ejemplo:
```sh
>>buscar_entero(0.002)
>>2
>>buscar_entero(0.02)
>>20
>>buscar_entero(0.981)
>>981
```
Se creo con el solo proposito de que las probabilidades no sean despreciables y se hizo de modo recursivo por optimizar tiempo de ejecutacion.
Este es un supuesto que hice para que fuera mas posibles los eventos

Seguimos en el mismo modulo,,
Con un poco de inspiracion, escribi esta funcion
```sh
>>def evento_ocurra(prob):
>>return boolean
```
Esta es mi version de __simulacion__ de probabildades aleatorias,
Esto es lo que hace:
 - Recibe el numero entero generado por la funcion explicada en la pagina anterior
 - Crea una lista llamada __"lista_imposible"__, la cual tiene 1000 elementos que incialmente son todos de tipo *None*
 - Despues, se agrega con un randint(0,999) en el rango del numero entero, una posicion *True* en para reemplazar algun *None* suertudo.
 - El ultimo paso (que ojala se explique por si solo cuando corra el codigo), es que se toma una posicion aleatoria y ver si esa contiende a un *True* para ver si la probabilidad ocurre
 - Preferi este metodo porque se pueden aprovechar las estructuas que creamos, como mi *class ListaLigada():* para simular probabilidades y me parecio divertido llevarlo a mis propias manos en vez de solo utilizar "random.uniform(0.1)"

---
##### Modulo menu.py

- Aprovechando mi conocimiento de funcional, este modulo fue dedicado a crear la interaccion con el usuario con loops de input.
- Tambien se debe notar que se utilizaron map() y filter() con el proposito de reducir las lineas de codigo necesarias para realizar ciertas operaciones en estructuras de datos.__(Estos generadores nunca son entregados a una estructura prohibida por enunciado)__
---
##### Modulo main.py
- En este modulo se ecuentra la creacion de objetos y la creacion del grafo de conexiones.

### **[IMPORTANTE]**
```sh
>>import csv
>>from estructuras import Nodo, ListaLigada, ColaPrioridades
>>#from probabilities import Probabilidades, randint
>>from probabilities2 import Probabilidades, randint
>>from funciones import promedio_fronteras, evento_ocurra, buscar_entero
```
- Se creo un modulo llamado ``` probabilities2.py```, que cumple con el proposito de testing, el cual tiene valor de probabilides mayor los cuales hace que los evento ocurran con mayor frequencia. El **original** segun enunciado es ``` probabilities.py```. Asi que porfavor, solo importar uno de ellos para correr el juego.
---
### Modulo estructuras.py
Resumen: 
- Se creo una ``ListaLigada`` uni-direccional contendiendos elementos tipo ``Nodo``, (*Uni-direccional*:Nodos con referencia al siguiente valor). 
- Tambien, heredando de la clase recien mencionada, se creo la```ColaPrioridades(ListaLigada)```, la cual tienen metodos para retornar las prioridades y modificarse a si misma al mismo tiempo.

Metodos a explicar:
#### 1)
```sh
>>def __iter__(self):
    actual = self.cabeza
    while actual is not None:
        yield actual.valor
        actual = actual.siguiente
```
- Metodo MUY importante, es lo que permite que que la lista sea un **iterable**. Esto se hace mediante yields de una funcion generadora.

#### 2)
```sh
>>def __getitem__(self):
...
return nodo.valor
```
- Metodo que permite la indexacion de elementos mediante el uso de [indice], tambien se puede tener una lista con solo este metodo y sin **"iter"** pero esta lista seria una iterable "falsa".

#### 3)
```sh
>>def __siguiente__(self):
        return self.cabeza.siguiente
```
- Permite iterar sobre si mismo
#### 4)
```sh
>>def __len__(self):
...
return largo
>>a=ListaLigada(1,2)
>>a
[1,2]
>>len(a)
2

```
- En este metodo se recorren los Nodos pertenecientes a la lista ligada, gracias a que esta es iterable con un for y retorna el largo de la lista.

### 5)
```sh
>>def __contains__(self, valor):
...
return boolean
>>a=ListaLigada(1,2)
>>a
[1,2]
>>print(1 in a)
True
```
- Permite usar el "sugar syntax" if x "in":

### 6)
```sh
>>def __setitem__(self, valor):
...
>>a=ListaLigada(1,2)
>>a
[1,2]
>>a[0]="Funciona?"
>>a
["Funciona?",2]
```
- Se puede sobre-escribir un valor dado su indice dentro de la lista.


### 7)
```sh
>>def clear(self):
        self = ListaLigada()

```
- Este es un metodo unico, pero util que vacia la lista para alguna utilidad en el futuro. (futuro cercano ```ColaPrioridades```)

### 8)
```sh
>>def delete(self,valor):
...
>>a
[1,2]
>>a.delete(2)
>>a
[1]

```
- Como lo dice su nombre, se borra de la existencia del planeta el valor entregado.
- Esto aprovechando los atributos de los nodos y entregandoles un valor vacio al valor buscado.

### 9)
```sh
>>def __gt__(self, other):
    return self[1] > other[1]
>>b=ListaLiagada(ListaLigada("Este es mayor que",10),ListaLigada("Este",2))
>>b
[["Este es mayor que",10],["Este",2]]
>>print(b[0]>b[1])
True
```

- Se sobre escriba el operador > de la lista, comparando solo la posicion [1] de la lista, con el proposito de utilizarlo en la siguiente clase

Ahora en ```ColaPrioridades(ListaLigada)```:

### 10)
```sh
>>def insert(self,valor):
    ...
    return
...
>>ordenada=ColaPrioridades()
>>ordenada.insert(["Mediano",199"])
>>ordenada.insert(["Mayor",123123"])
>>ordenada.insert(["random",2312"])
>>ordenada
[["Mediano",199"],["random",2312"],["Mayor",123123"]]
```
- De manera ingeniosa, se utilizo un algoritmo de busqueda comparando los valores de los nodos en la posicion actual, con esto se insertan los valores de manera ordenado aprovechando el operador **">"** sobre-escrito en **8)**

### 11)
```sh
>>def crear_cola(self, Pais, paises_conectados, progreso_cura):
....
   self.insert(..)
```
- Crea una cola dependiendo de la prioridad de cada accion del gobierno, de manera ordenada, aprovechando insert()

### 12)
```sh
>>def primeros_tres(self)
....
   return temp
```
- Retorna las primeras tres acciones del gobierno, que estaban primeras en la cola ordeanada, este tiene condiciones si el largo es >3, se debe eliminar los elementos con ```self.delete(valor)``` en caso contrario se usa ```self.clear()``` porque no sobran elementos en la cola.





