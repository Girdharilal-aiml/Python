"""
Password Generator
Generate secure random passwords with customization
"""

import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x650")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        # Title
        tk.Label(
            root,
            text="🔐 Password Generator",
            font=('Arial', 24, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(pady=20)

        # Password display
        self.password_var = tk.StringVar(value="Click Generate!")
        password_display = tk.Entry(
            root,
            textvariable=self.password_var,
            font=('Courier', 16, 'bold'),
            bg='#16213e',
            fg='#00ff00',
            justify='center',
            state='readonly',
            relief=tk.SUNKEN,
            bd=5
        )
        password_display.pack(pady=15, padx=30, fill=tk.X, ipady=10)

        # Copy button
        tk.Button(
            root,
            text="📋 Copy to Clipboard",
            command=self.copy_password,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            cursor='hand2',
            bd=0,
            width=20,
            height=2
        ).pack(pady=10)

        # Settings frame
        settings_frame = tk.Frame(root, bg='#1a1a2e')
        settings_frame.pack(pady=20, padx=30, fill=tk.X)

        # Password length
        tk.Label(
            settings_frame,
            text="Password Length:",
            font=('Arial', 12, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(anchor='w', pady=(10, 5))

        length_frame = tk.Frame(settings_frame, bg='#1a1a2e')
        length_frame.pack(fill=tk.X, pady=5)

        self.length_var = tk.IntVar(value=12)
        tk.Scale(
            length_frame,
            from_=4,
            to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg='#16213e',
            fg='white',
            highlightthickness=0,
            length=350,
            troughcolor='#0e7c7b'
        ).pack(side=tk.LEFT)

        self.length_label = tk.Label(
            length_frame,
            text="12",
            font=('Arial', 16, 'bold'),
            bg='#1a1a2e',
            fg='#f39c12',
            width=3
        )
        self.length_label.pack(side=tk.LEFT, padx=10)

        self.length_var.trace('w', self.update_length_label)

        # Character options
        tk.Label(
            settings_frame,
            text="Include:",
            font=('Arial', 12, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(anchor='w', pady=(20, 5))

        options_frame = tk.Frame(settings_frame, bg='#1a1a2e')
        options_frame.pack(fill=tk.X)

        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Uppercase (A-Z)",
            variable=self.uppercase_var,
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='white',
            selectcolor='#16213e',
            activebackground='#1a1a2e',
            activeforeground='white'
        ).pack(anchor='w', pady=3)

        self.lowercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Lowercase (a-z)",
            variable=self.lowercase_var,
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='white',
            selectcolor='#16213e',
            activebackground='#1a1a2e',
            activeforeground='white'
        ).pack(anchor='w', pady=3)

        self.numbers_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="Numbers (0-9)",
            variable=self.numbers_var,
            font=('Arial', 11),
            bg='#1a1a2e',
            fg='white',
            selectcolor='#16213e',
            activebackground='#1a1a2e',
            activeforeground='white'
        ).pack(anchor='w', pady=3)

