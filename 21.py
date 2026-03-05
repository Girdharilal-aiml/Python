"""
Language Quiz - Modern UI (Responsive)
Practice vocabulary with multiple languages
"""

import tkinter as tk
from tkinter import font as tkfont
import random

class LanguageQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Quiz")
        self.root.geometry("700x800")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Vocabulary database
        self.vocabularies = {

