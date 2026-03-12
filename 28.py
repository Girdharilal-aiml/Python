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

        # Question area
        question_frame = tk.Frame(root, bg='#2196F3', relief=tk.SOLID, bd=0, height=150)
        question_frame.pack(fill=tk.X, padx=40, pady=10)
        question_frame.pack_propagate(False)

        self.question_label = tk.Label(
            question_frame,
            text="Click 'Start Quiz' to begin",
            font=('Arial', 28, 'bold'),
            bg='#2196F3',
            fg='white',
            wraplength=500
        )
        self.question_label.pack(expand=True)

        # Answer input
        answer_container = tk.Frame(root, bg='white')
        answer_container.pack(pady=8)

        tk.Label(
            answer_container,
            text="Your Answer:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#333'
        ).pack()

        self.answer_entry = tk.Entry(
            answer_container,
            font=('Arial', 20, 'bold'),
            bg='#f5f5f5',
            fg='#333',
            relief=tk.SOLID,
            bd=2,
            justify='center',
            width=15,
            state='disabled'
        )
        self.answer_entry.pack(pady=5, ipady=8)
        self.answer_entry.bind('<Return>', lambda e: self.submit_answer())

        # Result feedback
        self.result_label = tk.Label(
            root,
            text="",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#4CAF50'
        )
        self.result_label.pack(pady=5)

        # Progress
        self.progress_label = tk.Label(
            root,
            text="",
            font=('Arial', 11),
            bg='white',
            fg='#666'
        )
        self.progress_label.pack()

        # Buttons
        btn_frame = tk.Frame(root, bg='white')
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ START QUIZ",
            command=self.start_quiz,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=25,
            pady=12
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.submit_btn = tk.Button(
            btn_frame,
            text="SUBMIT",
            command=self.submit_answer,
            font=('Arial', 14, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=25,
            pady=12,
            state='disabled'
        )
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(
            btn_frame,
            text="NEXT ➜",
            command=self.next_question,
            font=('Arial', 14, 'bold'),
            bg='#FF9800',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=25,
            pady=12,
            state='disabled'
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)

    def set_difficulty(self, level):
        self.difficulty = level
        for lvl, btn in self.diff_buttons.items():
            if lvl == level:
                btn.config(bg='#4CAF50', fg='white')
            else:
                btn.config(bg='#e0e0e0', fg='#333')

    def update_operations(self):
        self.selected_operations = [op for op, var in self.op_vars.items() if var.get()]
        if not self.selected_operations:
            messagebox.showwarning("No Operations", "Select at least one operation!")
            self.op_vars['+'].set(True)
            self.selected_operations = ['+']

    def start_quiz(self):
        self.quiz_active = True
        self.score = 0
        self.total_questions = 0
        self.start_time = time.time()
        
        self.start_btn.config(state='disabled')
        self.answer_entry.config(state='normal')
        self.submit_btn.config(state='normal')
        
        self.score_label.config(text="0 / 0")
        self.result_label.config(text="")
        
        self.generate_question()

    def generate_question(self):
        if self.total_questions >= self.questions_per_quiz:
            self.end_quiz()
            return

        # Clear previous
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.result_label.config(text="")
        
        # Generate based on difficulty
        operation = random.choice(self.selected_operations)
        
        if self.difficulty == 'Easy':
            num1 = random.randint(1, 20)
            num2 = random.randint(1, 20)
        elif self.difficulty == 'Medium':
            num1 = random.randint(10, 50)
            num2 = random.randint(10, 50)
        else:  # Hard
            num1 = random.randint(20, 100)
            num2 = random.randint(20, 100)
        
        # Calculate answer
        if operation == '+':
            self.current_answer = num1 + num2
            question = f"{num1} + {num2}"
        elif operation == '-':
            # Make sure result is positive
            if num1 < num2:
                num1, num2 = num2, num1
            self.current_answer = num1 - num2
            question = f"{num1} - {num2}"
        elif operation == '×':
            if self.difficulty == 'Easy':
                num1 = random.randint(1, 12)
                num2 = random.randint(1, 12)
            self.current_answer = num1 * num2
            question = f"{num1} × {num2}"
        elif operation == '÷':
            # Make sure division is exact
            if self.difficulty == 'Easy':
                divisor = random.randint(2, 10)
                quotient = random.randint(2, 10)
            elif self.difficulty == 'Medium':
                divisor = random.randint(2, 12)
                quotient = random.randint(5, 15)
            else:
                divisor = random.randint(5, 20)
                quotient = random.randint(5, 20)
            
            num1 = divisor * quotient
            num2 = divisor
            self.current_answer = quotient
            question = f"{num1} ÷ {num2}"
        
        self.question_label.config(text=question)
        self.progress_label.config(text=f"Question {self.total_questions + 1} / {self.questions_per_quiz}")

    def submit_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            
            self.total_questions += 1
            
            if user_answer == self.current_answer:
                self.score += 1
                self.result_label.config(text="✓ Correct!", fg='#4CAF50')
                self.question_label.config(bg='#4CAF50')
