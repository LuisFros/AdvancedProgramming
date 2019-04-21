import os
from json import dump, load


def escribir_constantes(nombre, diccionario):
    json = r"{}".format("constantes.json")
    if not os.path.exists(json):
        with open("{}".format("constantes.json"), "w") as arch:
            print("{}".format("constantes.json"))
            json_data = {}
            dump(json_data, arch, indent=4)
    else:
        with open("{}".format("constantes.json"), "r") as file:
            json_data = load(file)
        if nombre not in json_data:
            json_data[nombre] = diccionario
        else:
            json_data[nombre].update(diccionario)
        with open("{}".format("constantes.json"), "w") as arch:
            dump(json_data, arch, indent=4)


def main():
    Subditos_debiles = {"life": 45, "initial_pos": (255, 225),
                        "movement_speed": 8, "attack_damage": 2,
                        "attack_speed": 1, "attack_range": 5}

    Subditos_fuertes = {"life": 50, "initial_pos": (0, 0),
                        "movement_speed": 8, "attack_damage": 4,
                        "attack_speed": 1, "attack_range": 20}
    Hechicera = {"life": 500, "initial_pos": {"blue": (300, 215), "purple": (
        929, 470)},
                 "movement_speed": 30, "attack_damage": 5,
                 "attack_speed": 10, "attack_range": 40, "cooldown":
                     30, "ability_power": 0}
    Destructor = {"life": 666, "initial_pos": {"blue": (300, 215), "purple": (
        929, 470)},
                  "movement_speed": 10, "attack_damage": 20,
                  "attack_speed": 10, "attack_range": 5, "cooldown": 40,
                  "ability_power": 70}
    Rouge = {"life": 550, "initial_pos": {"blue": (300, 215), "purple": (
        929, 470)}, "movement_speed": 30,
             "attack_damage": 7, "attack_speed": 20, "attack_range": 10,
             "cooldown": 25}
    Torre = {"life": 250, "initial_pos": (0, 0), "attack_damage": 30,
             "attack_speed": 1, "attack_range": 40}
    Inhibidor = {"life": 600, "initial_pos": (0, 0), "cooldown": 30}
    Nexo = {"life": 1200, "initial_pos": (0, 0)}
    temp = [("Subditos_debiles", Subditos_debiles), ("Subditos_fuertes",
                                                     Subditos_fuertes),
            ("Hechicera", Hechicera), ("Destructor", Destructor),
            ("Rouge", Rouge),
            ("Torre", Torre), ("Inhibidor", Inhibidor), ("Nexo", Nexo)]
    for tupla in temp:
        escribir_constantes(tupla[0], tupla[1])


if __name__ == '__main__':
    main()
