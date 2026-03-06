"""
Note-Taking App - Simple & Perfect UI
Clean, functional note-taking app
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.root.geometry("900x600")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(700, 500)

        
