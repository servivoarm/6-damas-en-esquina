from juego_base_persona1.tablero import Tablero
from ia.control_turnos import ControlTurnos
from ia.ia_adversaria import IA
import time


#Tablero: Maneja la lógica y visualización del tablero de juego.

#ControlTurnos: Controla de quién es el turno, si es IA o humano, y lleva el historial de jugadas.

#IA: Clase que define el comportamiento de la inteligencia artificial.

#time: Biblioteca estándar de Python para trabajar con tiempos, aunque en este código no se usa directamente.

def coordenada_a_indices(coord):
    letras = 'abcdefgh'
    try:
        col = letras.index(coord[0].lower()) # Convierte letra (ej: 'a') a índice (0)
        fila = 8 - int(coord[1])             # Convierte número (ej: '7') a índice (1)
        return (fila, col)
    except:
        return None


def elegir_modo():
    print("\nSelecciona el modo de juego:")
    print("1. Humano vs IA")
    print("2. Humano vs Humano")
    print("3. IA vs IA")
    while True:
        opcion = input("Ingrese 1, 2 o 3: ")
        if opcion in {"1", "2", "3"}:
            return {"1": "HUMANO_IA", "2": "HUMANO_HUMANO", "3": "IA_IA"}[opcion]
        print("Opción inválida. Intenta de nuevo.")


def main():
    modo = elegir_modo() # Usuario elige el tipo de partida
    tablero = Tablero()  # Crea el tablero de juego
    control = ControlTurnos(modo)  # Prepara el controlador de turnos, IA incluidas si aplica


    while True:

        tablero.imprimir_tablero()#base en la cual se estara desarrollando el juego
        jugador_actual = "Rojo" if control.turno_actual == 'R' else "Negro"#esto solo es para definir cual jugador va de turno, si el jugador actual es el rojo, entonces sera el rojo
        print(f"\nTurno de {jugador_actual}")

        # Manejo de turnos
        if control.es_turno_humano():
            origen_input = input("Ingrese movimiento (ej: a7 b6): ")
            if origen_input.lower() == "salir": #en caso de querer parar el juego
                break
            try:
                coord_origen, coord_destino = origen_input.split() # esto es nuestra posicion actual hasta donde nos moveremos
                origen = coordenada_a_indices(coord_origen)
                destino = coordenada_a_indices(coord_destino)
                if origen is None or destino is None:
                    print("Coordenadas inválidas. Use formato como a7 b6")
                    continue
            except:
                print("Formato inválido. Ejemplo: a7 b6")
                continue
        else:
            #Si es el turno de una IA, se llama a su lógica. este es el caso.
            movimiento = control.manejar_turno_ia(tablero)
            if movimiento is None:#si es un movimiendo null o invalido que no entra en el formato del programa
                print(" La IA no encontró movimientos válidos")
                turnos_sin_movimiento += 1
                if turnos_sin_movimiento >= 2:
                    print("\nNinguno de los jugadores puede mover.Juego terminado por bloqueo. ")
                    break
                control.cambiar_turno()
                continue
            origen, destino = movimiento

        # Ejecutar movimiento
        if tablero.mover_ficha(origen, destino):
            control.registrar_movimiento(origen, destino)
            turnos_sin_movimiento = 0 #Si la IA no puede mover, se lleva un conteo. Si dos turnos seguidos no pueden moverse, el juego termina.
            if ganador := tablero.hay_ganador(): #como sabemos si es que ganamos? por una comparacion entre la posicion que tenemos entre el patron definido por Arlin
                tablero.imprimir_tablero()
                print(f"\n ¡{jugador_actual} ha ganado!")
                break
            control.cambiar_turno()
        else:
            print("Movimiento no válido. Intenta de nuevo.")

    print("\nHistorial de movimientos:")
    for i, mov in enumerate(control.historial, start=1):
        fila_o, col_o = mov['origen']#posicion origen
        fila_d, col_d = mov['destino']#posicion destino
        letra_o = chr(97 + col_o) # esto es una forma de convertir los indices a los numeros de columnas (este es origen)
        letra_d = chr(97 + col_d)#destino
        num_o = 8 - fila_o
        num_d = 8 - fila_d
        print(f"{i:02d}.  - {mov['turno']} movió de {letra_o}{num_o} a {letra_d}{num_d}")


if __name__ == "__main__":
    print("=== JUEGO DE 6 DAMAS EN ESQUINA ===")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido por el usuario.")