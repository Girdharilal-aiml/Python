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
