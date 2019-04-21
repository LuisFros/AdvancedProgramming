

from collections import deque
class Camiones:
	def __init__(self,capacidad_max="",urgencia="",peso_actual=0):
		self.capacidad_max,self.urgencia,self.peso_actual=capacidad_max,urgencia,peso_actual

	def agregar_producto(self,producto):
		self.productos=[]
		while self.peso_actual+producto.peso<=int(self.capacidad_max):
			self.productos.append(producto)
			suma+=producto.peso
		return True
	def __str__(self):
		productos_dict={}
		for producto in self.productos:
			if producto.nombre not in productos_dict:
				productos_dict[prodcto.tipo]=0
			else:
				productos_dict[producto.tipo]+=1
		for producto in productos_dict:
			print(tipo,productos_dict[tipo])
		# return tipo + cantidad

class CentroDistribucion:
	def __init__(self,fila,bodega={}):
		self.bodega=bodega
		self.fila=deque()
	def rellenar_camion(self,camion):
		camion.agregar_producto()
		pass
	def recibir_camion(self,camion):
		salida=open("camiones.txt","a",encoding="utf-8")
		print("{},{},{}".format(camion.capacidad_max,camion.urgencia))

		pass
	def enviar_camion(self):
		primero=self.fila[0]
		if rellenar_camion(primero):
			self.fila.popleft()
		else:
			rellenar_camion(primero)

	def mostrar_productos(self,tipo):
		for tipo in self.bodega:
			print(tipo,self.bodega[tipo])

	def recibir_donacion(self,*args):
		salida=open("productos.txt","a",encoding="utf-8")
		for producto in args:
			print("{},{},{}".format(producto.nombre,producto.tipo,producto.peso),file=salida)
			if producto.tipo not in self.bodega:
				self.bodega[producto.tipo]=0
			else:
				self.bodega[producto.tipo]+=1


class Producto:
	def __init__(self,nombre,tipo,peso):
		self.nombre,self.tipo,self.peso=nombre,tipo,peso
def leer_productos():
	producto={}
	productos=open("productos.txt",encoding="utf-8")
	salida=open("productos.txt","w",encoding="utf-8")
	leido=productos.readlines()
	primer_producto=linea[0].strip("\n").split(",")
	producto["nombre"]=primer_producto[0]
	producto["tipo"]=primer_producto[1]
	producto["peso"]=primer_producto[2]
	p=Producto(**producto)
	for linea in lista[1:]:
		print("{},{},{}".format(producto.nombre,producto.tipo,producto.peso),file=salida)		
	return p
def leer_camiones():
	camiones=open("camiones.txt",encoding="utf-8")
	leido=camiones.readlines()
	leido=[i.strip("\n").split(",") for i in leido]
	ordenado=sorted(leido[1:],key=lambda x:int(x[1]),reverse=True)

	






c=Camiones()

producto=leer_productos()

leer_camiones()


# for producto in lista_productos:
# 	c.agregar_producto(producto)
# 	print(c)
# print(lista_camiones)