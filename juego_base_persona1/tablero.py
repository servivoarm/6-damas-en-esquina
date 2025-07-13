# archivo: juego_base/tablero.py

class Tablero:
    def __init__(self):
        self.filas = 8
        self.columnas = 8
        self.tablero = [['.' for _ in range(self.columnas)] for _ in range(self.filas)]
        self.colocar_fichas_iniciales()

    def colocar_fichas_iniciales(self):
        # Fichas rojas en esquina superior izquierda
        posiciones_rojas = [(1, 0), (0, 1), (3, 0), (2, 1), (1, 2), (0, 3)]
        for fila, col in posiciones_rojas:
            self.tablero[fila][col] = 'R'

        # Fichas negras en esquina inferior derecha
        posiciones_negras = [(7, 6), (6, 7), (7, 4), (6, 5), (5, 6), (4, 7)]
        for fila, col in posiciones_negras:
            self.tablero[fila][col] = 'N'

    def imprimir_tablero(self):
        print("  a b c d e f g h")
        for i, fila in enumerate(self.tablero):
            print(f"{8 - i} " + ' '.join(fila) + f" {8 - i}")
        print("  a b c d e f g h")

    def es_movimiento_valido(self, origen, destino, color):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        # Verifica que destino esté dentro del tablero
        if not (0 <= fila_destino < self.filas and 0 <= col_destino < self.columnas):
            return False

        # El destino debe estar vacío
        if self.tablero[fila_destino][col_destino] != '.':
            return False

        # Movimiento diagonal (1 o 2 espacios)
        delta_fila = fila_destino - fila_origen
        delta_col = col_destino - col_origen

        if abs(delta_col) != abs(delta_fila):
            return False
        if abs(delta_fila) not in (1, 2):
            return False

        # Dirección correcta según color
        if color == 'R' and delta_fila <= 0:
            return False
        if color == 'N' and delta_fila >= 0:
            return False

        return True

    def mover_ficha(self, origen, destino):
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        ficha = self.tablero[fila_origen][col_origen]

        if ficha not in ('R', 'N'):
            print("No hay ficha del jugador en la posición origen.")
            return False

        if not self.es_movimiento_valido(origen, destino, ficha):
            print("Movimiento inválido.")
            return False

        # Realiza el movimiento
        self.tablero[fila_destino][col_destino] = ficha
        self.tablero[fila_origen][col_origen] = '.'
        print(f"Ficha {ficha} movida de {origen} a {destino}")
        return True

    def hay_ganador(self):
        zona_objetivo_rojas = [(7, 6), (6, 7), (7, 4), (6, 5), (5, 6), (4, 7)]
        zona_objetivo_negras = [(1, 0), (0, 1), (3, 0), (2, 1), (1, 2), (0, 3)]

        gana_rojas = all(self.tablero[f][c] == 'R' for f, c in zona_objetivo_rojas)
        gana_negras = all(self.tablero[f][c] == 'N' for f, c in zona_objetivo_negras)

        if gana_rojas:
            return 'R'
        elif gana_negras:
            return 'N'
        else:
            return None
