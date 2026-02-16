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
        
        # Button layout
        buttons = [
            ('C', 1, 0, '#e74c3c'), ('⌫', 1, 1, '#e67e22'), ('÷', 1, 2, '#3498db'), ('×', 1, 3, '#3498db'),
            ('7', 2, 0, '#34495e'), ('8', 2, 1, '#34495e'), ('9', 2, 2, '#34495e'), ('-', 2, 3, '#3498db'),
            ('4', 3, 0, '#34495e'), ('5', 3, 1, '#34495e'), ('6', 3, 2, '#34495e'), ('+', 3, 3, '#3498db'),
            ('1', 4, 0, '#34495e'), ('2', 4, 1, '#34495e'), ('3', 4, 2, '#34495e'), ('=', 4, 3, '#27ae60'),
            ('0', 5, 0, '#34495e'), ('.', 5, 1, '#34495e'), ('00', 5, 2, '#34495e'), ('', 5, 3, '')
        ]
        
        # Create buttons
        for (text, row, col, color) in buttons:
            if text:  # Skip empty cells
                btn = tk.Button(
                    root,
                    text=text,
                    font=('Arial', 18, 'bold'),
                    bg=color,
                    fg='white',
                    activebackground=color,
                    activeforeground='white',
                    bd=3,
                    relief=tk.RAISED,
                    cursor='hand2',
                    command=lambda t=text: self.on_button_click(t)
                )
                
                # Make = button span 2 columns
                if text == '=':
                    btn.grid(row=row, column=col, rowspan=2, padx=5, pady=5, sticky='nsew')
                else:
                    btn.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Configure grid weights for responsive sizing
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        
        # Keyboard bindings
        root.bind('<Key>', self.on_key_press)
        
        # Focus on display
        self.display.focus_set()
        
    def on_button_click(self, char):
        if char == 'C':
            self.clear()
        elif char == '⌫':
            self.backspace()
        elif char == '=':
            self.calculate()
        else:
            self.append_char(char)
    
    def append_char(self, char):
        # Replace × and ÷ with * and /
        if char == '×':
            char = '*'
        elif char == '÷':
            char = '/'
        
        self.current += str(char)
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current)
