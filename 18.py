"""
Image Editor - Modern UI (Responsive)
Edit images: crop, rotate, filters, brightness, contrast
Requires: pip install pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        # Image state
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.photo = None
        self.filename = None
