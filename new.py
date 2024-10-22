import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np
import os

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

    def make_move(self, x, y):
        if self.board[y][x] == 0:  # Only allow move on empty cell
            self.board[y][x] = self.current_player
            self.current_player = 2 if self.current_player == 1 else 1
            return True
        return False


class HexUI:
    def __init__(self, size):
        self.size = size
        self.root = tk.Tk()
        self.root.title(f"Hex Game - {size}x{size}")

        # Load hexagon images
        self.red_hex_path = r"C:\Users\Admin\Documents\College\Sem 5\AI LAb\Hex\HexGame\redHex.jpg"
        self.blue_hex_path = r"C:\Users\Admin\Documents\College\Sem 5\AI LAb\Hex\HexGame\blueHex.png"
        self.empty_hex_path = r"C:\Users\Admin\Documents\College\Sem 5\AI LAb\Hex\HexGame\emptyHex.jpg"

        # Load images using PIL
        self.red_hex = ImageTk.PhotoImage(Image.open(self.red_hex_path))
        self.blue_hex = ImageTk.PhotoImage(Image.open(self.blue_hex_path))
        self.empty_hex = ImageTk.PhotoImage(Image.open(self.empty_hex_path))

        # Initialize the game logic
        self.game = HexGame(size)

        # Set up the canvas for drawing the hexagons
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()

        # Initialize hexagonal buttons
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        self.create_buttons(size)
        self.draw_board()

    def create_buttons(self, size):
        # Size parameters for the hexagons
        self.hex_width = 50
        self.hex_height = 43.3

        for i in range(size):
            for j in range(size):
                x = j * self.hex_width + (i % 2) * (self.hex_width / 2)  # Adjust for hexagonal offset
                y = i * self.hex_height * 0.75  # Reduce height spacing for tighter connection

                # Define hexagon points
                points = [
                    x + self.hex_width / 2, y,
                    x + self.hex_width, y + self.hex_height / 4,
                    x + self.hex_width, y + 3 * self.hex_height / 4,
                    x + self.hex_width / 2, y + self.hex_height,
                    x, y + 3 * self.hex_height / 4,
                    x, y + self.hex_height / 4
                ]

                # Create a polygon and bind click event
                button = self.canvas.create_polygon(points, fill="", outline="black", tags=(i, j))
                self.canvas.tag_bind(button, '<Button-1>', lambda e, x=j, y=i: self.click(x, y))
                self.buttons[i][j] = button  # Store the button

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.game.board[i][j] == 1:
                    self.canvas.itemconfig(self.buttons[i][j], fill='red')
                elif self.game.board[i][j] == 2:
                    self.canvas.itemconfig(self.buttons[i][j], fill='blue')
                else:
                    self.canvas.itemconfig(self.buttons[i][j], fill='')

    def click(self, x, y):
        if self.game.make_move(x, y):  # Only proceed if move is valid
            self.draw_board()  # Update the board after a move

            # Check for winner
            if self.game.check_winner(1):
                messagebox.showinfo("Game Over", "Player 1 (Red) wins!")
                self.root.quit()
            elif self.game.check_winner(2):
                messagebox.showinfo("Game Over", "Player 2 (Blue) wins!")
                self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    hex_game_ui = HexUI(size=11)  # Specify the desired board size
    hex_game_ui.run()
