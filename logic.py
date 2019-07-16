class TicTacToe:
    def __init__(self):
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.player = 1
        self.symbols = {
            1: 'X',
            2: 'O',
        }
        self.winning_line = None

    def get_open_spots(self):
        return [(r, c)for r in range(3) for c in range(3) if self.board[r][c] == 0]

    def is_valid_move(self, r, c):
        return self.board[r][c] == 0

    def make_move(self, r, c):
        if self.is_valid_move(r, c):
            self.board[r][c] = self.player
            self.player = (self.player % 2) + 1

    def check_for_winner(self):
        for c in range(3):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] != 0:
                self.winning_line = 'column', c
                return self.board[0][c]
        for r in range(3):
            if self.board[r][0] == self.board[r][1] == self.board[r][2] != 0:
                self.winning_line = 'row', r
                return self.board[r][0]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winning_line = 'diagonal', 1
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winning_line = 'diagonal', 2
            return self.board[0][2]
        if not self.get_open_spots():
            return 'tie'

    def __str__(self):
        return (f'{self.board[0][0]} {self.board[0][1]} {self.board[0][2]}\n'
                f'{self.board[1][0]} {self.board[1][1]} {self.board[1][2]}\n'
                f'{self.board[2][0]} {self.board[2][1]} {self.board[2][2]}\n')


if __name__ == '__main__':
    game = TicTacToe()
    print(game)
    game.get_open_spots()
    print(game.get_open_spots())
    print(game.check_for_winner())
