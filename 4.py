"""
Simple Calculator
GUI calculator using tkinter

FEATURES:
- Basic operations (+, -, ×, ÷)
- Clear and backspace
- Keyboard support
- Clean design
"""

import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("350x500")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
