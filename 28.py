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
