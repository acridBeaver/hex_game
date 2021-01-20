from pathlib import Path
from hexogon.button import *


class Game:
    def __init__(self, size):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.size = size
        self.set_tile_size()
        self.state = [[0 for _ in range(self.size)] for __ in range(self.size)]
        self.origin = Point(WIDTH / 2 - (HEIGHT / 2 - 50) / sqrt(3), 50)
        self.move = 1
        self.started = False

    def load_data(self):
        game_folder = Path('..')
        img_folder = game_folder / 'img'
        self.bg_img = pg.image.load(str(img_folder / BG_IMG)).convert_alpha()

    def set_tile_size(self):
        self.tile_size = 4 * (HEIGHT / 2 - 50) / 3 / sqrt(3) / (self.size - 1)

    def coords(self, r, c):
        x = self.origin.x + c * 3 / 2 * self.tile_size
        y = self.origin.y + (c + 2 * r) * self.tile_size * sqrt(3) / 2
        return int(x), int(y)

    def tick(self, pos):
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if in_hex(pos, x, y, self.tile_size) \
                        and self.state[r][c] != 2 and self.state[r][c] != 1:
                    self.state[r][c] = self.move
                    self.move = 3 - self.move

    def highlight(self, pos):
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if self.state[r][c] == 0 and in_hex(pos, x, y, self.tile_size):
                    self.state[r][c] = self.move + 2
                elif self.state[r][c] > 2 \
                        and not in_hex(pos, x, y, self.tile_size):
                    self.state[r][c] = 0

    def show_grid(self):
        A = (self.origin.x - self.tile_size,
             self.origin.y - self.tile_size * sqrt(3))
        B = (self.origin.x - self.tile_size / 2 * (1 - 3 * self.size),
             self.origin.y + self.tile_size * sqrt(3) / 2
             * (self.size - 2) + self.tile_size * sqrt(3) / 6)
        C = (self.origin.x - self.tile_size / 2 * (1 - 3 * self.size),
             self.origin.y + self.tile_size * sqrt(3)
             / 2 * (2 * self.size + self.size - 1))
        D = (self.origin.x - self.tile_size,
             self.origin.y + self.tile_size * sqrt(3)
             * (self.size - 1 / 2) - self.tile_size * sqrt(3) / 6)
        M = ((A[0] + B[0]) / 2, (B[1] + C[1]) / 2)
        pg.draw.polygon(self.screen, GREEN, [A, B, M])
        pg.draw.polygon(self.screen, GREEN, [C, D, M])
        pg.draw.polygon(self.screen, BLUE, [B, C, M])
        pg.draw.polygon(self.screen, BLUE, [D, A, M])
        for r in range(self.size):
            for c in range(self.size):
                x, y = self.coords(r, c)
                if self.state[r][c] == 1:
                    draw_hex(self.screen,
                             GREEN, LIGHTYELLOW, (x, y), self.tile_size)
                elif self.state[r][c] == 2:
                    draw_hex(self.screen,
                             BLUE, LIGHTYELLOW, (x, y), self.tile_size)
                elif self.state[r][c] == 3:
                    draw_hex(self.screen, LIGHTGREEN, LIGHTYELLOW, (x, y),
                             self.tile_size)
                elif self.state[r][c] == 4:
                    draw_hex(self.screen,
                             LIGHTBLUE, LIGHTYELLOW, (x, y), self.tile_size)
                else:
                    draw_hex(self.screen,
                             DARKRED, LIGHTYELLOW, (x, y), self.tile_size)

    def checkWin(self):
        for y in range(self.size):
            if self.state[y][0] == 2:
                if check_move(Point(y, 0), self.state,
                              lambda v: (v.Y == self.size - 1), 2):
                    return 2

        for x in range(self.size):
            if self.state[0][x] == 1:
                if check_move(Point(0, x), self.state,
                              lambda v: (v.X == self.size - 1), 1):
                    return 1
        return 0

    def shadow(self):
        shadow = pg.Surface((WIDTH, HEIGHT))
        shadow.set_alpha(200)
        self.screen.blit(shadow, (0, 0))

    def start_screen(self):
        start = True
        play = Button((WIDTH / 2, 2 * HEIGHT / 3), 80, 'Play', col=RED)
        buttons = [play]
        while start:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:

                    if play.triggered():
                        self.__init__(self.size)
                        self.started = True
                        return True
            for button in buttons:
                button.highlighted()
            self.screen.blit(self.bg_img, (0, 0))
            text_out(self.screen, 'HEX', 200, ORANGE, (WIDTH / 2, HEIGHT / 3))
            for button in buttons:
                button.show(self.screen)
            pg.display.flip()

    def go_screen(self, winner):
        go = True
        home = Button((WIDTH / 2, 2 * HEIGHT / 3), 50, 'Home', col=WHITE)
        while go:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if home.triggered():
                        self.started = False
                        return True
            home.highlighted()

            self.screen.blit(self.bg_img, (0, 0))
            self.show_grid()
            self.shadow()
            text_out(self.screen,
                     'GAME OVER', 80, ORANGE, (WIDTH / 2, HEIGHT / 3))
            if winner == 2:
                text_out(self.screen,
                         'Blue won', 60, BLUE, (WIDTH / 2, HEIGHT / 2))
            else:
                text_out(self.screen,
                         'Green won', 60, GREEN, (WIDTH / 2, HEIGHT / 2))
            home.show(self.screen)
            pg.display.flip()
