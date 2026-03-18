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

        self.profile_label = tk.Label(
            header,
            text="",
            bg="#1f3b4d",
            fg="#e8edf0",
            font=("Consolas", 11, "bold"),
        )
        self.profile_label.pack(side=tk.RIGHT, padx=18)

        body = tk.Frame(self.root, bg="#f3f1eb")
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, weight=0)
        body.grid_rowconfigure(0, weight=1)

        self.build_form_panel(body)
        self.build_table_panel(body)
        self.build_timer_panel(body)

        footer = tk.Frame(self.root, bg="#d8d4c7", height=30)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)

        self.status_label = tk.Label(
            footer,
            text="Ready",
            bg="#d8d4c7",
            fg="#2d2d2d",
            anchor="w",
            font=("Segoe UI", 9),
        )
        self.status_label.pack(fill=tk.X, padx=10)

    def build_form_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg="#ece8dc", bd=1, relief=tk.SOLID)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        tk.Label(panel, text="Create / Edit Quest", bg="#ece8dc", fg="#1f3b4d", font=("Georgia", 14, "bold")).pack(
            anchor="w", padx=12, pady=(12, 8)
        )

        tk.Label(panel, text="Title", bg="#ece8dc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)
        tk.Entry(panel, textvariable=self.title_var, width=30, font=("Segoe UI", 10)).pack(fill=tk.X, padx=12, pady=(2, 8))

        tk.Label(panel, text="Category", bg="#ece8dc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)
        ttk.Combobox(
            panel,
            textvariable=self.category_var,
            values=["Study", "Work", "Health", "Code", "Creative", "Life"],
            state="readonly",
        ).pack(fill=tk.X, padx=12, pady=(2, 8))

