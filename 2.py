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
        
        self.task_entry = tk.Entry(
            input_frame,
            font=('Arial', 12),
            width=30
        )
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Priority dropdown
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = tk.OptionMenu(
            input_frame,
            self.priority_var,
            "High",
            "Medium",
            "Low"
        )
        priority_menu.config(width=8)
        priority_menu.pack(side=tk.LEFT, padx=5)
        
        # Add button
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = tk.Frame(root, bg='#f0f0f0')
        search_frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(search_frame, text="🔍 Search:", bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=('Arial', 10), width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_tasks())
        
        clear_search_btn = tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            font=('Arial', 8)
        )
        clear_search_btn.pack(side=tk.LEFT, padx=5)
        
        # Task list frame with scrollbar
        list_frame = tk.Frame(root, bg='white')
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    