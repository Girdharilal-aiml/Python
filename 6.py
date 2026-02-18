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
