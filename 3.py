"""
Rock Paper Scissors Game
Simple GUI game using tkinter

FEATURES:
- Play against computer
- Score tracking
- Visual feedback
- Best of 5 rounds mode
"""

import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')
        
        # Game state
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.game_mode = "endless"  # or "best_of_5"
        
