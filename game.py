import pygame
from sys import exit
from logic import TicTacToe

colors = {
    'white': (255, 255, 255),
    'blue': (0, 0, 200),
    'black': (0, 0, 0),
    'red': (200, 0, 0),
    'green': (0, 255, 0),
    'purple': (175, 0, 175)
    }

SIZE = WIDTH, HEIGHT = (600, 600)
WINDOW = pygame.display.set_mode(SIZE)  # returns game window surface object


class Window:
    def __init__(self):
        pygame.init()
        self.window = WINDOW
        pygame.display.set_caption('Tic Tac Toe')
        self.clock = pygame.time.Clock()
        self.grid = Grid()

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.grid.make_move()
                self.grid.announce_winner_terminal()
                self.grid.draw_moves()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.grid.reset()

    def update(self):
        self.window.fill(colors['black'])
        self.clock.tick(30)
        self.grid.draw()
        self.grid.get_hovered_square()
        self.grid.draw_moves()
        self.grid.draw_winning_line()
        self.grid.announce_winner()
        self.events()
        pygame.display.flip()


class Grid:
    squares = [
        [(0, 0, 200, 200), (200, 0, 200, 200), (400, 0, 200, 200)],
        [(0, 200, 200, 200), (200, 200, 200, 200), (400, 200, 200, 200)],
        [(0, 400, 200, 200), (200, 400, 200, 200), (400, 400, 200, 200)],
    ]

    def __init__(self):
        self.surface = WINDOW
        self.width = WIDTH
        self.height = HEIGHT
        self.rows = 3
        self.color = colors['white']
        self.game = TicTacToe()
        self.winner = None
        self.font = 'century gothic'
        self.font_name = pygame.font.match_font(self.font, 1)

    def draw(self):
        space = self.width // self.rows
        x = 0
        y = 0
        for line in range(self.rows):
            x += space
            y += space
            pygame.draw.line(self.surface, self.color, (x, 0), (x, self.width), 3)
            pygame.draw.line(self.surface, self.color, (0, y), (self.height, y), 3)

    def get_hovered_square(self):
        x, y = pygame.mouse.get_pos()
        if 0 < x < 200:
            c = 0
        elif 200 < x < 400:
            c = 1
        elif 400 < x < 600:
            c = 2
        else:
            c = None

        if 0 < y < 200:
            r = 0
        elif 200 < y < 400:
            r = 1
        elif 400 < y < 600:
            r = 2
        else:
            r = None

        if r is not None and c is not None:
            square = self.squares[r][c]
            if self.game.is_valid_move(r, c) and self.game.check_for_winner() is None:
                pygame.draw.rect(self.surface, colors['green'], square)
            return square, (r, c)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.surface.blit(text_surface, text_rect)

    def draw_moves(self):
        for r in range(3):
            for c in range(3):
                player = self.game.board[r][c]
                if player != 0:
                    square = self.squares[r][c]
                    x, y = square[0] + 100, square[1] + 100
                    if player == 1:
                        color = colors['blue']
                    else:
                        color = colors['red']
                    self.draw_text(self.game.symbols[player], 120, color, x, y)

    def draw_winning_line(self):
        if self.game.check_for_winner() is not None and self.game.check_for_winner() != 'tie':
            line, place = self.game.winning_line
            if line == 'row':
                y = (place * 200) + 100
                pygame.draw.line(self.surface, (173, 0, 173), (35, y), (self.width - 35, y), 15)
            if line == 'column':
                x = (place * 200) + 100
                pygame.draw.line(self.surface, colors['purple'], (x, 35), (x, self.height - 35), 15)
            if line == 'diagonal':
                if place == 1:
                    start = (35, 35)
                    end = (self.width - 35, self.height - 35)
                else:
                    start = (self.width - 35, 35)
                    end = (35, self.height - 35)
                pygame.draw.line(self.surface, colors['purple'], start, end, 15)

    def make_move(self):
        return_val = self.get_hovered_square()
        if return_val is not None and self.game.check_for_winner() is None:
            active_square, (r, c) = return_val
            self.game.make_move(r, c)

    def announce_winner_terminal(self):
        self.winner = self.game.check_for_winner()
        if self.winner == 'tie':
            print("It's a tie")
            print("to play again press space")
            print('to exit press esc')
        elif self.winner:
            print(f"The winner is player {self.winner} -> ({self.game.symbols[self.winner]})")
            print("to play again press space")
            print('to exit press esc')

    def announcement_bg(self):
        s = pygame.Surface((540, 140))
        s.set_alpha(100)
        s.fill(colors['purple'])
        self.surface.blit(s, (30, 230))

    def announce_winner(self):
        self.winner = self.game.check_for_winner()
        if self.winner == 'tie':
            self.announcement_bg()
            self.draw_text("It's a tie", 40, colors['green'], 300, 255)
            self.draw_text("to play again press space", 40, colors['green'], 300, 300)
            self.draw_text("to exit press esc", 40, colors['green'], 300, 345)

        elif self.winner:
            self.announcement_bg()
            self.draw_text(f"The winner is player {self.winner} -> {self.game.symbols[self.winner]}", 40,
                           colors['green'], 300, 255)
            self.draw_text("to play again press space", 40, colors['green'], 300, 300)
            self.draw_text("to exit press esc", 40, colors['green'], 300, 345)

    def reset(self):
        del self.game
        self.game = TicTacToe()


if __name__ == '__main__':
    window = Window()
    while True:
        window.update()
