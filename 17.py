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

        # Colors for tiles
        self.tile_colors = {
            0: '#1a1a2e',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e',
        }

