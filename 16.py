"""
Typing Speed Test - Modern UI
Test your typing speed (WPM) and accuracy
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)  # Allow resizing
        self.root.minsize(600, 500)  # Set minimum size

        # Test paragraphs
        self.paragraphs = [
            "The quick brown fox jumps over the lazy dog near the riverbank.",
            "Programming is the art of telling a computer what to do through code.",
            "Practice makes perfect when learning to type faster and more accurately.",
            "Technology has changed the way we communicate and share information.",
            "Typing speed is measured in words per minute and accuracy percentage.",
            "The best time to plant a tree was twenty years ago. The second best time is now.",
            "Success is not final, failure is not fatal. It is the courage to continue that counts.",
            "Life is what happens when you are busy making other plans for the future.",
            "The only way to do great work is to love what you do every single day.",
            "Innovation distinguishes between a leader and a follower in any field.",
        ]

        # Test state
        self.current_text = ""
        self.start_time = None
        self.test_running = False
        self.test_completed = False

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.text_font = tkfont.Font(family='Georgia', size=16)
        self.input_font = tkfont.Font(family='Courier New', size=14)

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="⌨️",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Typing Speed Test",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Instructions
        instructions_frame = tk.Frame(main_frame, bg='#161b22')
        instructions_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            instructions_frame,
            text="📝 Type the text below as fast and accurately as you can!",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e'
        ).pack(pady=12)

        # Text to type card
        text_card = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        text_card.pack(fill=tk.X, pady=10)

        tk.Label(
            text_card,
            text="Text to Type:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', padx=20, pady=(15, 10))

        self.text_label = tk.Label(
            text_card,
            text="Click 'Start Test' to begin",
            font=self.text_font,
            bg='#161b22',
            fg='#58a6ff',
            wraplength=700,
            justify='left'
        )
        self.text_label.pack(padx=20, pady=(0, 20), anchor='w', fill=tk.X)
        
        # Bind resize event to update wraplength
        self.root.bind('<Configure>', self.on_resize)

        # Input area
        input_card = tk.Frame(main_frame, bg='#161b22')
        input_card.pack(fill=tk.X, pady=10)

        tk.Label(
            input_card,
            text="Your Typing:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', padx=20, pady=(15, 10))

        self.input_text = tk.Text(
            input_card,
            font=self.input_font,
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=0,
            height=4,
            wrap=tk.WORD,
            state='disabled'
        )
        self.input_text.pack(padx=20, pady=(0, 15), fill=tk.X)
        self.input_text.bind('<KeyRelease>', self.on_type)

        # Timer and stats
        self.stats_frame = tk.Frame(main_frame, bg='#0d1117')
        self.stats_frame.pack(pady=15, fill=tk.X)

        # Create stats cards with grid for better responsiveness
        self.stats_container = tk.Frame(self.stats_frame, bg='#0d1117')
        self.stats_container.pack()

        # Timer
        timer_card = tk.Frame(self.stats_container, bg='#161b22')
        timer_card.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

