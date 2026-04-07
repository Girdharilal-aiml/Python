"""
eBook Reader - Simple & Perfect UI
Read TXT/PDF files with bookmarks and table of contents
Requires: pip install PyPDF2
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import json
import os

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

class EBookReader:
    def __init__(self, root):
        self.root = root
        self.root.title("eBook Reader")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f5f5dc')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        # Data
        self.bookmarks_file = "bookmarks.json"
        self.bookmarks = {}
        self.current_file = None
        self.current_page = 0
        self.total_pages = 0
        self.pdf_reader = None
        self.file_type = None
        self.load_bookmarks()

        # Menu bar
        menubar = tk.Menu(root, bg='#e8e8d8', fg='#333', bd=0)
        root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg='#e8e8d8', fg='#333')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Bookmarks menu
        bookmarks_menu = tk.Menu(menubar, tearoff=0, bg='#e8e8d8', fg='#333')
        menubar.add_cascade(label="Bookmarks", menu=bookmarks_menu)
        bookmarks_menu.add_command(label="Add Bookmark", command=self.add_bookmark, accelerator="Ctrl+B")
        bookmarks_menu.add_command(label="View Bookmarks", command=self.show_bookmarks)

        # Toolbar
        toolbar = tk.Frame(root, bg='#d4c5a9', height=50)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)

        tk.Button(
            toolbar,
            text="Open Book",
            command=self.open_file,
            font=('Arial', 10, 'bold'),
            bg='#8b7355',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(side=tk.LEFT, padx=10, pady=8)

        # Navigation (for PDFs)
        self.nav_frame = tk.Frame(toolbar, bg='#d4c5a9')
        self.nav_frame.pack(side=tk.LEFT, padx=20)

        tk.Button(
            self.nav_frame,
            text="◀",
            command=self.prev_page,
            font=('Arial', 12, 'bold'),
            bg='#a0826d',
            fg='white',
            bd=0,
            cursor='hand2',
            width=3
        ).pack(side=tk.LEFT, padx=2)

        self.page_label = tk.Label(
            self.nav_frame,
            text="Page 0 / 0",
            font=('Arial', 10),
            bg='#d4c5a9',
            fg='#333'
        )
        self.page_label.pack(side=tk.LEFT, padx=10)

        tk.Button(
            self.nav_frame,
            text="▶",
            command=self.next_page,
            font=('Arial', 12, 'bold'),
            bg='#a0826d',
            fg='white',
            bd=0,
            cursor='hand2',
            width=3
        ).pack(side=tk.LEFT, padx=2)

        # Filename
        self.filename_label = tk.Label(
            toolbar,
            text="No book open",
            font=('Arial', 11, 'italic'),
            bg='#d4c5a9',
            fg='#555'
        )
        self.filename_label.pack(side=tk.RIGHT, padx=15)

        # Main container
        main_container = tk.Frame(root, bg='#f5f5dc')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - TOC/Bookmarks
        sidebar = tk.Frame(main_container, bg='#e8e8d8', width=250, relief=tk.SOLID, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Tabs
        tabs_frame = tk.Frame(sidebar, bg='#e8e8d8')
        tabs_frame.pack(fill=tk.X)

        self.toc_btn = tk.Button(

