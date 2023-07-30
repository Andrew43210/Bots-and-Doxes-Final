import random

class DotsAndBoxes:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.score = {'Player': 0, 'AI': 0}

    def draw_grid(self):
        print('  ' + ' '.join(map(str, range(self.size))))
        for i, row in enumerate(self.grid):
            print(f'{i} ' + ' '.join(['X' if cell == 'Player' else 'O' if cell == 'AI' else '.' for cell in row]))
        print()
        print('Score:', self.score)
        print()

    def make_move(self, player, x, y):
        if self.grid[x][y] != 0:
            return False
        self.grid[x][y] = player
        self.update_score(player)
        return True

    def update_score(self, player):
        lines = []
        for row in self.grid:
            lines.append(row)
        for col in range(self.size):
            lines.append([self.grid[row][col] for row in range(self.size)])
        for line in lines:
            count = 0
            for cell in line:
                if cell == player:
                    count += 1
                else:
                    count = 0
                if count == 6:
                    print(f'{player} has won!')
                    self.reset_game()
                    return

    def ai_move(self):
        available_moves = [(x, y) for x in range(self.size) for y in range(self.size) if self.grid[x][y] == 0]
        if not available_moves:
            return False
        winning_moves = []
        blocking_moves = []
        for move in available_moves:
            self.grid[move[0]][move[1]] = 'AI'
            if self.check_win('AI'):
                winning_moves.append(move)
            self.grid[move[0]][move[1]] = 'Player'
            if self.check_win('Player'):
                blocking_moves.append(move)
            self.grid[move[0]][move[1]] = 0
        if winning_moves:
            move = random.choice(winning_moves)
        elif blocking_moves:
            move = random.choice(blocking_moves)
        else:
            move = random.choice(available_moves)
        self.make_move('AI', move[0], move[1])
        return True

    def check_win(self, player):
        lines = []
        for row in self.grid:
            lines.append(row)
        for col in range(self.size):
            lines.append([self.grid[row][col] for row in range(self.size)])
        for line in lines:
            count = 0
            for cell in line:
                if cell == player:
                    count += 1
                else:
                    count = 0
                if count == 6:
                    return True
        return False

    def reset_game(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.score = {'Player': 0, 'AI': 0}

    def play_game(self):
        while True:
            self.draw_grid()
            x = input('Enter x coordinate (or "r" to reset): ')
            if x == 'r':
                self.reset_game()
                continue
            y = input('Enter y coordinate (or "r" to reset): ')
            if y == 'r':
                self.reset_game()
                continue
            try:
                x = int(x)
                y = int(y)
                if not (0 <= x < self.size and 0 <= y < self.size):
                    raise ValueError
            except ValueError:
                print('Invalid input!')
                continue
            if not self.make_move('Player', x, y):
                print('Invalid move!')
                continue
            if not self.ai_move():
                break
        self.draw_grid()
        print('Final Score:', self.score)

game = DotsAndBoxes(6)
game.play_game()
