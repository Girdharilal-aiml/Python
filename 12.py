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
