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
