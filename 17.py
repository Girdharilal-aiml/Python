"""
2048 Game - Modern UI (Responsive)
Classic sliding tile puzzle game
"""

import tkinter as tk
from tkinter import font as tkfont
import random

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry("600x750")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        self.root.minsize(400, 500)

        # Game state
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
