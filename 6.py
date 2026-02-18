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

        tk.Label(input_frame, text="Hours:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=0, padx=5)
        tk.Label(input_frame, text="Minutes:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="Seconds:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=2, padx=5)

        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")

        hours_entry = tk.Entry(input_frame, textvariable=self.hours_var, width=8, font=('Arial', 18), justify='center')
        hours_entry.grid(row=1, column=0, padx=5)

        minutes_entry = tk.Entry(input_frame, textvariable=self.minutes_var, width=8, font=('Arial', 18), justify='center')
        minutes_entry.grid(row=1, column=1, padx=5)

        seconds_entry = tk.Entry(input_frame, textvariable=self.seconds_var, width=8, font=('Arial', 18), justify='center')
        seconds_entry.grid(row=1, column=2, padx=5)

        # Quick preset buttons
        preset_frame = tk.Frame(root, bg='#0f0f0f')
        preset_frame.pack(pady=10)

        tk.Label(preset_frame, text="Quick Set:", bg='#0f0f0f', fg='#aaa', font=('Arial', 10)).pack()

        presets_inner = tk.Frame(preset_frame, bg='#0f0f0f')
        presets_inner.pack(pady=5)

        presets = [
            ("1 min", 0, 1, 0),
            ("5 min", 0, 5, 0),
            ("10 min", 0, 10, 0),
            ("25 min", 0, 25, 0),
            ("1 hour", 1, 0, 0)
        ]

        for text, h, m, s in presets:
            tk.Button(
                presets_inner,
                text=text,
                command=lambda h=h, m=m, s=s: self.set_preset(h, m, s),
                bg='#2c2c2c',
                fg='white',
                font=('Arial', 9),
                cursor='hand2',
                bd=0,
                width=8
            ).pack(side=tk.LEFT, padx=3)

        # Control buttons
        btn_frame = tk.Frame(root, bg='#0f0f0f')
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start",
            command=self.start,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            cursor='hand2',
            bd=0
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
