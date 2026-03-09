"""
Music Player - Simple & Perfect UI
Play audio files with playlist and controls
Requires: pip install pygame-ce
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Initialize pygame mixer
        pygame.mixer.init()

