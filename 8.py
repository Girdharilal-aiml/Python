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
                bd=5
            )
            label.pack(side=tk.LEFT, padx=10)
            self.dice_labels.append(label)

    def set_num_dice(self, num):
        if not self.rolling:
            self.num_dice = num
            self.dice_values = [1] * num
            self.create_dice_labels()
            self.update_total()

    def roll_dice(self):
        if self.rolling:
            return
        
        self.rolling = True
        self.roll_btn.config(state='disabled', bg='#95a5a6')
        self.animate_roll(0)

    def animate_roll(self, step):
        if step < 15:
            # Random animation
            for i in range(self.num_dice):
                random_value = random.randint(1, 6)
                self.dice_labels[i].config(text=self.dice_faces[random_value])
            
            self.root.after(50, lambda: self.animate_roll(step + 1))
        else:
            # Final roll
            self.dice_values = [random.randint(1, 6) for _ in range(self.num_dice)]
            for i in range(self.num_dice):
                self.dice_labels[i].config(text=self.dice_faces[self.dice_values[i]])
            
            self.update_total()
            self.add_to_history()
            self.rolling = False
            self.roll_btn.config(state='normal', bg='#e74c3c')
