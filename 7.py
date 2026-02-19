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
            bg='#2c2c2c',
            fg='#ff5555',
            highlightthickness=0,
            command=self.on_slider_change,
            length=300,
            troughcolor='#ff5555'
        ).grid(row=0, column=1, pady=5, padx=10)
        self.r_label = tk.Label(slider_frame, text="52", bg='#1e1e1e', fg='white', font=('Courier', 11, 'bold'), width=4)
        self.r_label.grid(row=0, column=2)

        # Green slider
        tk.Label(slider_frame, text="Green:", bg='#1e1e1e', fg='#55ff55', font=('Arial', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        tk.Scale(
            slider_frame,
            from_=0, to=255,
            orient=tk.HORIZONTAL,
            variable=self.g_var,
            bg='#2c2c2c',
            fg='#55ff55',
            highlightthickness=0,
            command=self.on_slider_change,
            length=300,
            troughcolor='#55ff55'
        ).grid(row=1, column=1, pady=5, padx=10)
        self.g_label = tk.Label(slider_frame, text="152", bg='#1e1e1e', fg='white', font=('Courier', 11, 'bold'), width=4)
        self.g_label.grid(row=1, column=2)

        # Blue slider
        tk.Label(slider_frame, text="Blue:", bg='#1e1e1e', fg='#5555ff', font=('Arial', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        tk.Scale(
            slider_frame,
            from_=0, to=255,
            orient=tk.HORIZONTAL,
            variable=self.b_var,
            bg='#2c2c2c',
            fg='#5555ff',
            highlightthickness=0,
            command=self.on_slider_change,
            length=300,
            troughcolor='#5555ff'
        ).grid(row=2, column=1, pady=5, padx=10)
        self.b_label = tk.Label(slider_frame, text="219", bg='#1e1e1e', fg='white', font=('Courier', 11, 'bold'), width=4)
        self.b_label.grid(row=2, column=2)

        # Buttons
        btn_frame = tk.Frame(root, bg='#1e1e1e')
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="🎲 Random Color",
            command=self.random_color,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 12, 'bold'),
            cursor='hand2',
            bd=0,
            width=18,
            height=2
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="📋 Copy HEX",
            command=lambda: self.copy_code(self.hex_var.get()),
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            cursor='hand2',
            bd=0,
            width=18,
            height=2
        ).pack(side=tk.LEFT, padx=5)

    def on_slider_change(self, event=None):
        r = self.r_var.get()
        g = self.g_var.get()
        b = self.b_var.get()

        # Update labels
        self.r_label.config(text=str(r))
        self.g_label.config(text=str(g))
        self.b_label.config(text=str(b))

