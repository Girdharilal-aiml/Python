"""
Coin Flip Simulator
Simple & fun GUI using tkinter
"""

import tkinter as tk
import random
import time

class CoinFlip:
    def __init__(self, root):
        self.root = root
        self.root.title("Coin Flip")
        self.root.geometry("400x550")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        self.heads = 0
        self.tails = 0
        self.flipping = False

        # Coin frames for animation
        self.coin_frames = ["🪙", "⬜", "🟡", "⬜", "🪙"]

        # Title
        tk.Label(
            root,
            text="🪙 Coin Flip",
            font=('Arial', 26, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(pady=20)

        # Coin display
        self.coin_label = tk.Label(
            root,
            text="🪙",
            font=('Arial', 100),
            bg='#1a1a2e',
            fg='white'
        )
        self.coin_label.pack(pady=10)

        # Result label
        self.result_label = tk.Label(
            root,
            text="Press flip!",
            font=('Arial', 22, 'bold'),
            bg='#1a1a2e',
            fg='#f1c40f'
        )
        self.result_label.pack(pady=10)

        # Score frame
        score_frame = tk.Frame(root, bg='#1a1a2e')
        score_frame.pack(pady=15)

        self.heads_label = tk.Label(
            score_frame,
            text="Heads: 0",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='#2ecc71',
            width=12,
            pady=8,
            relief=tk.RAISED
        )
        self.heads_label.pack(side=tk.LEFT, padx=10)

        self.tails_label = tk.Label(
            score_frame,
            text="Tails: 0",
            font=('Arial', 14, 'bold'),
            bg='#16213e',
            fg='#e74c3c',
            width=12,
            pady=8,
            relief=tk.RAISED
        )
        self.tails_label.pack(side=tk.LEFT, padx=10)

        # Flip button
        self.flip_btn = tk.Button(
            root,
            text="🪙 FLIP!",
            font=('Arial', 18, 'bold'),
            bg='#f39c12',
            fg='white',
            width=15,
            height=2,
            cursor='hand2',
            bd=0,
