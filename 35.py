"""
QuestBoard Studio
-----------------
A medium-sized, unique Tkinter project:
- Manage tasks as "quests"
- Earn XP and level up when completing quests
- Track daily completion streaks
- Filter/search quests
- Built-in focus timer (work/break)

Run:
    python 35.py
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk
