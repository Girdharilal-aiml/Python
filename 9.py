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
