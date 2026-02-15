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
        
        # Choices
        self.choices = ["Rock", "Paper", "Scissors"]
        self.emojis = {
            "Rock": "🪨",
            "Paper": "📄",
            "Scissors": "✂️"
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="🎮 Rock Paper Scissors",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)
        
        # Score display
        score_frame = tk.Frame(self.root, bg='#2c3e50')
        score_frame.pack(pady=10)
        
        self.player_score_label = tk.Label(
            score_frame,
            text=f"You: {self.player_score}",
            font=('Arial', 18, 'bold'),
            bg='#27ae60',
            fg='white',
            width=10,
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
