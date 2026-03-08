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
        
