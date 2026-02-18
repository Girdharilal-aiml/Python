"""
Countdown Timer
Simple & useful timer with tkinter
"""

import tkinter as tk
from tkinter import messagebox
import time

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("450x500")
        self.root.configure(bg='#0f0f0f')
        self.root.resizable(False, False)

        self.running = False
        self.paused = False
        self.time_left = 0  # in seconds

        # Title
        tk.Label(
            root,
            text="⏱️ Countdown Timer",
            font=('Arial', 24, 'bold'),
            bg='#0f0f0f',
            fg='white'
        ).pack(pady=20)

        # Time display
        self.time_label = tk.Label(
            root,
            text="00:00:00",
            font=('Courier', 56, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00',
            relief=tk.SUNKEN,
            bd=5
        )
        self.time_label.pack(pady=20, padx=30, fill=tk.X)

        # Input frame
        input_frame = tk.Frame(root, bg='#0f0f0f')
        input_frame.pack(pady=20)

