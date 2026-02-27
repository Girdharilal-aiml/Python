"""
Age Calculator - Modern UI
Calculate exact age with detailed breakdown
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from datetime import datetime, date

class AgeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")
        self.root.geometry("550x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.result_font = tkfont.Font(family='Arial', size=48, weight='bold')

