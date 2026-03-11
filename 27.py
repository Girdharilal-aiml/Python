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

        # Data
        self.data_file = "flashcards.json"
        self.decks = {}
        self.current_deck = None
        self.current_cards = []
        self.current_index = 0
        self.show_answer = False
        self.load_data()

        # Main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - Decks
        sidebar = tk.Frame(main_container, bg='#f5f5f5', width=250, relief=tk.SOLID, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Sidebar header
        header = tk.Frame(sidebar, bg='#f5f5f5')
        header.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            header,
            text="📚 My Decks",
            font=('Arial', 16, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT)

