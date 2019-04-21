from archivos import start_archivos
from menu import crear_menu, crear_tiempo
from logica import convertir_tiempo_clima, convertir_tiempo_incendios, estado_actual_incendio, calcular_area


recursos, meteorologia, usuarios, incendios = start_archivos()


def main():
    main = crear_menu()
    convertir_tiempo_clima()
    convertir_tiempo_incendios()
    estado_actual_incendio(menu, 1)
    calcular_area(1,incendios,meteorologia)
    return

if __name__ == '__main__':
    main()


