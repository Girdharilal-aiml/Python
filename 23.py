"""
Pomodoro Timer - Simple & Perfect UI
Focus timer with work/break cycles
"""

import tkinter as tk
from tkinter import messagebox
import time
import winsound

class PomodoroTimer:
    def play_faah_sound(self):
        # 🔊 THIS PLAYS YOUR FAAH SOUND
        winsound.PlaySound("23_faaah.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x650")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(400, 550)

        # Timer settings (in seconds)
        self.work_time = 25 * 60  # 25 minutes
        self.short_break = 5 * 60  # 5 minutes
        self.long_break = 15 * 60  # 15 minutes
        
        # State
        self.time_left = self.work_time
        self.is_running = False
        self.is_work = True
        self.work_sessions = 0
        self.timer_id = None

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="⏰ Pomodoro Timer",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=20)

        # Session counter
        session_frame = tk.Frame(root, bg='white')
        session_frame.pack(pady=20)

        tk.Label(
            session_frame,
            text="Work Sessions:",
            font=('Arial', 12),
            bg='white',
            fg='#666'
        ).pack(side=tk.LEFT, padx=5)

        self.session_label = tk.Label(
            session_frame,
            text="0",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#4CAF50'
        )
        self.session_label.pack(side=tk.LEFT, padx=5)

        # Status
        self.status_label = tk.Label(
            root,
            text="WORK TIME",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#f44336'
        )
        self.status_label.pack(pady=10)

        # Timer display
        timer_frame = tk.Frame(root, bg='#f5f5f5', relief=tk.SOLID, bd=2)
        timer_frame.pack(pady=30, padx=40, fill=tk.X)

        self.time_label = tk.Label(
            timer_frame,
            text="25:00",
            font=('Courier', 72, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        )
        self.time_label.pack(pady=20)

        # Progress bar
        progress_frame = tk.Frame(root, bg='white')
        progress_frame.pack(fill=tk.X, padx=40, pady=20)

        self.progress_canvas = tk.Canvas(
            progress_frame,
            height=20,
            bg='#e0e0e0',
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.X)

        self.progress_bar = self.progress_canvas.create_rectangle(
            0, 0, 0, 20,
            fill='#4CAF50',
            outline=''
        )

        # Control buttons
        btn_frame = tk.Frame(root, bg='white')
        btn_frame.pack(pady=0)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ START",
            command=self.start_timer,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            width=12,
            height=2,
            bd=0,
            cursor='hand2',
            activebackground='#45a049'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=10)

        self.reset_btn = tk.Button(
            btn_frame,
            text="⟲ RESET",
            command=self.reset_timer,
            font=('Arial', 14, 'bold'),
            bg='#f44336',
            fg='white',
            width=12,
            height=2,
            bd=0,
            cursor='hand2',
            activebackground='#da190b'
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Settings
        settings_frame = tk.LabelFrame(
            root,
            text="Settings (minutes)",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333',
            relief=tk.SOLID,
            bd=1
        )
        settings_frame.pack(fill=tk.X, padx=40, pady=0)

        # Work time
        work_frame = tk.Frame(settings_frame, bg='white')
        work_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            work_frame,
            text="Work:",
            font=('Arial', 10),
            bg='white',
            fg='#666',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.work_spinbox = tk.Spinbox(
            work_frame,
            from_=1,
            to=60,
            font=('Arial', 10),
            width=10,
            command=self.update_work_time
        )
        self.work_spinbox.delete(0, tk.END)
        self.work_spinbox.insert(0, "25")
        self.work_spinbox.pack(side=tk.LEFT, padx=5)

        # Short break
        short_frame = tk.Frame(settings_frame, bg='white')
        short_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            short_frame,
            text="Short Break:",
            font=('Arial', 10),
            bg='white',
            fg='#666',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.short_spinbox = tk.Spinbox(
            short_frame,
            from_=1,
            to=30,
            font=('Arial', 10),
            width=10,
            command=self.update_short_break
        )
        self.short_spinbox.delete(0, tk.END)
        self.short_spinbox.insert(0, "5")
        self.short_spinbox.pack(side=tk.LEFT, padx=5)

        # Long break
        long_frame = tk.Frame(settings_frame, bg='white')
        long_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            long_frame,
            text="Long Break:",
            font=('Arial', 10),
            bg='white',
            fg='#666',
            width=12,
            anchor='w'
        ).pack(side=tk.LEFT)

        self.long_spinbox = tk.Spinbox(
            long_frame,
            from_=1,
            to=60,
            font=('Arial', 10),
            width=10,
            command=self.update_long_break
        )
        self.long_spinbox.delete(0, tk.END)
        self.long_spinbox.insert(0, "15")
        self.long_spinbox.pack(side=tk.LEFT, padx=5)

    def update_work_time(self):
        if not self.is_running:
            self.work_time = int(self.work_spinbox.get()) * 60
            if self.is_work:
                self.time_left = self.work_time
                self.update_display()

    def update_short_break(self):
        self.short_break = int(self.short_spinbox.get()) * 60

    def update_long_break(self):
        self.long_break = int(self.long_spinbox.get()) * 60

    def start_timer(self):
        if self.is_running:
            # Pause
            self.is_running = False
            self.start_btn.config(text="▶ START", bg='#4CAF50')
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        else:
