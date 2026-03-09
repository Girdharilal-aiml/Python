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

        # Playback controls - Main row
        controls_frame = tk.Frame(root, bg='white')
        controls_frame.pack(pady=10)

        tk.Button(
            controls_frame,
            text="⏮",
            command=self.previous_song,
            font=('Arial', 20),
            bg='#f5f5f5',
            fg='#333',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#e0e0e0'
        ).pack(side=tk.LEFT, padx=5)

        self.play_btn = tk.Button(
            controls_frame,
            text="▶",
            command=self.play_pause,
            font=('Arial', 24),
            bg='#4CAF50',
            fg='white',
            width=3,
            height=1,
            bd=0,
            cursor='hand2',
            activebackground='#45a049'
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="⏹",
            command=self.stop_song,
            font=('Arial', 20),
            bg='#f44336',
            fg='white',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#da190b'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="⏭",
            command=self.next_song,
            font=('Arial', 20),
            bg='#f5f5f5',
            fg='#333',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#e0e0e0'
        ).pack(side=tk.LEFT, padx=5)

        # Skip controls - Second row
        skip_frame = tk.Frame(root, bg='white')
        skip_frame.pack(pady=5)

        tk.Button(
            skip_frame,
            text="⏪ 10s",
            command=self.skip_backward,
            font=('Arial', 10, 'bold'),
            bg='#FF9800',
            fg='white',
            width=8,
            bd=0,
            cursor='hand2',
            activebackground='#F57C00',
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            skip_frame,
            text="10s ⏩",
            command=self.skip_forward,
            font=('Arial', 10, 'bold'),
            bg='#FF9800',
            fg='white',
            width=8,
            bd=0,
            cursor='hand2',
            activebackground='#F57C00',
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        # Playlist
        playlist_label_frame = tk.Frame(root, bg='white')
        playlist_label_frame.pack(fill=tk.X, padx=20, pady=(20, 5))

        tk.Label(
            playlist_label_frame,
            text="Playlist:",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT)

        tk.Button(
            playlist_label_frame,
            text="+ Add Files",
            command=self.add_songs,
            font=('Arial', 10, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#0b7dda'
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            playlist_label_frame,
            text="Clear",
            command=self.clear_playlist,
            font=('Arial', 10, 'bold'),
            bg='#f44336',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#da190b'
        ).pack(side=tk.RIGHT)

