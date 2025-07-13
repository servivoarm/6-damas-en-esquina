# archivo: main.py

from juego_base_persona1.tablero import Tablero

def coordenada_a_indices(coord):
    letras = 'abcdefgh'
    try:
        col = letras.index(coord[0].lower())
        fila = 8 - int(coord[1])
        return (fila, col)
    except:
        return None

def main():
    tablero = Tablero()
    turno_actual = 'R'

    while True:
        tablero.imprimir_tablero()
        print(f"\nTurno de {'Rojo' if turno_actual == 'R' else 'Negro'} ({turno_actual})")

        origen_input = input("Selecciona ficha a mover (ej: a7): ")
        destino_input = input("Selecciona destino (ej: b6): ")

        if origen_input.lower() == "salir" or destino_input.lower() == "salir":
            print("Juego terminado.")
            break

        origen = coordenada_a_indices(origen_input)
        destino = coordenada_a_indices(destino_input)

        if not origen or not destino:
            print("Coordenadas inválidas. Usa formato como a7, b6, etc.\n")
            continue

        ficha_en_origen = tablero.tablero[origen[0]][origen[1]]

        if ficha_en_origen != turno_actual:
            print(f"Debes mover una ficha {turno_actual}. Esa no te pertenece.\n")
            continue

        if tablero.mover_ficha(origen, destino):
            ganador = tablero.hay_ganador()
            if ganador:
                print(f"\n¡Jugador {ganador} ha ganado la partida!")
                tablero.imprimir_tablero()
                break

            # Cambiar turno
            turno_actual = 'N' if turno_actual == 'R' else 'R'
        else:
            print("Movimiento no válido. Intenta de nuevo.\n")

if __name__ == "__main__":
    main()
