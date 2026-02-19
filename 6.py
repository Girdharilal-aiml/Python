"""
Countdown Timer
Simple & useful timer with tkinter
"""

import tkinter as tk
from tkinter import messagebox
import time

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("450x500")
        self.root.configure(bg='#0f0f0f')
        self.root.resizable(False, False)

        self.running = False
        self.paused = False
        self.time_left = 0  # in seconds

        # Title
        tk.Label(
            root,
            text="⏱️ Countdown Timer",
            font=('Arial', 24, 'bold'),
            bg='#0f0f0f',
            fg='white'
        ).pack(pady=20)

        # Time display
        self.time_label = tk.Label(
            root,
            text="00:00:00",
            font=('Courier', 56, 'bold'),
            bg='#1a1a1a',
            fg='#00ff00',
            relief=tk.SUNKEN,
            bd=5
        )
        self.time_label.pack(pady=20, padx=30, fill=tk.X)

        # Input frame
        input_frame = tk.Frame(root, bg='#0f0f0f')
        input_frame.pack(pady=20)

        tk.Label(input_frame, text="Hours:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=0, padx=5)
        tk.Label(input_frame, text="Minutes:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=1, padx=5)
        tk.Label(input_frame, text="Seconds:", bg='#0f0f0f', fg='white', font=('Arial', 11)).grid(row=0, column=2, padx=5)

        self.hours_var = tk.StringVar(value="0")
        self.minutes_var = tk.StringVar(value="0")
        self.seconds_var = tk.StringVar(value="0")

        hours_entry = tk.Entry(input_frame, textvariable=self.hours_var, width=8, font=('Arial', 18), justify='center')
        hours_entry.grid(row=1, column=0, padx=5)

        minutes_entry = tk.Entry(input_frame, textvariable=self.minutes_var, width=8, font=('Arial', 18), justify='center')
        minutes_entry.grid(row=1, column=1, padx=5)

        seconds_entry = tk.Entry(input_frame, textvariable=self.seconds_var, width=8, font=('Arial', 18), justify='center')
        seconds_entry.grid(row=1, column=2, padx=5)

        # Quick preset buttons
        preset_frame = tk.Frame(root, bg='#0f0f0f')
        preset_frame.pack(pady=10)

        tk.Label(preset_frame, text="Quick Set:", bg='#0f0f0f', fg='#aaa', font=('Arial', 10)).pack()

        presets_inner = tk.Frame(preset_frame, bg='#0f0f0f')
        presets_inner.pack(pady=5)

        presets = [
            ("1 min", 0, 1, 0),
            ("5 min", 0, 5, 0),
            ("10 min", 0, 10, 0),
            ("25 min", 0, 25, 0),
            ("1 hour", 1, 0, 0)
        ]

        for text, h, m, s in presets:
            tk.Button(
                presets_inner,
                text=text,
                command=lambda h=h, m=m, s=s: self.set_preset(h, m, s),
                bg='#2c2c2c',
                fg='white',
                font=('Arial', 9),
                cursor='hand2',
                bd=0,
                width=8
            ).pack(side=tk.LEFT, padx=3)

        # Control buttons
        btn_frame = tk.Frame(root, bg='#0f0f0f')
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="▶ Start",
            command=self.start,
            bg='#27ae60',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            cursor='hand2',
            bd=0
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(
            btn_frame,
            text="⏸ Pause",
            command=self.pause,
            bg='#f39c12',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            cursor='hand2',
            bd=0,
            state='disabled'
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(
            btn_frame,
            text="⟳ Reset",
            command=self.reset,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            width=10,
            height=2,
            cursor='hand2',
            bd=0
        )
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def set_preset(self, h, m, s):
        if not self.running:
            self.hours_var.set(str(h))
            self.minutes_var.set(str(m))
            self.seconds_var.set(str(s))

    def start(self):
        if self.running and not self.paused:
            return

        if not self.paused:
            # Get time from inputs
            try:
                hours = int(self.hours_var.get() or 0)
                minutes = int(self.minutes_var.get() or 0)
                seconds = int(self.seconds_var.get() or 0)
                
                self.time_left = hours * 3600 + minutes * 60 + seconds
                
                if self.time_left <= 0:
                    messagebox.showwarning("Invalid Time", "Please set a time greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
                return

        self.running = True
        self.paused = False
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal', text="⏸ Pause")
        self.countdown()

    def pause(self):
        if self.running:
            if self.paused:
                # Resume
                self.paused = False
                self.pause_btn.config(text="⏸ Pause")
                self.countdown()
            else:
                # Pause
                self.paused = True
                self.pause_btn.config(text="▶ Resume")

    def reset(self):
        self.running = False
        self.paused = False
        self.time_left = 0
        self.time_label.config(text="00:00:00", fg='#00ff00')
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="⏸ Pause")
        self.hours_var.set("0")
        self.minutes_var.set("0")
        self.seconds_var.set("0")

    def countdown(self):
        if not self.running or self.paused:
            return

        if self.time_left > 0:
            # Calculate hours, minutes, seconds
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60

            # Update display
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)

            # Change color based on time left
            if self.time_left <= 10:
                self.time_label.config(fg='#ff0000')  # Red for last 10 seconds
            elif self.time_left <= 60:
                self.time_label.config(fg='#ff9900')  # Orange for last minute
            else:
                self.time_label.config(fg='#00ff00')  # Green

            self.time_left -= 1
            self.root.after(1000, self.countdown)
        else:
            # Timer finished
            self.time_label.config(text="00:00:00", fg='#ff0000')
            self.running = False
            self.start_btn.config(state='normal')
            self.pause_btn.config(state='disabled')
            
            # Alert
            self.root.bell()  # System beep
            messagebox.showinfo("⏰ Time's Up!", "Countdown finished!")

    def update_display(self):
        hours = self.time_left // 3600
        minutes = (self.time_left % 3600) // 60
        seconds = self.time_left % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def main():
    root = tk.Tk()
    timer = CountdownTimer(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()