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

        # Adjustments
        adjust_frame = tk.LabelFrame(
            self.sidebar,
            text="Adjust",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#c9d1d9',
            bd=0
        )
        adjust_frame.pack(fill=tk.X, padx=10, pady=5)

        # Brightness
        tk.Label(
            adjust_frame,
            text="☀️ Brightness",
            font=('Arial', 9),
            bg='#161b22',
            fg='#8b949e'
        ).pack(anchor='w', padx=10, pady=(5, 0))

        self.brightness_scale = tk.Scale(
            adjust_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.adjust_brightness,
            bg='#161b22',
            fg='#c9d1d9',
            troughcolor='#0d1117',
            highlightthickness=0
        )
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Contrast
        tk.Label(
            adjust_frame,
            text="🎚️ Contrast",
            font=('Arial', 9),
            bg='#161b22',
            fg='#8b949e'
        ).pack(anchor='w', padx=10, pady=(5, 0))

        self.contrast_scale = tk.Scale(
            adjust_frame,
            from_=0.5,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            command=self.adjust_contrast,
            bg='#161b22',
            fg='#c9d1d9',
            troughcolor='#0d1117',
            highlightthickness=0
        )
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Undo/Reset
        action_frame = tk.Frame(self.sidebar, bg='#161b22')
        action_frame.pack(fill=tk.X, padx=10, pady=20)

        tk.Button(
            action_frame,
            text="↶ Undo",
            command=self.undo,
            bg='#d29922',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            bd=0,
            activebackground='#e5a323'
        ).pack(fill=tk.X, pady=3)

        tk.Button(
            action_frame,
            text="⟲ Reset",
            command=self.reset_image,
            bg='#da3633',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2',
            bd=0,
            activebackground='#e5534b'
        ).pack(fill=tk.X, pady=3)

        # Right side - Canvas
        canvas_container = tk.Frame(main_frame, bg='#0d1117')
        canvas_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        # Info label
        self.info_label = tk.Label(
            canvas_container,
            text="Open an image to start editing",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e',
            pady=10
        )
        self.info_label.pack(fill=tk.X)

        # Canvas for image
        self.canvas = tk.Canvas(
            canvas_container,
            bg='#161b22',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind resize
        self.root.bind('<Configure>', self.on_resize)

    def open_image(self):
        filepath = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )

        if filepath:
            try:
                self.filename = filepath
                self.original_image = Image.open(filepath)
                self.current_image = self.original_image.copy()
                self.history = []
                
                # Reset sliders
                self.brightness_scale.set(1.0)
                self.contrast_scale.set(1.0)
                
                self.update_canvas()
                
                # Update info
                width, height = self.original_image.size
                size_kb = os.path.getsize(filepath) / 1024
                self.info_label.config(
                    text=f"📷 {os.path.basename(filepath)} | {width}x{height} | {size_kb:.1f} KB"
                )
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image:\n{str(e)}")

    def save_image(self):
        if not self.current_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )

        if filepath:
            try:
                self.current_image.save(filepath)
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")

    def save_to_history(self):
        if self.current_image:
            self.history.append(self.current_image.copy())
            if len(self.history) > self.max_history:
                self.history.pop(0)

    def undo(self):
        if self.history:
            self.current_image = self.history.pop()
            self.brightness_scale.set(1.0)
            self.contrast_scale.set(1.0)
            self.update_canvas()
        else:
            messagebox.showinfo("Undo", "No more actions to undo!")

    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.history = []
            self.brightness_scale.set(1.0)
            self.contrast_scale.set(1.0)
            self.update_canvas()

    def rotate_image(self, angle):
        if not self.current_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            return
        
        self.save_to_history()
        self.current_image = self.current_image.rotate(angle, expand=True)
        self.update_canvas()

    def flip_vertical(self):
        if not self.current_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            return
        
        self.save_to_history()
        self.current_image = ImageOps.flip(self.current_image)
        self.update_canvas()
