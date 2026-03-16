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


        
