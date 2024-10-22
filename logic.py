import numpy as np

class HexGame:
    def __init__(self, size):
        self.size = size
        self.board = np.zeros((size, size))
        self.current_player = 1  # Player 1 starts

    def check_winner(self, player):
        for i in range(self.size):
            if self.dfs(0, i, player, visited=set()) or self.dfs(i, 0, player, visited=set()):
                return True
        return False

    def dfs(self, x, y, player, visited):
        if (x, y) in visited:
            return False
        if player == 1 and x == self.size - 1:  # Player 1 connects top to bottom
            return True
        if player == 2 and y == self.size - 1:  # Player 2 connects left to right
            return True
        visited.add((x, y))

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx, ny] == player:
                if self.dfs(nx, ny, player, visited):
                    return True
        return False

    def bot_move(self):
        _, move = self.minimax(self.board, 2, -np.inf, np.inf)
        if move:
            self.board[move[0], move[1]] = 2
            return True
        return False

    def minimax(self, board, player, alpha, beta):
        if self.check_winner(1):
            return -1, None
        elif self.check_winner(2):
            return 1, None
        elif np.all(board):
            return 0, None  # Draw

        best_score = -np.inf if player == 2 else np.inf
        best_move = None

        for i in range(self.size):
            for j in range(self.size):
                if board[i, j] == 0:
                    board[i, j] = player
                    score, _ = self.minimax(board, 2 if player == 1 else 1, alpha, beta)
                    board[i, j] = 0

                    if player == 2:
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                        alpha = max(alpha, best_score)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
                        beta = min(beta, best_score)

                    if beta <= alpha:
                        break

        return best_score, best_move
