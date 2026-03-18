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


def xp_for_difficulty(difficulty: str) -> int:
    table = {
        "Easy": 20,
        "Normal": 40,
        "Hard": 70,
        "Epic": 110,
    }
    return table.get(difficulty, 40)


def next_level_cost(level: int) -> int:
    return 120 + (level - 1) * 80


def level_from_xp(total_xp: int) -> tuple[int, int, int]:
    level = 1
    spent = 0
    while True:
        cost = next_level_cost(level)
        if total_xp < spent + cost:
            in_level = total_xp - spent
            return level, in_level, cost
        spent += cost
        level += 1


def compute_streak(completion_dates: list[str]) -> int:
    if not completion_dates:
        return 0

    unique_days = sorted(set(completion_dates))
    today = date.today()
    cursor = today
    streak = 0


