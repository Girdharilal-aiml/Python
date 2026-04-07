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
