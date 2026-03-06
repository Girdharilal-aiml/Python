"""
Note-Taking App - Simple & Perfect UI
Clean, functional note-taking app
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.root.geometry("900x600")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(700, 500)

        # Data
        self.notes_file = "notes_data.json"
        self.notes = []
        self.current_note_index = None
        self.load_notes()

        # Main split
        # LEFT - Notes list (250px)
        left_frame = tk.Frame(root, bg='#f5f5f5', width=250, relief=tk.FLAT, bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        left_frame.pack_propagate(False)

        # Header
        header = tk.Frame(left_frame, bg='#f5f5f5')
        header.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            header,
            text="📝 Notes",
            font=('Arial', 16, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT)

        tk.Button(
            header,
            text="+",
            command=self.new_note,
            font=('Arial', 18, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=2,
            bd=0,
            cursor='hand2',
            activebackground='#45a049'
        ).pack(side=tk.RIGHT)

        # Search
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_notes())
        
        search = tk.Entry(
            left_frame,
            textvariable=self.search_var,
            font=('Arial', 10),
            bg='white',
            relief=tk.SOLID,
            bd=1
        )
        search.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Notes list
        list_frame = tk.Frame(left_frame, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            font=('Arial', 10),
            bg='white',
            fg='#333',
            selectbackground='#2196F3',
            selectforeground='white',
            bd=0,
            highlightthickness=0,
            yscrollcommand=scroll.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.select_note)

        # RIGHT - Editor
        right_frame = tk.Frame(root, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Title
        title_frame = tk.Frame(right_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 5))

        tk.Label(
            title_frame,
            text="Title:",
            font=('Arial', 10),
            bg='white',
            fg='#666'
        ).pack(anchor='w')

