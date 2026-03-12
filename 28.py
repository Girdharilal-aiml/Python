"""
Math Quiz Game - Simple & Perfect UI
Practice math with different difficulty levels
"""

import tkinter as tk
from tkinter import messagebox
import random
import time

class MathQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("600x650")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(500, 550)

        # Game state
        self.score = 0
        self.total_questions = 0
        self.difficulty = 'Easy'
        self.operations = ['+', '-', '×', '÷']
        self.selected_operations = ['+', '-']
        self.quiz_active = False
        self.questions_per_quiz = 10
        self.current_answer = None
        self.start_time = None

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧮 Math Quiz",
            font=('Arial', 20, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=15)

        # Score panel
        score_frame = tk.Frame(root, bg='white')
        score_frame.pack(pady=8)

        tk.Label(
            score_frame,
            text="SCORE:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#666'
        ).pack(side=tk.LEFT, padx=5)

        self.score_label = tk.Label(
            score_frame,
            text="0 / 0",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#4CAF50'
        )
        self.score_label.pack(side=tk.LEFT, padx=5)

        # Settings
        settings_frame = tk.LabelFrame(
            root,
            text="Settings",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#333',
            relief=tk.SOLID,
            bd=1
        )
        settings_frame.pack(fill=tk.X, padx=40, pady=8)

        # Difficulty
        diff_frame = tk.Frame(settings_frame, bg='white')
        diff_frame.pack(pady=8)

        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT, padx=10)

        self.diff_buttons = {}
        for level in ['Easy', 'Medium', 'Hard']:
            btn = tk.Button(
                diff_frame,
                text=level,
                command=lambda l=level: self.set_difficulty(l),
                font=('Arial', 10, 'bold'),
                bg='#4CAF50' if level == 'Easy' else '#e0e0e0',
                fg='white' if level == 'Easy' else '#333',
                bd=0,
                cursor='hand2',
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.diff_buttons[level] = btn

        # Operations
        ops_frame = tk.Frame(settings_frame, bg='white')
        ops_frame.pack(pady=8)

        tk.Label(
            ops_frame,
            text="Operations:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT, padx=10)

        self.op_vars = {}
        for op in self.operations:
            var = tk.BooleanVar(value=(op in ['+', '-']))
            self.op_vars[op] = var
            
            cb = tk.Checkbutton(
                ops_frame,
                text=op,
                variable=var,
                font=('Arial', 14, 'bold'),
                bg='white',
                fg='#333',
                selectcolor='white',
                command=self.update_operations
            )
            cb.pack(side=tk.LEFT, padx=8)

