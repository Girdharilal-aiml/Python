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
