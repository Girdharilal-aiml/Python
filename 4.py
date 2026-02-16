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
        
        # Current calculation
        self.current = ""
        self.total = 0
        
        # Display
        self.display = tk.Entry(
            root,
            font=('Arial', 24, 'bold'),
            bd=10,
            bg='#ecf0f1',
            fg='#2c3e50',
            justify='right',
            relief=tk.RIDGE
        )
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky='ew')
        
