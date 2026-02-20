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
