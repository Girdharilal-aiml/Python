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


DATA_FILE = Path(__file__).with_name("questboard_data.json")
DATE_FMT = "%Y-%m-%d"
STAMP_FMT = "%Y-%m-%d %H:%M"


def now_stamp() -> str:
    return datetime.now().strftime(STAMP_FMT)


def today_str() -> str:
    return date.today().strftime(DATE_FMT)



