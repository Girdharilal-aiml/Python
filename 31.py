"""
Memory Card Game - Simple & Perfect UI
Flip cards and match pairs
"""

import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Game")
        self.root.geometry("700x800")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(600, 700)

        # Game state
        self.cards = []
        self.card_buttons = []
        self.flipped = []
        self.matched = []
        self.moves = 0
        self.pairs_found = 0
        self.game_active = False

        # Card emojis
        self.symbols = ['🍎', '🍌', '🍇', '🍊', '🍓', '🍒', '🍑', '🍍',
                       '🥝', '🥥', '🍉', '🍋', '🥭', '🍏', '🫐', '🍈']

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🃏 Memory Card Game",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=20)

        # Score panel
        score_frame = tk.Frame(root, bg='white')
        score_frame.pack(pady=15)

        # Moves
        moves_container = tk.Frame(score_frame, bg='white')
        moves_container.pack(side=tk.LEFT, padx=20)

        tk.Label(
            moves_container,
            text="MOVES:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#666'
        ).pack()

        self.moves_label = tk.Label(
            moves_container,
            text="0",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2196F3'
        )
        self.moves_label.pack()

        # Pairs
        pairs_container = tk.Frame(score_frame, bg='white')
        pairs_container.pack(side=tk.LEFT, padx=20)

        tk.Label(
            pairs_container,
