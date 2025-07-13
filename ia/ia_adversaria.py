import math
import random
from juego_base_persona1.tablero import Tablero

class IA:
    def __init__(self, color_ia='N', dificultad=3):
        # Color que controla esta IA ('N' o 'R')
        self.color_ia = color_ia
        # Profundidad máxima del algoritmo Alpha-Beta
        self.dificultad = dificultad

    def mejor_movimiento(self, tablero):
        # Ejecuta algoritmo Alpha-Beta para encontrar el mejor movimiento
        _, movimiento = self.alpha_beta(tablero, self.dificultad, -math.inf, math.inf, True)

        # Verifica que el movimiento sea válido antes de devolverlo
        if movimiento and tablero.es_valido(movimiento[0], movimiento[1], self.color_ia):
            return movimiento
        return None

    def alpha_beta(self, tablero, profundidad, alpha, beta, es_maximizando):
        # Condición de parada: profundidad 0 o hay ganador
        if profundidad == 0 or tablero.hay_ganador():
            return self.calcular_heuristica(tablero), None

        # Determina color del jugador según si está maximizando o minimizando
        color = self.color_ia if es_maximizando else ('R' if self.color_ia == 'N' else 'N')

        # Genera y aleatoriza movimientos válidos
        movimientos = self.generar_movimientos_validos(tablero, color)
        random.shuffle(movimientos)

        mejor_mov = None

        if es_maximizando:
            max_eval = -math.inf
            for mov in movimientos:
                # Simula el movimiento en una copia del tablero
                tablero_copia = self.copiar_tablero(tablero)
                tablero_copia.mover_ficha(mov[0], mov[1])

                # Llamada recursiva como minimizador
                eval, _ = self.alpha_beta(tablero_copia, profundidad - 1, alpha, beta, False)

                # Actualiza mejor evaluación y movimiento si mejora
                if eval > max_eval:
                    max_eval = eval
                    mejor_mov = mov

                # Actualiza alpha
                alpha = max(alpha, eval)

                # Poda: termina si beta <= alpha
                if beta <= alpha:
                    break

            return max_eval, mejor_mov
        else:
            min_eval = math.inf
            for mov in movimientos:
                # Simula el movimiento en una copia del tablero
                tablero_copia = self.copiar_tablero(tablero)
                tablero_copia.mover_ficha(mov[0], mov[1])

                # Llamada recursiva como maximizador
                eval, _ = self.alpha_beta(tablero_copia, profundidad - 1, alpha, beta, True)

                # Actualiza mejor evaluación y movimiento si mejora
                if eval < min_eval:
                    min_eval = eval
                    mejor_mov = mov

                # Actualiza beta
                beta = min(beta, eval)

                # Poda: termina si beta <= alpha
                if beta <= alpha:
                    break

            return min_eval, mejor_mov

    def calcular_heuristica(self, tablero):
        # Evalúa el tablero: mientras más cerca estén las fichas de la IA de su zona objetivo, mayor la puntuación
        puntaje = 0

        # Define las posiciones objetivo según el color de la IA
        zona_objetivo = (
            [(1, 0), (0, 1), (3, 0), (2, 1), (1, 2), (0, 3)] if self.color_ia == 'N'
            else [(7, 6), (6, 7), (7, 4), (6, 5), (5, 6), (4, 7)]
        )

        for fila in range(8):
            for col in range(8):
                # Si encuentra una ficha de la IA
                if tablero.tablero[fila][col] == self.color_ia:
                    # Calcula la distancia a la zona objetivo más cercana
                    dist_min = min(abs(fila - f_obj) + abs(col - c_obj) for f_obj, c_obj in zona_objetivo)
                    # A mayor cercanía, mayor puntaje
                    puntaje += (10 - dist_min)
        return puntaje

    def generar_movimientos_validos(self, tablero, color):
        # Devuelve una lista con todos los movimientos válidos posibles para un color dado
        movimientos = []
        for fila in range(8):
            for col in range(8):
                # Si encuentra una ficha del color indicado
                if tablero.tablero[fila][col] == color:
                    # Explora posibles direcciones de movimiento (diagonales normales y de salto)
                    for df, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1), (2, 2), (2, -2), (-2, 2), (-2, -2)]:
                        destino = (fila + df, col + dc)
                        # Verifica que el destino esté dentro del tablero
                        if 0 <= destino[0] < 8 and 0 <= destino[1] < 8:
                            # Verifica si el movimiento es válido
                            if tablero.es_valido((fila, col), destino, color):
                                movimientos.append(((fila, col), destino))
        return movimientos

    def copiar_tablero(self, tablero):
        # Crea una copia profunda del tablero actual
        nuevo = Tablero()
        nuevo.tablero = [fila.copy() for fila in tablero.tablero]
        return nuevo
