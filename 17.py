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

        self.text_colors = {
            0: '#c9d1d9',
            2: '#776e65',
            4: '#776e65',
        }

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.score_font = tkfont.Font(family='Arial', size=16, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title and scores
        header_frame = tk.Frame(main_frame, bg='#161b22')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Left side - Title
        left_header = tk.Frame(header_frame, bg='#161b22')
        left_header.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(
            left_header,
            text="🎮",
            font=('Arial', 35),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            left_header,
            text="2048",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT)

        # Right side - Scores
        scores_container = tk.Frame(header_frame, bg='#161b22')
        scores_container.pack(side=tk.RIGHT, padx=20, pady=15)

        # Score
        score_frame = tk.Frame(scores_container, bg='#21262d')
        score_frame.pack(side=tk.LEFT, padx=5)

        tk.Label(
            score_frame,
            text="SCORE",
            font=('Arial', 10, 'bold'),
            bg='#21262d',
            fg='#8b949e'
        ).pack(pady=(8, 2), padx=15)

        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=self.score_font,
            bg='#21262d',
            fg='#c9d1d9'
        )
        self.score_label.pack(pady=(0, 8), padx=15)

        # Best score
        best_frame = tk.Frame(scores_container, bg='#21262d')
        best_frame.pack(side=tk.LEFT, padx=5)
