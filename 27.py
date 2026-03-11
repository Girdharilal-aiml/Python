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

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.decks = json.load(f)
            except:
                self.decks = {}

    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.decks, f, indent=2, ensure_ascii=False)

    def display_decks(self):
        self.decks_listbox.delete(0, tk.END)
        for deck_name in self.decks.keys():
            count = len(self.decks[deck_name])
            self.decks_listbox.insert(tk.END, f"{deck_name} ({count})")

    def new_deck(self):
        name = simpledialog.askstring("New Deck", "Enter deck name:")
        if name and name.strip():
            name = name.strip()
            if name in self.decks:
                messagebox.showwarning("Exists", "Deck already exists!")
            else:
                self.decks[name] = []
                self.save_data()
                self.display_decks()

    def delete_deck(self):
        sel = self.decks_listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Select a deck first!")
            return
        
        deck_name = list(self.decks.keys())[sel[0]]
        if messagebox.askyesno("Delete", f"Delete '{deck_name}'?"):
            del self.decks[deck_name]
            self.save_data()
            self.display_decks()
            self.current_deck = None
            self.show_manage()

    def select_deck(self, event):
        sel = self.decks_listbox.curselection()
        if sel:
            self.current_deck = list(self.decks.keys())[sel[0]]
            if hasattr(self, 'current_mode'):
                if self.current_mode == 'manage':
                    self.show_manage()
                else:
                    self.show_study()

    def show_manage(self):
        self.current_mode = 'manage'
        self.manage_btn.config(bg='#2196F3', fg='white')
        self.study_btn.config(bg='#e0e0e0', fg='#333')
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.current_deck:
            tk.Label(
                self.content_frame,
                text="Select a deck to manage cards",
                font=('Arial', 14),
                bg='white',
                fg='#666'
            ).pack(pady=50)
            return

        # Header
        tk.Label(
            self.content_frame,
            text=f"Deck: {self.current_deck}",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#333'
        ).pack(pady=10)

        # Add card button
        tk.Button(
            self.content_frame,
            text="+ Add Card",
            command=self.add_card,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(pady=10)

        # Cards list
        cards_frame = tk.Frame(self.content_frame, bg='white')
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        cards = self.decks[self.current_deck]
        
        if not cards:
            tk.Label(
                cards_frame,
                text="No cards yet. Click '+ Add Card' to create one.",
                font=('Arial', 12),
                bg='white',
                fg='#999'
            ).pack(pady=20)
        else:
            for i, card in enumerate(cards):
                card_widget = tk.Frame(cards_frame, bg='#f5f5f5', relief=tk.SOLID, bd=1)
                card_widget.pack(fill=tk.X, pady=5)

                tk.Label(
                    card_widget,
                    text=f"Q: {card['question']}",
                    font=('Arial', 11, 'bold'),
                    bg='#f5f5f5',
                    fg='#333',
                    anchor='w',
                    wraplength=500
                ).pack(fill=tk.X, padx=10, pady=(8, 2))

                tk.Label(
                    card_widget,
                    text=f"A: {card['answer']}",
                    font=('Arial', 10),
                    bg='#f5f5f5',
                    fg='#666',
                    anchor='w',
                    wraplength=500
                ).pack(fill=tk.X, padx=10, pady=(2, 8))

                tk.Button(
                    card_widget,
                    text="Delete",
                    command=lambda idx=i: self.delete_card(idx),
                    font=('Arial', 8),
                    bg='#f44336',
                    fg='white',
                    bd=0,
                    cursor='hand2',
                    padx=8,
                    pady=3
                ).pack(side=tk.RIGHT, padx=10, pady=5)

    def add_card(self):
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Card")
        dialog.geometry("400x300")
        dialog.configure(bg='white')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="Question:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(pady=(20, 5), padx=20, anchor='w')

        question_text = tk.Text(dialog, font=('Arial', 10), height=3, width=40, relief=tk.SOLID, bd=1)
        question_text.pack(padx=20)

        tk.Label(
            dialog,
            text="Answer:",
            font=('Arial', 11, 'bold'),
            bg='white'
        ).pack(pady=(15, 5), padx=20, anchor='w')

        answer_text = tk.Text(dialog, font=('Arial', 10), height=3, width=40, relief=tk.SOLID, bd=1)
        answer_text.pack(padx=20)

        def save():
            q = question_text.get('1.0', 'end-1c').strip()
            a = answer_text.get('1.0', 'end-1c').strip()
            
            if q and a:
                self.decks[self.current_deck].append({'question': q, 'answer': a})
                self.save_data()
                self.display_decks()
                self.show_manage()
                dialog.destroy()
            else:
                messagebox.showwarning("Empty Fields", "Please fill both fields!")

        tk.Button(
            dialog,
            text="Add Card",
            command=save,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(pady=20)

    def delete_card(self, index):
        if messagebox.askyesno("Delete", "Delete this card?"):
            self.decks[self.current_deck].pop(index)
            self.save_data()
            self.display_decks()
            self.show_manage()

    def show_study(self):
        self.current_mode = 'study'
        self.manage_btn.config(bg='#e0e0e0', fg='#333')
        self.study_btn.config(bg='#2196F3', fg='white')
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not self.current_deck:
            tk.Label(
                self.content_frame,
                text="Select a deck to study",
                font=('Arial', 14),
                bg='white',
                fg='#666'
            ).pack(pady=50)
            return

        cards = self.decks[self.current_deck]
        
        if not cards:
            tk.Label(
                self.content_frame,
                text="No cards in this deck",
                font=('Arial', 14),
                bg='white',
                fg='#666'
            ).pack(pady=50)
            return

