from funciones import distancia, direction
from random import choice
from PyQt5.QtCore import pyqtSignal, QObject


def generador_matriz1(largo, ancho):
    return {(i, j): Coordenada(i, j) for i in range(largo) for j in
            range(ancho)}


class GameEngine(QObject):
    _collision = pyqtSignal(tuple)

    def __init__(self):
        super(GameEngine, self).__init__()
        self.get_value_2 = (0, 0)

    def give_points(self, object):
        if object.tipo in ["Subditos_fuertes", "Subditos_debiles"]:
            return 1
        elif object.tipo in ["Inhibidor", "Torre"]:
            return 15
        else:
            return 5

    def get_value(self, val):
        if self.is_enemy(val["user"], val["target"]) and val[
            "user"].image.isVisible():
            if self.check_range(val["user"], val["origen"], val["destino"]):
                val["target"].disminuir_vida(val["user"].attack_damage)
                if val["target"].is_dead:
                    val["user"].kills += 1
                    val["user"].puntos += self.give_points(val["target"])

    @property
    def get_value_2(self):
        return self._get_value_2

    @get_value_2.setter
    def get_value_2(self, val):
        self._get_value_2 = val

    def mapa(self):
        return self.mapa

    @property
    def make_connection(self):
        return self._make_conection

    @property
    def make_connection_2(self):
        return self._make_conection_2

    @make_connection.setter
    def make_connection(self, front):
        self._make_conection = front._click.connect(self.get_value)
        if str(type(front.brain)) != "<class '__main__.Edificio'>":
            self._make_conection_2 = self._collision.connect(
                front.brain.collision)

    def is_enemy(self, obj_1, obj_2):
        if obj_1.team != obj_2.team:
            return True
        return False

    def aim(self, objeto, parent):

        team, position = objeto.team, objeto.position
        rango, damage = objeto.attack_range, objeto.attack_damage
        enemies = []
        validation = []
        for hijo in parent.children():
            if "brain" in hijo.__dict__ and hijo.brain.team != team and \
                    hijo.brain.isRunning() and hijo.isVisible():
                if hijo.brain.tipo == ("Nexo" or "Inhibidor"):
                    if hijo.isVisible():
                        validation.append(hijo.brain)
                else:
                    enemies.append(hijo.brain)
        if len(validation) == 2:
            aux = list(filter(lambda x: x.tipo == "Inhibidor", validation))
            enemies += aux
        elif len(validation) == 1:
            validation += validation

        elegido = min(enemies,
                      key=lambda x: distancia(position, x.position))
        if distancia(position, elegido.position) <= rango * 5:
            objeto.atacar(elegido)
            elegido.disminuir_vida(damage)

        return direction(position, enemies[0].position)

    def what_to_do(self, objeto, parent):
        for hijo in parent.children():
            if "brain" in hijo.__dict__ and hijo.brain.tipo in [ \
                    "Subditos_fuertes", "Subditos_debiles"] and \
                            objeto != hijo.thread and \
                    objeto.image.geometry().intersects(hijo.geometry()) and \
                            hijo.brain.team != objeto.team and \
                    hijo.brain.isRunning() and hijo.isVisible():
                self._collision.emit((0, 0))
                # elif "brain" in hijo.__dict__ and hijo.brain.tipo in [ \
                #         "Subditos_fuertes", "Subditos_debiles"] and \
                #                 objeto != hijo.thread and objeto.image.geometry().intersects(
                #     hijo.geometry()) and \
                #                 hijo.brain.team == objeto.team and \
                #         hijo.brain.isRunning():
                #     self.position=direction(objeto.position, hijo.brain.position)

    def check_range(self, attacker, origen, destino):
        if attacker.attack_range * 15 >= distancia(origen, destino):
            return True
        return False


class ShopEngine(QObject):
    def __init__(self, champ):
        super().__init__()
        self.champion = champ

    def Upgrade(self, precio, mejora):
        valor = float(precio.text().split(":")[-1])
        valor += (valor / 2)
        self.evaluar(mejora.text())
        precio.setText("Precio:{}".format(str(valor)))

    def evaluar(self, texto):
        if texto == "#daño+5":
            self.champion.attack_damage += 5
        elif texto == "#rango+2":
            self.champion.attack_range += 2
        elif texto == "#velocidad+3":
            self.champion.movement_speed += 3
        elif texto == "#habilidad+2":
            pass
        elif texto == "#vida+2":
            self.champion.life += 2
        else:
            self.evaluar(choice(["#rango+2", "#daño+5", "#velocidad+3",
                                         "#habilidad+2",
                                         "#vida+2"]))

