from datetime import datetime
from ia.ia_adversaria import IA
import time

class ControlTurnos:
    def __init__(self, modo_juego):
        self.turno_actual = 'R'  # Rojo siempre inicia
        self.historial = []
        self.modo_juego = modo_juego  # Ej: "HUMANO_IA"
        self.ia_roja = None
        self.ia_negra = None

        if modo_juego != "HUMANO_HUMANO":
            self.ia_negra = IA(color_ia='N')
            if modo_juego == "IA_IA":
                self.ia_roja = IA(color_ia='R')
                self.ia_negra = IA(color_ia='N')

    def es_turno_humano(self):
        if self.modo_juego == "HUMANO_IA":
            return self.turno_actual == 'R'  # Humano es Rojo
        elif self.modo_juego == "HUMANO_HUMANO":
            return True
        elif self.modo_juego == "IA_IA":
            return False  # IA vs IA

    def manejar_turno_ia(self, tablero):
        """Método dedicado para turnos de IA. Devuelve (origen, destino) o None"""
        ia_actual = self.ia_roja if self.turno_actual == 'R' else self.ia_negra
        print(f"🤖 IA {self.turno_actual} pensando...")
        time.sleep(1)  # Pausa para visualización

        movimiento = ia_actual.mejor_movimiento(tablero)
        if movimiento:
            origen, destino = movimiento
            print(f"IA mueve: {chr(97 + destino[1])}{8 - destino[0]}")
            return origen, destino
        return None

    def cambiar_turno(self):
        self.turno_actual = 'N' if self.turno_actual == 'R' else 'R'

    def registrar_movimiento(self, origen, destino):
        self.historial.append({
            'turno': self.turno_actual,
            'origen': origen,
            'destino': destino,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })