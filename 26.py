"""
Drawing/Paint App - Simple & Perfect UI
Draw with different tools and colors
"""

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(700, 500)

        # Drawing state
        self.old_x = None
        self.old_y = None
        self.color = '#000000'
        self.bg_color = '#FFFFFF'
        self.brush_size = 3
        self.tool = 'pen'  # pen, eraser, line, rectangle, circle
        
        # For PIL image saving
        self.image = None
        self.draw = None

        # Top toolbar
        toolbar = tk.Frame(root, bg='#f5f5f5', height=60, relief=tk.FLAT, bd=1)
        toolbar.pack(fill=tk.X, side=tk.TOP)
        toolbar.pack_propagate(False)

        # File buttons
        file_frame = tk.Frame(toolbar, bg='#f5f5f5')
        file_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Button(
            file_frame,
            text="New",
            command=self.new_canvas,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            file_frame,
            text="Save",
            command=self.save_drawing,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=2)

        tk.Button(
            file_frame,
            text="Clear",
            command=self.clear_canvas,
            bg='#f44336',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=2)

        # Tools
        tools_frame = tk.Frame(toolbar, bg='#f5f5f5')
        tools_frame.pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            tools_frame,
            text="Tool:",
            font=('Arial', 10, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=5)

        self.tool_buttons = {}
        tools = [
            ('Pen', 'pen', '✏️'),
            ('Eraser', 'eraser', '🧹'),
            ('Line', 'line', '📏'),
            ('Rectangle', 'rectangle', '▭'),
            ('Circle', 'circle', '⭕')
        ]

        for name, tool_id, icon in tools:
            btn = tk.Button(
                tools_frame,
                text=icon,
                command=lambda t=tool_id: self.select_tool(t),
                bg='#2196F3' if tool_id == 'pen' else '#e0e0e0',
                fg='white' if tool_id == 'pen' else '#333',
                font=('Arial', 14),
                width=2,
                bd=0,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.tool_buttons[tool_id] = btn

        # Main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - Colors & Size
        sidebar = tk.Frame(main_container, bg='#f5f5f5', width=150, relief=tk.FLAT, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Color picker
        tk.Label(
            sidebar,
            text="Color:",
            font=('Arial', 11, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=(15, 5))

        self.color_display = tk.Canvas(
            sidebar,
            width=80,
            height=80,
            bg=self.color,
            highlightthickness=2,
            highlightbackground='#333'
        )
        self.color_display.pack(pady=5)

        tk.Button(
            sidebar,
            text="Choose Color",
            command=self.choose_color,
            bg='#2196F3',
            fg='white',
            font=('Arial', 9, 'bold'),
            bd=0,
            cursor='hand2',
            padx=10,
            pady=5
        ).pack(pady=5)

        # Quick colors
        tk.Label(
            sidebar,
            text="Quick Colors:",
            font=('Arial', 9, 'bold'),
            bg='#f5f5f5',
            fg='#666'
        ).pack(pady=(15, 5))

        quick_colors = [
            '#000000', '#FFFFFF', '#f44336', '#E91E63',
            '#9C27B0', '#673AB7', '#3F51B5', '#2196F3',
            '#03A9F4', '#00BCD4', '#009688', '#4CAF50',
            '#8BC34A', '#CDDC39', '#FFEB3B', '#FFC107',
            '#FF9800', '#FF5722', '#795548', '#9E9E9E'
        ]

