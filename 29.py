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

        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.word_count_label = tk.Label(
            status_bar,
            text="0 words",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor='e'
        )
        self.word_count_label.pack(side=tk.RIGHT, padx=10)

        # Sample content
        sample = """# Welcome to Markdown Editor

## Features
- **Live Preview** - See changes instantly
- *Easy formatting* - Simple syntax
- `Code snippets` - Inline code support

## Quick Guide
### Headings
Use # for headings (# to ######)

### Lists
- Item 1
- Item 2
- Item 3

### Emphasis
**Bold text**
*Italic text*
`Inline code`

### Links
[Click here](https://example.com)

> This is a blockquote
> It can span multiple lines

---

Start typing to create your document!
"""
        self.editor.insert('1.0', sample)
        self.update_preview()

    def update_preview(self, event=None):
        # Get markdown text
        md_text = self.editor.get('1.0', 'end-1c')
        
        # Convert to HTML
        html = markdown.markdown(md_text, extensions=['extra', 'nl2br'])
        
        # Simple HTML to text conversion for preview
        self.preview.config(state='normal')
        self.preview.delete('1.0', tk.END)
        
        # Basic rendering (simplified)
        lines = md_text.split('\n')
        for line in lines:
            if line.startswith('# '):
                self.preview.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.startswith('## '):
                self.preview.insert(tk.END, line[3:] + '\n', 'h2')
            elif line.startswith('### '):
                self.preview.insert(tk.END, line[4:] + '\n', 'h3')
            elif line.startswith('> '):
                self.preview.insert(tk.END, line[2:] + '\n', 'blockquote')
            elif line.startswith('---'):
                self.preview.insert(tk.END, '─' * 50 + '\n')
            elif line.startswith('- ') or line.startswith('* '):
                self.preview.insert(tk.END, '  • ' + line[2:] + '\n')
            else:
                # Handle inline formatting
                self.render_inline(line + '\n')
        
        self.preview.config(state='disabled')
        
        # Update word count
        words = len(md_text.split())
        chars = len(md_text)
        self.word_count_label.config(text=f"{words} words · {chars} chars")

    def render_inline(self, text):
        """Simple inline formatting"""
        import re
        
        # Bold
        parts = re.split(r'(\*\*[^*]+\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                self.preview.insert(tk.END, part[2:-2], 'bold')
            else:
                # Italic
                italic_parts = re.split(r'(\*[^*]+\*)', part)
                for ip in italic_parts:
                    if ip.startswith('*') and ip.endswith('*') and not ip.startswith('**'):
                        self.preview.insert(tk.END, ip[1:-1], 'italic')
                    else:
                        # Code
                        code_parts = re.split(r'(`[^`]+`)', ip)
                        for cp in code_parts:
                            if cp.startswith('`') and cp.endswith('`'):
                                self.preview.insert(tk.END, cp[1:-1], 'code')
                            else:
                                # Links
                                link_parts = re.split(r'(\[[^\]]+\]\([^)]+\))', cp)
                                for lp in link_parts:
                                    if lp.startswith('[') and '](' in lp:
                                        link_text = lp[lp.find('[')+1:lp.find(']')]
                                        self.preview.insert(tk.END, link_text, 'link')
                                    else:
                                        self.preview.insert(tk.END, lp)

    def new_file(self):
        if messagebox.askyesno("New File", "Create new file? (Unsaved changes will be lost)"):
            self.editor.delete('1.0', tk.END)
            self.current_file = None
            self.filename_label.config(text="Untitled.md")
            self.status_label.config(text="New file created")

