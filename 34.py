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

        tk.Button(
            input_frame,
            text="🔍 SEARCH",
            command=self.search_files,
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Filters
        filter_frame = tk.Frame(root, bg='#f5f5f5')
        filter_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(
            filter_frame,
            text="Filters:",
            font=('Arial', 10, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=(0, 15))

        # File type filter
        tk.Label(
            filter_frame,
            text="Type:",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.file_type = tk.StringVar(value='All')
        types = ['All', 'Documents', 'Images', 'Videos', 'Audio', 'Code']
        
        type_menu = tk.OptionMenu(filter_frame, self.file_type, *types)
        type_menu.config(
            font=('Arial', 9),
            bg='white',
            fg='#333',
            bd=1,
            relief=tk.SOLID,
            cursor='hand2'
        )
        type_menu.pack(side=tk.LEFT, padx=(0, 15))

        # Case sensitive
        self.case_sensitive = tk.BooleanVar(value=False)
        tk.Checkbutton(
            filter_frame,
            text="Case sensitive",
            variable=self.case_sensitive,
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#333',
            selectcolor='white'
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Search in subdirectories
        self.search_subdirs = tk.BooleanVar(value=True)
        tk.Checkbutton(
            filter_frame,
            text="Include subdirectories",
            variable=self.search_subdirs,
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#333',
            selectcolor='white'
        ).pack(side=tk.LEFT)

        # Main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Results list
        results_frame = tk.Frame(main_container, bg='white')
        results_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            results_frame,
            text="Results:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333',
            anchor='w'
        ).pack(fill=tk.X, pady=(0, 5))

        # Listbox with scrollbar
        list_container = tk.Frame(results_frame, bg='white', relief=tk.SOLID, bd=1)
        list_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_listbox = tk.Listbox(
            list_container,
            font=('Consolas', 9),
            bg='white',
            fg='#333',
            selectbackground='#2196F3',
            selectforeground='white',
            bd=0,
            yscrollcommand=scrollbar.set
        )
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_listbox.yview)

        self.results_listbox.bind('<<ListboxSelect>>', self.show_file_info)
        self.results_listbox.bind('<Double-Button-1>', self.open_file)

        # File info panel
        info_frame = tk.Frame(main_container, bg='#f5f5f5', width=300, relief=tk.SOLID, bd=1)
        info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        info_frame.pack_propagate(False)

        tk.Label(
            info_frame,
            text="File Info",
            font=('Arial', 12, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=15)

        # Info text
        info_scroll = tk.Scrollbar(info_frame)
        info_scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5))

        self.info_text = tk.Text(
            info_frame,
            font=('Arial', 9),
            bg='white',
            fg='#333',
            wrap=tk.WORD,
            bd=0,
            padx=10,
            pady=10,
            state='disabled',
            yscrollcommand=info_scroll.set
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        info_scroll.config(command=self.info_text.yview)

        # Action buttons
        btn_frame = tk.Frame(info_frame, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="Open File",
            command=self.open_file,
            font=('Arial', 9, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=5
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_frame,
            text="Open Location",
            command=self.open_location,
            font=('Arial', 9, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=5
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_frame,
            text="Copy Path",
            command=self.copy_path,
            font=('Arial', 9, 'bold'),
            bg='#FF9800',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=5
        ).pack(fill=tk.X, pady=2)
