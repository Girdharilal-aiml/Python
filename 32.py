"""
Pong Game - Simple & Perfect UI
Classic 2-player paddle game with AI opponent
"""

import tkinter as tk
from tkinter import messagebox
import random

class Pong:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(600, 450)

        # Game settings (will be updated on resize)
        self.canvas_width = 800
        self.canvas_height = 500
        
        # Paddle settings
        self.paddle_width = 15
        self.paddle_height = 100
        self.paddle_speed = 20
        
        # Ball settings
        self.ball_size = 15
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        
        # Game state
        self.game_running = False
        self.game_mode = 'ai'  # 'ai' or '2player'
        self.player1_score = 0
        self.player2_score = 0

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Scores
        score_frame = tk.Frame(header, bg='#f5f5f5')
        score_frame.pack(expand=True)

        self.p1_score_label = tk.Label(
            score_frame,
            text="0",
            font=('Arial', 28, 'bold'),
            bg='#f5f5f5',
            fg='#2196F3'
        )
        self.p1_score_label.pack(side=tk.LEFT, padx=50)

        tk.Label(
            score_frame,
            text="🏓",
            font=('Arial', 24),
            bg='#f5f5f5'
        ).pack(side=tk.LEFT, padx=20)

