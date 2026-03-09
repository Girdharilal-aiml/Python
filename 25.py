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

        # State
        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.start_position = 0  # Track where playback started (in seconds)

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎵 Music Player",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=20)

        # Now playing
        now_playing_frame = tk.Frame(root, bg='white')
        now_playing_frame.pack(fill=tk.X, pady=15)

        tk.Label(
            now_playing_frame,
            text="Now Playing:",
            font=('Arial', 11),
            bg='white',
            fg='#666'
        ).pack()

        self.current_song_label = tk.Label(
            now_playing_frame,
            text="No song selected",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#333',
            wraplength=500
        )
        self.current_song_label.pack(pady=5)

