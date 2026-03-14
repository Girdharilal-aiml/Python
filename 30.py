"""
Calendar/Planner - Simple & Perfect UI
Monthly calendar with event management
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
import json
import os
from datetime import datetime, timedelta

class CalendarPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Planner")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

        # Data
        self.events_file = "calendar_events.json"
        self.events = {}  # Format: {"YYYY-MM-DD": ["event1", "event2"]}
        self.load_events()

        # Current date
        self.today = datetime.now()
        self.current_month = self.today.month
        self.current_year = self.today.year
        self.selected_date = None

        # Header
        header = tk.Frame(root, bg='#2196F3', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🗓️ Calendar Planner",
            font=('Arial', 24, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=20)

        # Navigation
        nav_frame = tk.Frame(root, bg='#f5f5f5', height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        tk.Button(
            nav_frame,
            text="◀",
            command=self.prev_month,
            font=('Arial', 16, 'bold'),
            bg='#e0e0e0',
            fg='#333',
            bd=0,
            cursor='hand2',
            width=3
        ).pack(side=tk.LEFT, padx=20, pady=15)

        self.month_label = tk.Label(
            nav_frame,
            text="",
            font=('Arial', 18, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        )
        self.month_label.pack(side=tk.LEFT, expand=True)

        tk.Button(
            nav_frame,
            text="▶",
            command=self.next_month,
            font=('Arial', 16, 'bold'),
            bg='#e0e0e0',
            fg='#333',
            bd=0,
            cursor='hand2',
            width=3
        ).pack(side=tk.RIGHT, padx=20, pady=15)

        tk.Button(
            nav_frame,
            text="Today",
            command=self.go_to_today,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=15,
            pady=5
        ).pack(side=tk.RIGHT, padx=10)

        # Main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Calendar grid
        self.calendar_frame = tk.Frame(main_container, bg='white')
        self.calendar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Event sidebar
        sidebar = tk.Frame(main_container, bg='#f5f5f5', width=250, relief=tk.SOLID, bd=1)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        sidebar.pack_propagate(False)

        # Sidebar header
        tk.Label(
            sidebar,
            text="Events",
            font=('Arial', 16, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=15)

        self.selected_date_label = tk.Label(
            sidebar,
            text="Select a date",
            font=('Arial', 11),
            bg='#f5f5f5',
            fg='#666'
        )
        self.selected_date_label.pack(pady=5)

        tk.Button(
            sidebar,
            text="+ Add Event",
            command=self.add_event,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=15,
            pady=8
        ).pack(pady=10)

