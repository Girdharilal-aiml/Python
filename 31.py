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
