# Tarea 04

Para el Tareo:
-La aplicacion de simulacion me parecio muy interesante, por lo que la tarea la realize con bastante tiempo pero por razones logistica hubieron ciertos aspectos de la tarea que no pude implementar y me gustaria ahorrarte el trabajo de darte cuenta por ti mismo:

-----------------------------------------------------------------------------------
# Lo que me falto :(

- Dr.Mavrakis desgraciadamente no forma parte de la simulacion.
- Los distintos escenearios en "escenarios.csv", no se pudieron entregar de manera correcta, llegue hasta el punto de entregarle el objeto "escenarios" a cada simulacion pero no el "unpacking" de este objeto para cambiar la simulacion.
- Al momento de entregar, hay algunos comentarios que deberia haber eliminado y no me di cuenta. (error mio por tenerlos de color gris y no se leen)
- Lo que mas me disculpo, es que no implemente el tipo de documentacion que fue pedido. Estuve muy ocupado tratando de hacer que la simulacion este funcionando correctamente y solo al final me di cuenta que me falto documentar.Por esto, agregare una seccion en el readme, donde tratare de explicar algunas funcionalidades para que no haya inconvenientes. Me disculpo por causar mas dificultad al leer mi tarea.
- Las estadisticas finales no estan completas, se entrega solo informacion parcial.
- No implemente el grafico que pedian, esto consecuente con la linea anterior
- Siguiendo a pie de letra, las formulas indicadas en el enunciado y las probabilidades necesarias, muchos terminan "botando" el ramo, por lo que la simulacion termina antes de lo normal. Facilmente esto se puede evitar bajando las exigencias pero eso no estaba especificado en el enunciado y no quise hacer ningun supuesto poco fundamentado.
## Guia General:
 1) Para correr la simulacion, correr el archivo [main.py](main.py)  (Estos links si funcionan!)
 2) Gran parte de las funciones usadas son importadas de [Funcional.py](Funcional.py)
 3) "escenarios.csv" es manejado mediante el archivo [Analisis.py](Analisis.py) 
  y la creacion del grafo de conexiones.


## Extra por no tener documentacion:

##### Hay ciertas cosas que deberia aclarar, ya que la documentacion no esta presente en el codigo y me siento obligado a hacer algo para reponer ese error:
- Al instanciar a las clases principales desde "integrantes.csv", aproveche mi conociemiento de metaclases y los atributos de agregaban de manera dinamica aprovechando el hecho de que la primera fila tenia los "nombres" de los atributos que tendran los objetos. 

-       self.__dict__.update(**kwargs)
- Algunos eventos se pueden pre-definir antes de iniciar la simulacion ya que la ocurrencia de ellos es constante o simplemente se puede obtener de manera probabilistica, pero otros como las Tareas, se tuvieron que ir agregando a mediados que avanzaban las semanas ya que estaba la posibiilidad de un cambio de fechas.
- En el archivo [Funcional.py](main.py), se manejaron los eventos que ocurrian y como los objetos cambiaban en el tiempo. Esto se llevo a cabo mediante una combinacion de "one-linesr" de map() y decoradores que recibian los objetos (alumnos, profesores etc.) y retornaban estos mismos despues de haberlos cambiado. Esto se hizo, ya que los "lambda" no puede asignar atributos a objetos en python y encontre que esto era una manera dinamica de hacer el trabajo.
- La funcion "evaluar_evento" en [main.py](main.py) es la que evalua los eventos segun el string de la lista_eventos y entrega la instancia de simulacion.
-       def evaluar_evento(evento, simulacion):
- La clase "DiccRango", se creo con el proposito de evitar tener un gran numero de llaves y "explotar" las funcionalidades que tienen los diccionaries.
-       class DiccRango(dict)
