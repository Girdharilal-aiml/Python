"""
Breakout Game - Simple & Perfect UI
Classic brick-breaking game
"""

import tkinter as tk
from tkinter import messagebox
import random

class Breakout:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Game settings
        self.canvas_width = 600
        self.canvas_height = 600
        
        # Paddle
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_speed = 20
        
        # Ball
        self.ball_radius = 8
        self.ball_speed_x = 4
        self.ball_speed_y = -4
        
        # Bricks
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_width = 58
        self.brick_height = 20
        self.brick_padding = 2
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_running = False
        self.bricks = []
        
        # Colors
        self.brick_colors = ['#f44336', '#FF9800', '#FFC107', '#4CAF50', '#2196F3']

        
