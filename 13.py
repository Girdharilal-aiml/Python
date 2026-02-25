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
            fg='#c9d1d9',
            selectcolor='#0d1117',
            activebackground='#161b22',
            activeforeground='#58a6ff'
        )
        imperial_btn.pack(side=tk.LEFT, padx=10)

        # Input card
        input_card = tk.Frame(main_frame, bg='#161b22')
        input_card.pack(fill=tk.X, pady=10)

        # Weight input
        weight_frame = tk.Frame(input_card, bg='#161b22')
        weight_frame.pack(fill=tk.X, padx=20, pady=15)

        self.weight_label = tk.Label(
            weight_frame,
            text="Weight (kg):",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        )
        self.weight_label.pack(anchor='w', pady=(0, 8))

        self.weight_entry = tk.Entry(
            weight_frame,
            font=('Arial', 18),
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=0
        )
        self.weight_entry.pack(fill=tk.X, ipady=10)

        # Height input
        height_frame = tk.Frame(input_card, bg='#161b22')
        height_frame.pack(fill=tk.X, padx=20, pady=15)

        self.height_label = tk.Label(
            height_frame,
            text="Height (cm):",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        )
        self.height_label.pack(anchor='w', pady=(0, 8))

        self.height_entry = tk.Entry(
            height_frame,
            font=('Arial', 18),
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=0
        )
        self.height_entry.pack(fill=tk.X, ipady=10)

        # Calculate button
        calc_btn = tk.Button(
            main_frame,
            text="Calculate BMI",
            command=self.calculate_bmi,
            bg='#238636',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#2ea043',
            activeforeground='white'
        )
        calc_btn.pack(pady=25, ipadx=40, ipady=12)

        # Result card
        self.result_card = tk.Frame(main_frame, bg='#161b22')
        self.result_card.pack(fill=tk.BOTH, expand=True, pady=10)

        # BMI value
        self.bmi_label = tk.Label(
            self.result_card,
            text="--",
            font=self.result_font,
            bg='#161b22',
            fg='#8b949e'
        )
        self.bmi_label.pack(pady=(30, 5))

        tk.Label(
            self.result_card,
            text="Your BMI",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e'
        ).pack()

        # Category
        self.category_label = tk.Label(
            self.result_card,
            text="",
            font=('Arial', 16, 'bold'),
