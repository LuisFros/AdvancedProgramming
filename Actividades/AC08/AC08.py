__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
#Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
#será penalizada con nota 1.0


class MetaPerson(type):
    def __new__(cls, name, bases, dic):
        if name == "Chef":
            def cook(ins):
                plate = Plate()
                print("cooking...")
                dic["choose_food"](cls, plate)
                dic["choose_drink"](cls, plate)
                return plate

            dic["cook"] = cook
            dic["restaurante"] = None

            if "Person" not in bases:
                bases = (Person,)

        elif name == "Client":
            def eat(ins, plate):
                if isinstance(plate.drink, Drink):
                    if isinstance(plate.food, Food):
                        calidad = plate.food.quality + plate.drink.quality
                        if calidad >= 50:
                            print("Que delicia!")
                        else:
                            print("Esto no es digno de mi palabra")
                    else:
                        print("Mi plato tiene dos comidas")
                else:
                    print("Mi plato tiene dos bebidas")
            dic["eat"] = eat
            if "Person" not in bases:
                bases = (Person,)
        return super().__new__(cls, name, bases, dic)


    def __call__(cls, *args, **kwargs):

        return super().__call__(*args, **kwargs)
class MetaRestaurant(type):
    todos_chefs=[]
    todos_clientes=[]
    def __new__(meta, name, bases, dic):
        dic["llega_cliente"]=None
        dic["cliente_se_va"]=None
        dic["chefs"]={}
        return super().__new__(meta, name, bases, dic)
    def __init__(clase,name,bases,dic):
        
        def llega_cliente(self,persona):
            if isinstance(persona,Cliente):
                self.clients.append(persona)
        dic["llega_cliente"]=llega_cliente
        def cliente_se_va(self,persona):
            nombre=persona.name
            for cliente in self.clients:
                if cliente.name==nombre:
                    self.clients.remove(cliente)
                    break
        dic["cliente_se_va"]=llega_cliente
        for i in dic["chefs"]:
            MetaRestaurant.todos_chefs.append(i)
        super().__init__(name,bases,dic)
    def __call__(clase,*args,**kwargs):
        funcion=getattr(clase,"start")
        nombre=None
        if len(args)>=2:
            chefs={i.name:i for i in args[1]}
            if len(args)==3:
                nombre = args[0]
                chefs = args[1]
                clientes = args[2]
            else:
                nombre=args[0]
                chefs=args[1]
                clientes = []
                print("El",nombre,"no tiene clientes, que pena")
            print("Instanciacion exitosa ,chefs contratados: ")
            for chef in chefs:
                print(chef.name)
        if nombre:
            return super().__call__(nombre, chefs, clientes)
    
            


###############################################################################
#De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients


    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass = MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients


    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
                Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
