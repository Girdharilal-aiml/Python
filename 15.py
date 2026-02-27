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

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🎂",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Age Calculator",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Input card
        input_card = tk.Frame(main_frame, bg='#161b22')
        input_card.pack(fill=tk.X, pady=10)

        # Birth date section
        birth_frame = tk.Frame(input_card, bg='#161b22')
        birth_frame.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            birth_frame,
            text="Birth Date:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', pady=(0, 10))

        date_inputs = tk.Frame(birth_frame, bg='#161b22')
        date_inputs.pack(fill=tk.X)

        # Day
        day_frame = tk.Frame(date_inputs, bg='#161b22')
        day_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        tk.Label(day_frame, text="Day", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.day_var = tk.StringVar()
        day_spin = tk.Spinbox(
            day_frame,
            from_=1,
            to=31,
            textvariable=self.day_var,
            font=('Arial', 16),
            bg='#0d1117',
            fg='#c9d1d9',
            buttonbackground='#21262d',
            relief=tk.FLAT,
            bd=0,
            width=8
        )
        day_spin.pack(fill=tk.X, ipady=8)

        # Month
        month_frame = tk.Frame(date_inputs, bg='#161b22')
        month_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Label(month_frame, text="Month", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.month_var = tk.StringVar()
        month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"],
            state='readonly',
            font=('Arial', 12),
            width=10
        )
        month_combo.pack(fill=tk.X, ipady=6)
        month_combo.current(0)

        # Year
        year_frame = tk.Frame(date_inputs, bg='#161b22')
        year_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        tk.Label(year_frame, text="Year", font=('Arial', 9), bg='#161b22', fg='#8b949e').pack(anchor='w')
        self.year_var = tk.StringVar()
        year_spin = tk.Spinbox(
            year_frame,
            from_=1900,
            to=datetime.now().year,
            textvariable=self.year_var,
            font=('Arial', 16),
            bg='#0d1117',
            fg='#c9d1d9',
