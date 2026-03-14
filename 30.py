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
