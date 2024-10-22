import tkinter as tk
from tkinter import messagebox
from logic import HexGame

class HexUI:
    def __init__(self, size):
        self.game = HexGame(size)
        self.root = tk.Tk()
        self.root.title(f"Hex Game - {size}x{size}")
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.click)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.game.size):
            for j in range(self.game.size):
                x = j * 50 + (i % 2) * 25
                y = i * 43.3
                color = "red" if self.game.board[i, j] == 1 else "blue" if self.game.board[i, j] == 2 else "white"
                self.draw_hexagon(x, y, color)

    def draw_hexagon(self, x, y, color):
        points = [
            (x + 25, y),
            (x + 50, y + 21.65),
            (x + 50, y + 64.95),
            (x + 25, y + 86.6),
            (x, y + 64.95),
            (x, y + 21.65)
        ]
        self.canvas.create_polygon(points, fill=color, outline="black")

    def click(self, event):
        x = int(event.x // 50)
        y = int(event.y // 43.3)
        if 0 <= x < self.game.size and 0 <= y < self.game.size and self.game.board[y, x] == 0:
            self.game.board[y, x] = self.game.current_player
            self.draw_board()
            if self.game.check_winner(self.game.current_player):
                messagebox.showinfo("Game Over", f"Player {self.game.current_player} wins!")
                self.root.quit()
            self.game.current_player = 2 if self.game.current_player == 1 else 1
            if self.game.current_player == 2:
                if self.game.bot_move():
                    self.draw_board()
                    if self.game.check_winner(2):
                        messagebox.showinfo("Game Over", "Player 2 (Bot) wins!")
                        self.root.quit()
                    self.game.current_player = 1

    def run(self):
        self.root.mainloop()
