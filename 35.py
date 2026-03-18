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

        tk.Label(panel, text="Difficulty", bg="#ece8dc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)
        ttk.Combobox(
            panel,
            textvariable=self.difficulty_var,
            values=["Easy", "Normal", "Hard", "Epic"],
            state="readonly",
        ).pack(fill=tk.X, padx=12, pady=(2, 8))

        tk.Label(panel, text="Notes", bg="#ece8dc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)
        self.notes_text = tk.Text(panel, height=6, font=("Segoe UI", 10), wrap="word")
        self.notes_text.pack(fill=tk.X, padx=12, pady=(2, 10))

        actions = tk.Frame(panel, bg="#ece8dc")
        actions.pack(fill=tk.X, padx=12, pady=(4, 10))

        tk.Button(actions, text="Add Quest", command=self.add_quest, bg="#1c7c54", fg="white", bd=0, padx=10, pady=7).pack(
            fill=tk.X, pady=3
        )
        tk.Button(
            actions, text="Update Selected", command=self.update_selected, bg="#2a5d8f", fg="white", bd=0, padx=10, pady=7
        ).pack(fill=tk.X, pady=3)
        tk.Button(
            actions, text="Mark Completed", command=self.complete_selected, bg="#b36a1f", fg="white", bd=0, padx=10, pady=7
        ).pack(fill=tk.X, pady=3)
        tk.Button(actions, text="Delete Selected", command=self.delete_selected, bg="#9b2d30", fg="white", bd=0, padx=10, pady=7).pack(
            fill=tk.X, pady=3
        )
        tk.Button(actions, text="Clear Form", command=self.clear_form, bg="#5d5d5d", fg="white", bd=0, padx=10, pady=7).pack(
            fill=tk.X, pady=3
        )

        tk.Label(
            panel,
            text="Tip: Double-click a row to load it into the form.",
            bg="#ece8dc",
            fg="#5a5a5a",
            font=("Segoe UI", 9, "italic"),
            wraplength=260,
            justify="left",
        ).pack(anchor="w", padx=12, pady=(4, 12))

    def build_table_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        filter_bar = tk.Frame(panel, bg="#f2f2f2", height=56)
        filter_bar.grid(row=0, column=0, sticky="ew")
        filter_bar.grid_columnconfigure(1, weight=1)

        tk.Label(filter_bar, text="Search", bg="#f2f2f2", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=(8, 4), pady=10)
        tk.Entry(filter_bar, textvariable=self.search_var, width=18).grid(row=0, column=1, padx=4, pady=10, sticky="ew")

        ttk.Combobox(
            filter_bar,
            textvariable=self.filter_status_var,
            values=["All", "Open", "In Progress", "Done"],
            state="readonly",
            width=12,
        ).grid(row=0, column=2, padx=4, pady=10)

        ttk.Combobox(
            filter_bar,
            textvariable=self.filter_category_var,
            values=["All", "Study", "Work", "Health", "Code", "Creative", "Life"],
            state="readonly",
            width=12,
        ).grid(row=0, column=3, padx=4, pady=10)

        tk.Button(filter_bar, text="Apply", command=self.refresh_table, bg="#1f3b4d", fg="white", bd=0, padx=10).grid(
            row=0, column=4, padx=4, pady=10
        )
        tk.Button(filter_bar, text="Reset", command=self.reset_filters, bg="#4a4a4a", fg="white", bd=0, padx=10).grid(
            row=0, column=5, padx=(4, 8), pady=10
        )

        table_frame = tk.Frame(panel, bg="white")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        yscroll = ttk.Scrollbar(table_frame, orient="vertical")
        yscroll.grid(row=0, column=1, sticky="ns")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "title", "cat", "diff", "status", "xp", "created", "completed"),
            show="headings",
            yscrollcommand=yscroll.set,
            selectmode="browse",
        )
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.config(command=self.tree.yview)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("cat", text="Category")
        self.tree.heading("diff", text="Difficulty")
        self.tree.heading("status", text="Status")
        self.tree.heading("xp", text="XP")
        self.tree.heading("created", text="Created")
        self.tree.heading("completed", text="Completed")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("title", width=210, anchor="w")
        self.tree.column("cat", width=95, anchor="center")
        self.tree.column("diff", width=90, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("xp", width=60, anchor="center")
        self.tree.column("created", width=130, anchor="center")
        self.tree.column("completed", width=130, anchor="center")

        self.tree.bind("<Double-1>", self.load_selected_into_form)

    def build_timer_panel(self, parent: tk.Widget) -> None:
        panel = tk.Frame(parent, bg="#ece8dc", bd=1, relief=tk.SOLID)
        panel.grid(row=0, column=2, sticky="nsew", padx=(12, 0))

        tk.Label(panel, text="Focus Timer", bg="#ece8dc", fg="#1f3b4d", font=("Georgia", 14, "bold")).pack(
            anchor="w", padx=12, pady=(12, 8)
        )

