import pygame
import sys
import time

# Importar la lógica existente
from juego_base_persona1.tablero import Tablero
from ia.control_turnos import ControlTurnos
from ia.ia_adversaria import IA

# Dimensiones
WIDTH, HEIGHT = 640, 640
FPS = 30
MARGIN = 40  # espacio alrededor del tablero
CELL_SIZE = (WIDTH - 2 * MARGIN) // 8

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE_BG = (137, 207, 232)

# Ruta de los sonidos y fuentes
MOVE_SOUND_PATH = "assets/sound/move.wav"
DROP_SOUND_PATH = "assets/sound/drop.wav"
CUSTOM_FONT_PATH = "assets/fonts/8bitoperator_jve.ttf"


class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(CUSTOM_FONT_PATH, 32)

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()


class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Juego de 6 Damas en Esquina")
        self.menu_bg = pygame.image.load("assets/images/menu_bg.jpg").convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.mode = None
        self.buttons = []
        self.end_buttons = []
        self.running = True
        self.in_menu = True
        self.game_over = False
        self.selected = None
        self.winner = None
        self.ia_roja = None
        self.ia_negra = None
        self.turnos_sin_movimiento = 0

        # Cargar fuentes personalizadas
        self.font_28 = pygame.font.Font(CUSTOM_FONT_PATH, 28)
        self.font_36 = pygame.font.Font(CUSTOM_FONT_PATH, 36)
        self.font_48 = pygame.font.Font(CUSTOM_FONT_PATH, 48)
        self.font_52 = pygame.font.Font(CUSTOM_FONT_PATH, 52)

        self.setup_menu()

        # Inicializar el mixer y cargar sonidos
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound(MOVE_SOUND_PATH)
        self.drop_sound = pygame.mixer.Sound(DROP_SOUND_PATH)

        pygame.mixer.music.load("assets/sound/background.mp3")
        pygame.mixer.music.set_volume(0.18)
        pygame.mixer.music.play(-1)

    def setup_menu(self):
        btn_w, btn_h = 300, 60
        spacing = 20
        start_y = (HEIGHT - (3 * btn_h + 2 * spacing)) // 2 + 80

        def set_mode_h_i(): self.start_game('HUMANO_IA')

        def set_mode_h_h(): self.start_game('HUMANO_HUMANO')

        def set_mode_i_i(): self.start_game('IA_IA')

        self.buttons = [
            Button((WIDTH // 2 - btn_w // 2, start_y, btn_w, btn_h), "Humano vs IA", set_mode_h_i),
            Button((WIDTH // 2 - btn_w // 2, start_y + btn_h + spacing, btn_w, btn_h), "Humano vs Humano",
                   set_mode_h_h),
            Button((WIDTH // 2 - btn_w // 2, start_y + 2 * (btn_h + spacing), btn_w, btn_h), "IA vs IA", set_mode_i_i),
        ]

    def start_game(self, mode):
        self.mode = mode
        self.in_menu = False
        self.game_over = False
        self.selected = None
        self.winner = None
        self.turnos_sin_movimiento = 0
        self.tablero = Tablero()
        self.control = ControlTurnos(mode)
        self.ia_negra = IA(color_ia='N') if mode in ('HUMANO_IA', 'IA_IA') else None
        self.ia_roja = IA(color_ia='R') if mode == 'IA_IA' else None
        self.setup_end_buttons()

    def setup_end_buttons(self):
        btn_w, btn_h = 200, 50
        spacing = 20
        x = WIDTH // 2 - btn_w // 2
        y = HEIGHT // 2 + 20

        def volver():
            self.in_menu = True
            self.setup_menu()

        def salir():
            pygame.quit()
            sys.exit()

        self.end_buttons = [
            Button((x, y, btn_w, btn_h), "Volver al menú", volver),
            Button((x, y + btn_h + spacing, btn_w, btn_h), "Salir", salir)
        ]

    def draw_menu(self):
        self.screen.blit(self.menu_bg, (0, 0))  # Fondo del menú
        title_text = self.font_52.render("Juego de 6 Damas en Esquina", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        for btn in self.buttons:
            btn.draw(self.screen)
        pygame.display.flip()

    def draw_board(self):
        self.screen.fill(BLUE_BG)
        for row in range(8):
            for col in range(8):
                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE
                color = DARK_GRAY if (row + col) % 2 else GRAY
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pieza = self.tablero.tablero[row][col]
                if pieza in ('R', 'N'):
                    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    radius = CELL_SIZE // 2 - 5
                    pygame.draw.circle(self.screen, RED if pieza == 'R' else BLACK, center, radius)
        if self.selected:
            x = MARGIN + self.selected[1] * CELL_SIZE
            y = MARGIN + self.selected[0] * CELL_SIZE
            pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE), 3)
        turno_text = f"Turno: {'Rojo' if self.control.turno_actual == 'R' else 'Negro'}"
        self.screen.blit(self.font_28.render(turno_text, True, BLACK), (MARGIN, 10))
        self.draw_back_button()
        pygame.display.flip()

    def draw_end_screen(self):
        self.screen.fill(BLUE_BG)
        text = "Empate por bloqueo!" if self.winner is None else f"¡{self.winner} ha ganado!"
        surf = self.font_48.render(text, True, BLACK)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        self.screen.blit(surf, rect)
        for btn in self.end_buttons:
            btn.draw(self.screen)
        pygame.display.flip()

    def draw_back_button(self):
        btn_w, btn_h = 200, 40
        x, y = WIDTH - btn_w - 20, 10

        def volver():
            self.in_menu = True
            self.setup_menu()

        self.back_button = Button((x, y, btn_w, btn_h), "Volver al menú", volver)
        self.back_button.draw(self.screen)

    def handle_back_button_event(self, event):
        if hasattr(self, 'back_button'):
            self.back_button.handle_event(event)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for btn in self.buttons:
                btn.handle_event(event)

    def handle_human_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            if MARGIN <= x < WIDTH - MARGIN and MARGIN <= y < HEIGHT - MARGIN:
                col = (x - MARGIN) // CELL_SIZE
                row = (y - MARGIN) // CELL_SIZE
                if not self.selected and self.tablero.tablero[row][col] == self.control.turno_actual:
                    self.selected = (row, col)
                    self.drop_sound.play()
                elif self.selected:
                    origen, destino = self.selected, (row, col)
                    if self.tablero.mover_ficha(origen, destino):
                        self.control.registrar_movimiento(origen, destino)
                        self.move_sound.play()
                        self.turnos_sin_movimiento = 0
                        if self.tablero.hay_ganador():
                            self.winner = 'Rojo' if self.control.turno_actual == 'R' else 'Negro'
                            self.game_over = True
                        else:
                            self.control.cambiar_turno()
                    self.selected = None

    def handle_ai_turn(self):
        ia = self.ia_roja if self.control.turno_actual == 'R' else self.ia_negra
        if ia:
            movimiento = ia.mejor_movimiento(self.tablero)
            if movimiento is None:
                self.turnos_sin_movimiento += 1
                if self.turnos_sin_movimiento >= 2:
                    self.winner = None
                    self.game_over = True
                    self.setup_end_buttons()
                else:
                    self.control.cambiar_turno()
            else:
                origen, destino = movimiento
                time.sleep(0.5)
                self.tablero.mover_ficha(origen, destino)
                self.control.registrar_movimiento(origen, destino)
                self.move_sound.play()
                self.turnos_sin_movimiento = 0
                if self.tablero.hay_ganador():
                    self.winner = 'Rojo' if self.control.turno_actual == 'R' else 'Negro'
                    self.game_over = True
                    self.setup_end_buttons()
                else:
                    self.control.cambiar_turno()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if self.in_menu:
                self.handle_menu_events()
                self.draw_menu()
            elif self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit();
                        sys.exit()
                    for btn in self.end_buttons:
                        btn.handle_event(event)
                self.draw_end_screen()
            else:
                if not self.control.es_turno_humano():
                    self.handle_ai_turn()
                    self.draw_board()
                    continue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit();
                        sys.exit()
                    self.handle_human_event(event)
                    self.handle_back_button_event(event)
                self.draw_board()


if __name__ == '__main__':
    Game().run()