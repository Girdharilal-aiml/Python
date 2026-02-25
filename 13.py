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

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.result_font = tkfont.Font(family='Arial', size=48, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="⚖️",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="BMI Calculator",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Unit selector
        unit_frame = tk.Frame(main_frame, bg='#161b22')
        unit_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            unit_frame,
            text="Units:",
            font=('Arial', 12, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, padx=20, pady=15)

        self.unit_var = tk.StringVar(value="metric")

        metric_btn = tk.Radiobutton(
            unit_frame,
            text="Metric (kg, cm)",
            variable=self.unit_var,
            value="metric",
            command=self.update_labels,
            font=('Arial', 11),
            bg='#161b22',
            fg='#c9d1d9',
            selectcolor='#0d1117',
            activebackground='#161b22',
            activeforeground='#58a6ff'
        )
        metric_btn.pack(side=tk.LEFT, padx=10)

        imperial_btn = tk.Radiobutton(
            unit_frame,
            text="Imperial (lbs, inches)",
            variable=self.unit_var,
            value="imperial",
            command=self.update_labels,
            font=('Arial', 11),
            bg='#161b22',
