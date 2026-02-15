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
        
        reset_btn = tk.Button(
            bottom_frame,
            text="🔄 Reset Score",
            command=self.reset_game,
            font=('Arial', 11),
            bg='#95a5a6',
            fg='white',
            cursor='hand2',
            width=15
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        mode_btn = tk.Button(
            bottom_frame,
            text="🎯 Best of 5",
            command=self.toggle_mode,
            font=('Arial', 11),
            bg='#9b59b6',
            fg='white',
            cursor='hand2',
            width=15
        )
        mode_btn.pack(side=tk.LEFT, padx=5)
        
        self.mode_btn = mode_btn  # Save reference for updating text
        
    def play(self, player_choice):
        # Computer makes random choice
        computer_choice = random.choice(self.choices)
        
        # Update displays
        self.player_choice_label.config(text=self.emojis[player_choice])
        self.computer_choice_label.config(text=self.emojis[computer_choice])
        
        # Determine winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update scores
        if result == "win":
            self.player_score += 1
            self.result_label.config(
                text=f"🎉 You Win! {player_choice} beats {computer_choice}!",
                fg='#2ecc71'
            )
        elif result == "lose":
            self.computer_score += 1
            self.result_label.config(
                text=f"😢 You Lose! {computer_choice} beats {player_choice}!",
                fg='#e74c3c'
            )
        else:
            self.result_label.config(
                text=f"🤝 It's a Tie! Both chose {player_choice}!",
                fg='#f39c12'
            )
        
        # Update score labels
        self.player_score_label.config(text=f"You: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        
        # Check for game end in best of 5 mode
        if self.game_mode == "best_of_5":
            self.rounds_played += 1
            if self.player_score == 3:
                messagebox.showinfo("🏆 Victory!", "You won Best of 5!")
                self.reset_game()
            elif self.computer_score == 3:
                messagebox.showinfo("😔 Defeat", "Computer won Best of 5!")
                self.reset_game()
    
    def determine_winner(self, player, computer):
        if player == computer:
            return "tie"
        
        win_conditions = {
            "Rock": "Scissors",
            "Paper": "Rock",
            "Scissors": "Paper"
        }
        
        if win_conditions[player] == computer:
            return "win"
        else:
            return "lose"
    
