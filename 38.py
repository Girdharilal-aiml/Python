"""
Music Organizer Pro
A real-world music library manager with playback, ratings, mood tags,
play history, smart views, search, and M3U export.

Requires: pip install mutagen
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import json
import os
import time
import threading
import subprocess
from pathlib import Path
from datetime import datetime

PYGAME_AVAILABLE = False

try:
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

MOODS = ["Chill", "Energetic", "Sad", "Happy", "Focus", "Party"]

C = {
    'primary':  '#1DB954',
    'accent':   '#1ed760',
    'dark':     '#121212',
    'surface':  '#282828',
    'surface2': '#333333',
    'text':     '#FFFFFF',
    'subtext':  '#B3B3B3',
    'danger':   '#c0392b',
}


class MusicOrganizerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Organizer Pro")
        self.root.geometry("1280x760")
        self.root.configure(bg=C['dark'])
        self.root.resizable(True, True)
        self.root.minsize(960, 620)

        # Data
        self.library_file = "music_library.json"
        self.library = []
        self.playlists = {}
        self.current_playlist = None
        self.current_view = []
        self.load_data()

        # Playback state
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self._song_length = 0
        self._seek_pos = 0
        self._playback_start = 0

        self.build_ui()

        if not MUTAGEN_AVAILABLE:
            messagebox.showwarning(
                "mutagen not found",
                "Install mutagen for metadata reading:\n\npip install mutagen"
            )

    # ------------------------------------------------------------------ data

    def load_data(self):
        if os.path.exists(self.library_file):
            try:
                with open(self.library_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.library = data.get('library', [])
                    self.playlists = data.get('playlists', {})
            except Exception:
                self.library = []
                self.playlists = {}

    def save_data(self):
        with open(self.library_file, 'w', encoding='utf-8') as f:
            json.dump({'library': self.library, 'playlists': self.playlists},
                      f, indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------- ui

    def build_ui(self):
        self._build_header()
        body = tk.Frame(self.root, bg=C['dark'])
        body.pack(fill=tk.BOTH, expand=True)
        self._build_sidebar(body)
        self._build_center(body)
        self._build_right_panel(body)
        self._build_playback_bar()
        self.status_label = tk.Label(
            self.root, text="", font=('Arial', 9),
            bg=C['surface'], fg=C['subtext'], anchor='w', padx=10
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

        self.display_playlists()
        self.show_library()
        self.update_stats_panel()


