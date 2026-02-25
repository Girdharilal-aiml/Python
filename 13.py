"""
BMI Calculator - Modern UI
Calculate Body Mass Index with health categories
"""

import tkinter as tk
from tkinter import font as tkfont
import math

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("500x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)
