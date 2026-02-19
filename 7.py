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

        # Title
        tk.Label(
            root,
            text="🎨 Color Code Generator",
            font=('Arial', 22, 'bold'),
            bg='#1e1e1e',
            fg='white'
        ).pack(pady=15)

        # Color preview (big square)
        self.preview_frame = tk.Frame(
            root,
            bg=self.current_color,
            width=300,
            height=200,
            relief=tk.RAISED,
            bd=5
        )
        self.preview_frame.pack(pady=20)
        self.preview_frame.pack_propagate(False)

        # Color codes frame
        codes_frame = tk.Frame(root, bg='#1e1e1e')
        codes_frame.pack(pady=15)

        # HEX code
        tk.Label(codes_frame, text="HEX:", bg='#1e1e1e', fg='#aaa', font=('Arial', 11)).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.hex_var = tk.StringVar(value=self.current_color)
        hex_entry = tk.Entry(codes_frame, textvariable=self.hex_var, font=('Courier', 14, 'bold'), width=15, justify='center')
        hex_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(codes_frame, text="📋", command=lambda: self.copy_code(self.hex_var.get()), bg='#555', fg='white', cursor='hand2', bd=0, width=3).grid(row=0, column=2, padx=5)

