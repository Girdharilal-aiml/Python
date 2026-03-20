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
