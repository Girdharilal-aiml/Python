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
