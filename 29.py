"""
Markdown Editor - Simple & Perfect UI
Write markdown with live preview
Requires: pip install markdown
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
import os

class MarkdownEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Editor")
        self.root.geometry("1000x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(800, 500)

