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
        
        # History for undo
        self.history = []
        self.max_history = 10

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=24, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - Tools (with scrollbar)
        sidebar_container = tk.Frame(main_frame, bg='#0d1117')
        sidebar_container.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)

        # Canvas for scrolling
        sidebar_canvas = tk.Canvas(sidebar_container, bg='#161b22', width=250, highlightthickness=0)
        scrollbar = tk.Scrollbar(sidebar_container, orient='vertical', command=sidebar_canvas.yview)
        
        self.sidebar = tk.Frame(sidebar_canvas, bg='#161b22')
        
        self.sidebar.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=self.sidebar, anchor='nw')
        sidebar_canvas.configure(yscrollcommand=scrollbar.set)
        
        sidebar_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        sidebar_canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Sidebar title
        tk.Label(
            self.sidebar,
            text="🎨 Image Editor",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(pady=20)

        # File operations
        file_frame = tk.LabelFrame(
            self.sidebar,
            text="File",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#c9d1d9',
            bd=0
        )
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            file_frame,
            text="📁 Open Image",
            command=self.open_image,
            bg='#238636',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#2ea043'
        ).pack(fill=tk.X, padx=8, pady=3)

        tk.Button(
            file_frame,
            text="💾 Save Image",
            command=self.save_image,
            bg='#1f6feb',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#388bfd'
        ).pack(fill=tk.X, padx=8, pady=3)

        # Basic operations
        basic_frame = tk.LabelFrame(
            self.sidebar,
            text="Basic",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#c9d1d9',
            bd=0
        )
        basic_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            basic_frame,
            text="↻ Rotate Left",
            command=lambda: self.rotate_image(-90),
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            basic_frame,
            text="↺ Rotate Right",
            command=lambda: self.rotate_image(90),
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            basic_frame,
            text="↕️ Flip Vertical",
            command=self.flip_vertical,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            basic_frame,
            text="↔️ Flip Horizontal",
            command=self.flip_horizontal,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        # Filters
        filter_frame = tk.LabelFrame(
            self.sidebar,
            text="Filters",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#c9d1d9',
            bd=0
        )
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(
            filter_frame,
            text="🌫️ Blur",
            command=self.apply_blur,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            filter_frame,
            text="✨ Sharpen",
            command=self.apply_sharpen,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            filter_frame,
            text="⚫ Grayscale",
            command=self.apply_grayscale,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)

        tk.Button(
            filter_frame,
            text="🎭 Contour",
            command=self.apply_contour,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 10),
            cursor='hand2',
            bd=0,
            activebackground='#30363d'
        ).pack(fill=tk.X, padx=10, pady=3)
