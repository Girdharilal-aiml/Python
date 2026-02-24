"""
Stopwatch with Lap Timer - Modern UI
Beautiful redesign with better visuals
"""

import tkinter as tk
from tkinter import font as tkfont
import time

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Stopwatch")
        self.root.geometry("500x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)

        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.laps = []

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.time_font = tkfont.Font(family='Courier New', size=56, weight='bold')
        self.btn_font = tkfont.Font(family='Arial', size=13, weight='bold')

        # Main container with gradient effect
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title with modern styling
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="⏱",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Stopwatch",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Time display with modern card design
        time_card = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT, bd=0)
        time_card.pack(pady=10, fill=tk.X)

        self.time_label = tk.Label(
            time_card,
            text="00:00:00.00",
            font=self.time_font,
            bg='#161b22',
            fg='#58a6ff',
            pady=30
        )
        self.time_label.pack()

        # Milliseconds label
        millisec_label = tk.Label(
            time_card,
            text="HH : MM : SS . CS",
            font=('Arial', 10),
            bg='#161b22',
            fg='#8b949e'
        )
        millisec_label.pack(pady=(0, 20))

        # Control buttons with modern design
        btn_frame = tk.Frame(main_frame, bg='#0d1117')
        btn_frame.pack(pady=25)

        # Start button
        self.start_btn = tk.Button(
            btn_frame,
            text="Start",
            command=self.start,
            bg='#238636',
            fg='white',
            font=self.btn_font,
            width=12,
            height=2,
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#2ea043',
            activeforeground='white'
        )
        self.start_btn.grid(row=0, column=0, padx=8)

        # Lap button
        self.lap_btn = tk.Button(
            btn_frame,
            text="Lap",
            command=self.record_lap,
            bg='#1f6feb',
            fg='white',
            font=self.btn_font,
            width=12,
            height=2,
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            state='disabled',
            activebackground='#388bfd',
            activeforeground='white'
        )
        self.lap_btn.grid(row=0, column=1, padx=8)

        # Reset button
        self.reset_btn = tk.Button(
            btn_frame,
            text="Reset",
            command=self.reset,
            bg='#21262d',
            fg='#c9d1d9',
            font=self.btn_font,
            width=12,
            height=2,
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            activebackground='#30363d',
            activeforeground='white'
        )
        self.reset_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Laps section with modern card design
        laps_card = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        laps_card.pack(pady=10, fill=tk.BOTH, expand=True)

        # Laps header
        header_frame = tk.Frame(laps_card, bg='#161b22')
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))

        tk.Label(
            header_frame,
            text="🏁 Lap Times",
            font=('Arial', 14, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT)

        self.lap_count_label = tk.Label(
            header_frame,
            text="0 laps",
            font=('Arial', 10),
            bg='#161b22',
            fg='#8b949e'
        )
        self.lap_count_label.pack(side=tk.RIGHT)

        # Laps container with scrollbar
        laps_container = tk.Frame(laps_card, bg='#161b22')
        laps_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))

        # Canvas for scrolling
        canvas = tk.Canvas(laps_container, bg='#161b22', highlightthickness=0, height=200)
        scrollbar = tk.Scrollbar(laps_container, orient='vertical', command=canvas.yview)
        self.laps_frame = tk.Frame(canvas, bg='#161b22')

        self.laps_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.laps_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Empty state
        self.empty_label = tk.Label(
            self.laps_frame,
            text="No laps recorded yet\nPress 'Lap' while running",
            font=('Arial', 11),
            bg='#161b22',
            fg='#8b949e',
            pady=40
        )
        self.empty_label.pack()

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time
            self.start_btn.config(text='Pause', bg='#da3633', activebackground='#e5534b')
            self.lap_btn.config(state='normal')
            self.update_time()
        else:
            # Pause
            self.running = False
            self.start_btn.config(text='Resume', bg='#238636', activebackground='#2ea043')

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.laps = []
        self.time_label.config(text="00:00:00.00", fg='#58a6ff')
        self.start_btn.config(text='Start', bg='#238636', activebackground='#2ea043')
        self.lap_btn.config(state='disabled')
        self.lap_count_label.config(text='0 laps')
        
        # Clear laps
        for widget in self.laps_frame.winfo_children():
            widget.destroy()
        
        self.empty_label = tk.Label(
            self.laps_frame,
            text="No laps recorded yet\nPress 'Lap' while running",
            font=('Arial', 11),
            bg='#161b22',
            fg='#8b949e',
            pady=40
        )
        self.empty_label.pack()

    def record_lap(self):
        if self.running:
            if hasattr(self, 'empty_label'):
                self.empty_label.destroy()
                delattr(self, 'empty_label')

            lap_time = self.elapsed_time
            self.laps.insert(0, lap_time)
            
            # Create lap card
            lap_card = tk.Frame(self.laps_frame, bg='#0d1117', relief=tk.FLAT)
            lap_card.pack(fill=tk.X, pady=3, padx=5)

            # Lap number and time
            left_frame = tk.Frame(lap_card, bg='#0d1117')
            left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)

            tk.Label(
                left_frame,
                text=f"Lap {len(self.laps)}",
                font=('Arial', 11, 'bold'),
                bg='#0d1117',
                fg='#58a6ff'
            ).pack(side=tk.LEFT)

            tk.Label(
                left_frame,
                text=self.format_time(lap_time),
                font=('Courier New', 13, 'bold'),
                bg='#0d1117',
                fg='#c9d1d9'
            ).pack(side=tk.RIGHT)

            # Split time (if not first lap)
            if len(self.laps) > 1:
                split = lap_time - self.laps[1]
                split_color = '#3fb950' if split > 0 else '#f85149'
                
                split_frame = tk.Frame(lap_card, bg='#0d1117')
                split_frame.pack(side=tk.RIGHT, padx=15)
                
                tk.Label(
                    split_frame,
                    text=f"Split: {self.format_time(abs(split))}",
                    font=('Arial', 9),
                    bg='#0d1117',
                    fg='#8b949e'
                ).pack()

            self.lap_count_label.config(text=f"{len(self.laps)} lap{'s' if len(self.laps) != 1 else ''}")

