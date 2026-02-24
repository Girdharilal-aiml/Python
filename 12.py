"""
Stopwatch with Lap Timer - Modern UI
Beautiful redesign with better visuals
"""

import tkinter as tk
from tkinter import font as tkfont
import time

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("500x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.laps = []

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.time_font = tkfont.Font(family='Courier New', size=56, weight='bold')
        self.btn_font = tkfont.Font(family='Arial', size=13, weight='bold')

        # Main container with gradient effect
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title with modern styling
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="⏱",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Stopwatch",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Time display with modern card design
        time_card = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT, bd=0)
        time_card.pack(pady=10, fill=tk.X)

        self.time_label = tk.Label(
            time_card,
            text="00:00:00.00",
            font=self.time_font,
            bg='#161b22',
            fg='#58a6ff',
            pady=30
        )
        self.time_label.pack()

        # Milliseconds label
        millisec_label = tk.Label(
            time_card,
            text="HH : MM : SS . CS",
            font=('Arial', 10),
            bg='#161b22',
            fg='#8b949e'
        )
