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

