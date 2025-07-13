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

    def es_valido(self, origen, destino, color, verbose=False):  # Cambiar verbose=False por defecto
        fila_o, col_o = origen
        fila_d, col_d = destino

        # Validaciones silenciosas (sin prints)
        if not (0 <= fila_o < 8 and 0 <= col_o < 8 and 0 <= fila_d < 8 and 0 <= col_d < 8):
            return False
        if self.tablero[fila_o][col_o] != color or self.tablero[fila_d][col_d] != '.':
            return False

        delta_fila = fila_d - fila_o
        delta_col = col_d - col_o

        if abs(delta_col) != abs(delta_fila) or abs(delta_fila) not in (1, 2):
            return False
        if (color == 'R' and delta_fila <= 0) or (color == 'N' and delta_fila >= 0):
            return False

        return True  # Todas las validaciones pasaron

    def mover_ficha(self, origen, destino):
        if not self.es_valido(origen, destino, self.tablero[origen[0]][origen[1]]):
            return False

        # Movimiento silencioso
        ficha = self.tablero[origen[0]][origen[1]]
        self.tablero[destino[0]][destino[1]] = ficha
        self.tablero[origen[0]][origen[1]] = '.'
        return True

    def mover_ficha(self, origen, destino):
        fila_o, col_o = origen
        ficha = self.tablero[fila_o][col_o]

        if ficha not in ('R', 'N'):
            print("❌ No hay ficha seleccionable en la casilla de origen.")
            return False

        if not self.es_valido(origen, destino, ficha, verbose=False):
            print("⚠️ Movimiento no permitido.")
            return False

        # Movimiento válido
        fila_d, col_d = destino
        self.tablero[fila_d][col_d] = ficha
        self.tablero[fila_o][col_o] = '.'
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
