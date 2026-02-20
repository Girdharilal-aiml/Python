"""
Dice Roller
Roll dice with animations and multiple dice support
"""

import tkinter as tk
import random

class DiceRoller:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Roller")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)

        self.rolling = False
        self.num_dice = 1
        self.dice_values = [1]

        # Dice faces using Unicode
        self.dice_faces = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }

        # Title
        tk.Label(
            root,
            text="🎲 Dice Roller",
            font=('Arial', 26, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)

        # Dice display frame
        self.dice_frame = tk.Frame(root, bg='#2c3e50')
        self.dice_frame.pack(pady=20)

        self.dice_labels = []
        self.create_dice_labels()

        # Total display
        self.total_label = tk.Label(
            root,
            text="Total: 1",
            font=('Arial', 24, 'bold'),
            bg='#34495e',
            fg='#f39c12',
            relief=tk.RAISED,
            bd=5,
            padx=20,
            pady=10
        )
        self.total_label.pack(pady=15)

        # Number of dice selector
        selector_frame = tk.Frame(root, bg='#2c3e50')
        selector_frame.pack(pady=15)

