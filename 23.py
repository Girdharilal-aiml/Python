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
        
