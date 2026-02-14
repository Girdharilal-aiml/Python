"""
To-Do List App
Lightweight GUI app using tkinter

FEATURES:
- Add, delete, and mark tasks as complete
- Tasks save automatically to a file
- Priority levels (High, Medium, Low)
- Search/filter tasks
- Clean, simple interface
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # File to save tasks
        self.data_file = "tasks.json"
        self.tasks = []
        
        # Load existing tasks
        self.load_tasks()
        
        # Title
        title_label = tk.Label(
            root, 
            text="📝 My To-Do List", 
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(root, bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill=tk.X)
        
    