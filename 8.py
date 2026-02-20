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

        tk.Label(
            selector_frame,
            text="Number of Dice:",
            font=('Arial', 13, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)

        for i in range(1, 7):
            tk.Button(
                selector_frame,
                text=str(i),
                command=lambda x=i: self.set_num_dice(x),
                bg='#95a5a6',
                fg='white',
                font=('Arial', 12, 'bold'),
                width=3,
                height=1,
                cursor='hand2',
                bd=0
            ).pack(side=tk.LEFT, padx=3)

        # Roll button
        self.roll_btn = tk.Button(
            root,
            text="🎲 ROLL DICE!",
            command=self.roll_dice,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 18, 'bold'),
            width=20,
            height=2,
            cursor='hand2',
            bd=0,
            activebackground='#c0392b'
        )
        self.roll_btn.pack(pady=20)

        # History frame
        history_frame = tk.Frame(root, bg='#2c3e50')
        history_frame.pack(pady=10)

        tk.Label(
            history_frame,
            text="Last 5 Rolls:",
            font=('Arial', 11, 'bold'),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()

        self.history_label = tk.Label(
            history_frame,
            text="No rolls yet",
            font=('Courier', 10),
            bg='#34495e',
            fg='#ecf0f1',
            padx=15,
            pady=8,
            relief=tk.SUNKEN
        )
        self.history_label.pack(pady=5)

        self.history = []

    def create_dice_labels(self):
        # Clear existing labels
        for label in self.dice_labels:
            label.destroy()
        self.dice_labels = []

        # Create new labels based on num_dice
        for i in range(self.num_dice):
            label = tk.Label(
                self.dice_frame,
                text=self.dice_faces[self.dice_values[i]],
                font=('Arial', 80),
                bg='white',
                fg='#2c3e50',
                width=2,
                height=1,
                relief=tk.RAISED,
