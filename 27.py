"""
Flashcard App - Simple & Perfect UI
Create decks, study, and track progress
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import random

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcards")
        self.root.geometry("800x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(600, 500)

