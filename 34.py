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

