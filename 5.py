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
