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
        self.player_score_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            score_frame,
            text="VS",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        self.computer_score_label = tk.Label(
            score_frame,
            text=f"Computer: {self.computer_score}",
            font=('Arial', 18, 'bold'),
            bg='#e74c3c',
            fg='white',
            width=10,
            relief=tk.RAISED,
            padx=10,
            pady=5
        )
        self.computer_score_label.pack(side=tk.LEFT, padx=10)
        
        # Result display
        self.result_label = tk.Label(
            self.root,
            text="Choose your move!",
            font=('Arial', 16),
            bg='#2c3e50',
            fg='#ecf0f1',
            wraplength=400
        )
        self.result_label.pack(pady=20)
        
        # Choice display
        choice_frame = tk.Frame(self.root, bg='#2c3e50')
        choice_frame.pack(pady=20)
        
        tk.Label(
            choice_frame,
            text="Your Choice:",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        ).pack()
        
        self.player_choice_label = tk.Label(
            choice_frame,
            text="❓",
            font=('Arial', 48),
            bg='#34495e',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED
        )
        self.player_choice_label.pack(pady=5)
        
        tk.Label(
            choice_frame,
            text="Computer's Choice:",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=(20, 0))
        
        self.computer_choice_label = tk.Label(
            choice_frame,
            text="❓",
            font=('Arial', 48),
            bg='#34495e',
            fg='white',
            width=3,
            height=1,
            relief=tk.RAISED
        )
        self.computer_choice_label.pack(pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=30)
        
        for choice in self.choices:
            btn = tk.Button(
                button_frame,
                text=f"{self.emojis[choice]}\n{choice}",
                command=lambda c=choice: self.play(c),
                font=('Arial', 14, 'bold'),
                bg='#3498db',
                fg='white',
                width=10,
                height=3,
                cursor='hand2',
                relief=tk.RAISED,
                bd=3
            )
            btn.pack(side=tk.LEFT, padx=10)
        
        # Bottom buttons
        bottom_frame = tk.Frame(self.root, bg='#2c3e50')
        bottom_frame.pack(pady=20)
        
