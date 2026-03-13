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

        self.current_file = None

        # Toolbar
        toolbar = tk.Frame(root, bg='#f5f5f5', height=50, relief=tk.FLAT, bd=1)
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)

        # File buttons
        tk.Button(
            toolbar,
            text="New",
            command=self.new_file,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            cursor='hand2',
            padx=12,
            pady=8
        ).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(
            toolbar,
            text="Open",
            command=self.open_file,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            cursor='hand2',
            padx=12,
            pady=8
        ).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(
            toolbar,
            text="Save",
            command=self.save_file,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            cursor='hand2',
            padx=12,
            pady=8
        ).pack(side=tk.LEFT, padx=5, pady=8)

        tk.Button(
            toolbar,
            text="Export HTML",
            command=self.export_html,
            bg='#9C27B0',
            fg='white',
            font=('Arial', 10, 'bold'),
            bd=0,
            cursor='hand2',
            padx=12,
            pady=8
        ).pack(side=tk.LEFT, padx=5, pady=8)

        # Filename label
        self.filename_label = tk.Label(
            toolbar,
            text="Untitled.md",
            font=('Arial', 10, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        )
        self.filename_label.pack(side=tk.RIGHT, padx=15)

        # Main container - Split view
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left - Editor
        editor_frame = tk.Frame(main_container, bg='white')
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Editor header
        editor_header = tk.Frame(editor_frame, bg='#f5f5f5', height=40)
        editor_header.pack(fill=tk.X)
        editor_header.pack_propagate(False)

        tk.Label(
            editor_header,
            text="✏️ Markdown",
            font=('Arial', 12, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # Editor text area
        editor_text_frame = tk.Frame(editor_frame, bg='white')
        editor_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        editor_scroll = tk.Scrollbar(editor_text_frame)
        editor_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.editor = tk.Text(
            editor_text_frame,
            font=('Consolas', 11),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white',
            relief=tk.FLAT,
            wrap=tk.WORD,
            yscrollcommand=editor_scroll.set,
            padx=15,
            pady=15,
            undo=True
        )
        self.editor.pack(fill=tk.BOTH, expand=True)
        editor_scroll.config(command=self.editor.yview)

        # Bind typing to update preview
        self.editor.bind('<KeyRelease>', self.update_preview)

        # Separator
        separator = tk.Frame(main_container, bg='#cccccc', width=2)
        separator.pack(side=tk.LEFT, fill=tk.Y)

        # Right - Preview
        preview_frame = tk.Frame(main_container, bg='white')
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Preview header
        preview_header = tk.Frame(preview_frame, bg='#f5f5f5', height=40)
        preview_header.pack(fill=tk.X)
        preview_header.pack_propagate(False)

        tk.Label(
            preview_header,
            text="👁️ Preview",
            font=('Arial', 12, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(side=tk.LEFT, padx=15, pady=8)

        # Preview area
        preview_text_frame = tk.Frame(preview_frame, bg='white')
        preview_text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        preview_scroll = tk.Scrollbar(preview_text_frame)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.preview = tk.Text(
            preview_text_frame,
            font=('Arial', 11),
            bg='white',
            fg='#333',
            relief=tk.FLAT,
            wrap=tk.WORD,
            yscrollcommand=preview_scroll.set,
            padx=15,
            pady=15,
            state='disabled'
        )
        self.preview.pack(fill=tk.BOTH, expand=True)
        preview_scroll.config(command=self.preview.yview)

        # Configure preview tags
        self.preview.tag_configure('h1', font=('Arial', 24, 'bold'), foreground='#1a1a1a')
        self.preview.tag_configure('h2', font=('Arial', 20, 'bold'), foreground='#1a1a1a')
        self.preview.tag_configure('h3', font=('Arial', 16, 'bold'), foreground='#1a1a1a')
        self.preview.tag_configure('bold', font=('Arial', 11, 'bold'))
        self.preview.tag_configure('italic', font=('Arial', 11, 'italic'))
        self.preview.tag_configure('code', font=('Consolas', 10), background='#f5f5f5', foreground='#d73a49')
        self.preview.tag_configure('blockquote', font=('Arial', 11, 'italic'), foreground='#666', lmargin1=20, lmargin2=20)
        self.preview.tag_configure('link', font=('Arial', 11), foreground='#2196F3', underline=True)

        # Status bar
        status_bar = tk.Frame(root, bg='#f5f5f5', height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

