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
