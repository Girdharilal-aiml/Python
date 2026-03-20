"""
NovaPad - Upgraded Tkinter Code Editor

Features:
- Multi-tab editor
- Syntax highlighting (regex-based)
- Line numbers and status bar
- Find/replace in active tab
- Light/Dark theme toggle
- Recent files list (persisted to JSON)
- Autosave (for already saved files)
- Run current Python file and show output panel
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


APP_STATE = Path(__file__).with_name("novapad_state.json")


class DocumentTab:
    def __init__(self, parent: ttk.Notebook, app: "CodeEditorApp", title: str = "Untitled") -> None:
        self.app = app
        self.file_path: Path | None = None
        self.modified = False

        self.frame = tk.Frame(parent, bg=self.app.theme["editor_bg"])
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.line_numbers = tk.Text(
            self.frame,
            width=5,
            padx=6,
            pady=8,
            bd=0,
            state="disabled",
            wrap="none",
            cursor="arrow",
            font=("Consolas", 11),
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")

        editor_container = tk.Frame(self.frame, bg=self.app.theme["editor_bg"])
        editor_container.grid(row=0, column=1, sticky="nsew")
        editor_container.grid_rowconfigure(0, weight=1)
        editor_container.grid_columnconfigure(0, weight=1)

        self.v_scroll = tk.Scrollbar(editor_container, orient="vertical")
        self.v_scroll.grid(row=0, column=1, sticky="ns")

        self.h_scroll = tk.Scrollbar(editor_container, orient="horizontal")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.text = tk.Text(
            editor_container,
            wrap="none",
            undo=True,
            font=("Consolas", 11),
            insertwidth=2,
            padx=10,
            pady=10,
            yscrollcommand=self._on_text_yscroll,
            xscrollcommand=self.h_scroll.set,
        )
        self.text.grid(row=0, column=0, sticky="nsew")

        self.v_scroll.config(command=self._on_vertical_scroll)
        self.h_scroll.config(command=self.text.xview)

        self.text.tag_configure("keyword", foreground="#569cd6")
        self.text.tag_configure("string", foreground="#ce9178")
        self.text.tag_configure("comment", foreground="#6a9955")
        self.text.tag_configure("number", foreground="#b5cea8")
        self.text.tag_configure("found", background="#ffb347", foreground="#111111")

        self.text.bind("<KeyRelease>", self._on_key_release)
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<ButtonRelease-1>", lambda _e: self.app.update_status_bar())

        self.highlight_job: str | None = None
        self.set_tab_title(title)
        self.apply_theme()
        self.update_line_numbers()

    def apply_theme(self) -> None:
        th = self.app.theme
        self.frame.configure(bg=th["editor_bg"])
        self.line_numbers.configure(bg=th["line_bg"], fg=th["line_fg"], insertbackground=th["line_fg"])
        self.text.configure(
            bg=th["editor_bg"],
            fg=th["editor_fg"],
            insertbackground=th["cursor"],
            selectbackground=th["select_bg"],
            selectforeground=th["select_fg"],
        )

    def _on_text_yscroll(self, first: str, last: str) -> None:
        self.v_scroll.set(first, last)
        self.line_numbers.yview_moveto(first)

    def _on_vertical_scroll(self, *args: str) -> None:
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def _on_key_release(self, _event: tk.Event) -> None:
        self.update_line_numbers()
        self.app.update_status_bar()
        if self.highlight_job:
            self.app.root.after_cancel(self.highlight_job)
        self.highlight_job = self.app.root.after(80, self.highlight_syntax)

    def _on_modified(self, _event: tk.Event) -> None:
        if self.text.edit_modified():
            self.modified = True
            self.update_tab_visual()
            self.text.edit_modified(False)

    def set_tab_title(self, title: str) -> None:
        self.base_title = title

    def update_tab_visual(self) -> None:
        title = self.display_name
        if self.modified:
            title += " *"
        self.app.notebook.tab(self.frame, text=title)

    @property
    def display_name(self) -> str:
        return self.file_path.name if self.file_path else self.base_title

    def update_line_numbers(self) -> None:
        line_count = self.text.get("1.0", "end-1c").count("\n") + 1
        nums = "\n".join(str(i) for i in range(1, line_count + 1))
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", nums)
        self.line_numbers.configure(state="disabled")

    def highlight_syntax(self) -> None:
        for tag in ("keyword", "string", "comment", "number"):
            self.text.tag_remove(tag, "1.0", tk.END)

        content = self.text.get("1.0", "end-1c")
        for kw in self.app.keywords:
            for match in re.finditer(r"\\b" + re.escape(kw) + r"\\b", content):
                self.text.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(r'(["\'])(?:(?=(\\?))\\2.)*?\\1', content):
            self.text.tag_add("string", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(r"#.*?$|//.*?$", content, re.MULTILINE):
            self.text.tag_add("comment", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

        for match in re.finditer(r"\\b\\d+\\.?\\d*\\b", content):
            self.text.tag_add("number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    def load_content(self, text: str) -> None:
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", text)
        self.modified = False
        self.update_line_numbers()
        self.highlight_syntax()
        self.update_tab_visual()

    def get_content(self) -> str:
        return self.text.get("1.0", "end-1c")


class CodeEditorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("NovaPad")
        self.root.geometry("1180x760")
        self.root.minsize(920, 620)

        self.keywords = [
            "def", "class", "import", "from", "if", "elif", "else", "for", "while",
            "return", "try", "except", "with", "as", "pass", "break", "continue",
            "True", "False", "None", "and", "or", "not", "in", "is", "lambda",
            "function", "var", "let", "const", "async", "await", "new", "this",
        ]

        self.themes = {
            "dark": {
                "window_bg": "#1e1e1e",
                "toolbar_bg": "#2d2d2d",
                "toolbar_fg": "#e6e6e6",
                "editor_bg": "#1e1e1e",
                "editor_fg": "#d4d4d4",
                "line_bg": "#2d2d2d",
                "line_fg": "#8b949e",
                "cursor": "#ffffff",
                "select_bg": "#264f78",
                "select_fg": "#ffffff",
                "status_bg": "#2d2d2d",
                "status_fg": "#8b949e",
                "output_bg": "#101010",
                "output_fg": "#d0d0d0",
            },
            "light": {
                "window_bg": "#f4f4f4",
                "toolbar_bg": "#e4e4e4",
                "toolbar_fg": "#202020",
                "editor_bg": "#ffffff",
                "editor_fg": "#1a1a1a",
                "line_bg": "#ececec",
                "line_fg": "#666666",
                "cursor": "#111111",
                "select_bg": "#cfe8ff",
                "select_fg": "#111111",
                "status_bg": "#e4e4e4",
                "status_fg": "#353535",
                "output_bg": "#f8f8f8",
                "output_fg": "#222222",
            },
        }

        self.theme_name = "dark"
        self.theme = self.themes[self.theme_name]

        self.autosave_enabled = tk.BooleanVar(value=True)
        self.autosave_seconds = tk.IntVar(value=20)
        self.recent_files: list[str] = []
        self.tabs: list[DocumentTab] = []

        self._build_ui()
        self._load_state()
        self.apply_theme()
        self.new_tab()
        self.schedule_autosave()

    def _build_ui(self) -> None:
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Tab", command=self.new_tab, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_as)
        self.file_menu.add_separator()
        self.recent_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Recent Files", menu=self.recent_menu)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close Tab", command=self.close_current_tab, accelerator="Ctrl+W")
        self.file_menu.add_command(label="Exit", command=self.on_exit)

        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Find", command=self.show_find, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.show_replace, accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")

        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

        run_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run Current Python File", command=self.run_current_file, accelerator="F5")

        settings_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_checkbutton(label="Enable Autosave", variable=self.autosave_enabled)
        settings_menu.add_command(label="Set Autosave Seconds", command=self.set_autosave_interval)

        self.toolbar = tk.Frame(self.root, height=42)
        self.toolbar.pack(fill=tk.X)
        self.toolbar.pack_propagate(False)

        tk.Button(self.toolbar, text="New", command=self.new_tab, padx=10, pady=5, bd=0).pack(side=tk.LEFT, padx=4, pady=6)
        tk.Button(self.toolbar, text="Open", command=self.open_file, padx=10, pady=5, bd=0).pack(side=tk.LEFT, padx=4, pady=6)
        tk.Button(self.toolbar, text="Save", command=self.save_file, padx=10, pady=5, bd=0).pack(side=tk.LEFT, padx=4, pady=6)
        tk.Button(self.toolbar, text="Run", command=self.run_current_file, padx=10, pady=5, bd=0).pack(side=tk.LEFT, padx=4, pady=6)

        self.autosave_label = tk.Label(self.toolbar, text="Autosave: ON")
        self.autosave_label.pack(side=tk.RIGHT, padx=12)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda _e: self.update_status_bar())

        self.output_frame = tk.Frame(self.root, height=160)
        self.output_frame.pack(fill=tk.X)
        self.output_frame.pack_propagate(False)

        out_header = tk.Frame(self.output_frame, height=24)
        out_header.pack(fill=tk.X)
        out_header.pack_propagate(False)
        tk.Label(out_header, text="Output", anchor="w").pack(side=tk.LEFT, padx=8)
        tk.Button(out_header, text="Clear", command=lambda: self.output_text.delete("1.0", tk.END), bd=0, padx=8).pack(
            side=tk.RIGHT, padx=8, pady=2
        )

        self.output_text = tk.Text(self.output_frame, height=8, wrap="word", state="disabled", font=("Consolas", 10), bd=1)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(0, 6))

        self.status_bar = tk.Frame(self.root, height=26)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar.pack_propagate(False)

        self.status_label = tk.Label(self.status_bar, text="Line 1, Col 1", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.file_label = tk.Label(self.status_bar, text="Untitled", anchor="e")
        self.file_label.pack(side=tk.RIGHT, padx=10)

        self.root.bind("<Control-n>", lambda _e: self.new_tab())
        self.root.bind("<Control-o>", lambda _e: self.open_file())
        self.root.bind("<Control-s>", lambda _e: self.save_file())
        self.root.bind("<Control-w>", lambda _e: self.close_current_tab())
        self.root.bind("<Control-f>", lambda _e: self.show_find())
        self.root.bind("<Control-h>", lambda _e: self.show_replace())
        self.root.bind("<Control-a>", lambda _e: self.select_all())
        self.root.bind("<F5>", lambda _e: self.run_current_file())

    def _load_state(self) -> None:
        if not APP_STATE.exists():
            return
