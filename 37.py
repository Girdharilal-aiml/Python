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

