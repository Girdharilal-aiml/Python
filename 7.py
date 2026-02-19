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

        # RGB code
        tk.Label(codes_frame, text="RGB:", bg='#1e1e1e', fg='#aaa', font=('Arial', 11)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.rgb_var = tk.StringVar()
        rgb_entry = tk.Entry(codes_frame, textvariable=self.rgb_var, font=('Courier', 14, 'bold'), width=15, justify='center', state='readonly')
        rgb_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(codes_frame, text="📋", command=lambda: self.copy_code(self.rgb_var.get()), bg='#555', fg='white', cursor='hand2', bd=0, width=3).grid(row=1, column=2, padx=5)

        # Update RGB display
        self.update_rgb()

        # RGB Sliders
        slider_frame = tk.Frame(root, bg='#1e1e1e')
        slider_frame.pack(pady=15, padx=30, fill=tk.X)

        self.r_var = tk.IntVar(value=52)
        self.g_var = tk.IntVar(value=152)
        self.b_var = tk.IntVar(value=219)

        # Red slider
        tk.Label(slider_frame, text="Red:", bg='#1e1e1e', fg='#ff5555', font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        tk.Scale(
            slider_frame,
            from_=0, to=255,
            orient=tk.HORIZONTAL,
            variable=self.r_var,
