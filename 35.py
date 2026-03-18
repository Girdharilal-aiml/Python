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

    days_set = {datetime.strptime(d, DATE_FMT).date() for d in unique_days}

    if cursor not in days_set:
        cursor = cursor - timedelta(days=1)
        if cursor not in days_set:
            return 0

    while cursor in days_set:
        streak += 1
        cursor = cursor - timedelta(days=1)

    return streak


@dataclass
class Quest:
    quest_id: int
    title: str
    category: str
    difficulty: str
    notes: str
    status: str
    xp: int
    created_at: str
    completed_at: str


class QuestBoardApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("QuestBoard Studio")
        self.root.geometry("1240x760")
        self.root.minsize(1000, 640)
        self.root.configure(bg="#f3f1eb")

        self.quests: list[Quest] = []
        self.next_id = 1
        self.total_xp = 0
        self.completion_days: list[str] = []

        self.timer_running = False
        self.timer_remaining = 25 * 60
        self.timer_mode = "Work"
        self.timer_job: str | None = None

        self.title_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Study")
        self.difficulty_var = tk.StringVar(value="Normal")
        self.status_var = tk.StringVar(value="Open")
        self.search_var = tk.StringVar()
        self.filter_status_var = tk.StringVar(value="All")
        self.filter_category_var = tk.StringVar(value="All")
        self.work_var = tk.IntVar(value=25)
        self.break_var = tk.IntVar(value=5)

        self.build_ui()
        self.load_state()
        self.refresh_all()

    def build_ui(self) -> None:
        header = tk.Frame(self.root, bg="#1f3b4d", height=76)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="QuestBoard Studio",
            bg="#1f3b4d",
            fg="#f7d78b",
            font=("Georgia", 22, "bold"),
        ).pack(side=tk.LEFT, padx=18)


