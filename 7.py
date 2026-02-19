"""
Color Code Generator
Generate and preview colors with their codes (HEX, RGB)
"""

import tkinter as tk
from tkinter import messagebox
import random

class ColorGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Code Generator")
        self.root.geometry("500x600")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(False, False)

        # Current color
        self.current_color = "#3498db"

