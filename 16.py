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

