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

        tk.Button(
            header,
            text="+",
            command=self.new_deck,
            font=('Arial', 16, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=2,
            bd=0,
            cursor='hand2'
        ).pack(side=tk.RIGHT)

        # Decks list
        list_frame = tk.Frame(sidebar, bg='#f5f5f5')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.decks_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='white',
            fg='#333',
            selectbackground='#2196F3',
            selectforeground='white',
            bd=1,
            relief=tk.SOLID,
            yscrollcommand=scroll.set
        )
        self.decks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.decks_listbox.yview)
        self.decks_listbox.bind('<<ListboxSelect>>', self.select_deck)

        # Deck actions
        actions = tk.Frame(sidebar, bg='#f5f5f5')
        actions.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            actions,
            text="Delete Deck",
            command=self.delete_deck,
            font=('Arial', 9, 'bold'),
            bg='#f44336',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=10,
            pady=5
        ).pack(fill=tk.X)

        # Right side - Main area
        right_frame = tk.Frame(main_container, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Tabs
        tabs_frame = tk.Frame(right_frame, bg='#f5f5f5', height=50)
        tabs_frame.pack(fill=tk.X)
        tabs_frame.pack_propagate(False)

        self.manage_btn = tk.Button(
            tabs_frame,
            text="Manage Cards",
            command=self.show_manage,
            font=('Arial', 11, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.manage_btn.pack(side=tk.LEFT, padx=2, pady=5)

        self.study_btn = tk.Button(
            tabs_frame,
            text="Study Mode",
            command=self.show_study,
            font=('Arial', 11, 'bold'),
            bg='#e0e0e0',
            fg='#333',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=10
        )
        self.study_btn.pack(side=tk.LEFT, padx=2, pady=5)

        # Content area
        self.content_frame = tk.Frame(right_frame, bg='white')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Load decks
        self.display_decks()
        self.show_manage()

