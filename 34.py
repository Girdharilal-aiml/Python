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
