"""
Snake Game - Simple & Perfect UI
Classic snake with score and speed increase
"""

import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(False, False)

        # Game settings
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # Game state
        self.snake = []
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.food = None
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.speed = 150  # milliseconds



        
