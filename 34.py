"""
File Search Tool - Simple & Perfect UI
Search files with filters and preview
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
import subprocess
import sys

class FileSearchTool:
    def __init__(self, root):
        self.root = root
        self.root.title("File Search Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        # Search state
        self.search_path = str(Path.home())
        self.results = []

        # Header
        header = tk.Frame(root, bg='#2196F3', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔍 File Search Tool",
            font=('Arial', 24, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=18)

        # Search controls
        search_frame = tk.Frame(root, bg='#f5f5f5')
        search_frame.pack(fill=tk.X, padx=20, pady=15)

        # Path selection
        path_frame = tk.Frame(search_frame, bg='#f5f5f5')
        path_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            path_frame,
            text="Search in:",
            font=('Arial', 10, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.path_entry = tk.Entry(
            path_frame,
            font=('Arial', 10),
            bg='white',
            fg='#333',
            relief=tk.SOLID,
            bd=1
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        self.path_entry.insert(0, self.search_path)

        tk.Button(
            path_frame,
            text="Browse",
            command=self.browse_path,
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Search input
        input_frame = tk.Frame(search_frame, bg='#f5f5f5')
        input_frame.pack(fill=tk.X)

        tk.Label(
            input_frame,
            text="Filename:",
            font=('Arial', 10, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.search_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            bg='white',
            fg='#333',
            relief=tk.SOLID,
            bd=1
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        self.search_entry.bind('<Return>', lambda e: self.search_files())
