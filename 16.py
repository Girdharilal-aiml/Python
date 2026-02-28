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

