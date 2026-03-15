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
