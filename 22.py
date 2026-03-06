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

        
