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

    def _build_header(self):
        header = tk.Frame(self.root, bg=C['surface'], height=58)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="♪  Music Organizer Pro",
            font=('Arial', 19, 'bold'), bg=C['surface'], fg=C['primary']
        ).pack(side=tk.LEFT, padx=20, pady=10)

        # Search bar
        sf = tk.Frame(header, bg=C['surface2'], padx=6, pady=4)
        sf.pack(side=tk.LEFT, padx=30, pady=10)
        tk.Label(sf, text="🔍", bg=C['surface2'], fg=C['subtext'],
                 font=('Arial', 11)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.on_search)
        tk.Entry(
            sf, textvariable=self.search_var,
            font=('Arial', 11), bg=C['surface2'], fg=C['text'],
            insertbackground='white', relief=tk.FLAT, width=28, bd=0
        ).pack(side=tk.LEFT, padx=4)

        self.header_stats = tk.Label(
            header, text="", font=('Arial', 9),
            bg=C['surface'], fg=C['subtext']
        )
        self.header_stats.pack(side=tk.RIGHT, padx=20)

    def _sidebar_btn(self, parent, text, cmd):
        tk.Button(
            parent, text=text, command=cmd,
            font=('Arial', 10), bg=C['surface'], fg=C['text'],
            bd=0, relief=tk.FLAT, cursor='hand2',
            anchor='w', padx=15, pady=7,
            activebackground=C['surface2'], activeforeground=C['primary']
        ).pack(fill=tk.X)

    def _build_sidebar(self, body):
        sb = tk.Frame(body, bg=C['surface'], width=215)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack_propagate(False)

        tk.Label(sb, text="LIBRARY", font=('Arial', 8, 'bold'),
                 bg=C['surface'], fg=C['subtext']).pack(anchor='w', padx=15, pady=(14, 4))

        self._sidebar_btn(sb, "📚   All Songs",       self.show_library)
        self._sidebar_btn(sb, "⭐   Top Rated",        self.show_top_rated)
        self._sidebar_btn(sb, "🔥   Most Played",      self.show_most_played)
        self._sidebar_btn(sb, "🕐   Recently Played",  self.show_recently_played)

        tk.Frame(sb, bg=C['surface2'], height=1).pack(fill=tk.X, padx=15, pady=8)

        tk.Label(sb, text="PLAYLISTS", font=('Arial', 8, 'bold'),
                 bg=C['surface'], fg=C['subtext']).pack(anchor='w', padx=15, pady=(0, 4))

        lf = tk.Frame(sb, bg=C['surface'])
        lf.pack(fill=tk.BOTH, expand=True, padx=10)

        sc = tk.Scrollbar(lf)
        sc.pack(side=tk.RIGHT, fill=tk.Y)

        self.playlist_listbox = tk.Listbox(
            lf, font=('Arial', 10),
            bg=C['surface2'], fg=C['text'],
            selectbackground=C['primary'], selectforeground='black',
            bd=0, relief=tk.FLAT, yscrollcommand=sc.set, activestyle='none'
        )
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc.config(command=self.playlist_listbox.yview)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.select_playlist)

        bf = tk.Frame(sb, bg=C['surface'])
        bf.pack(fill=tk.X, padx=10, pady=4)
        tk.Button(bf, text="＋ New", command=self.new_playlist,
                  font=('Arial', 9, 'bold'), bg=C['primary'], fg='black',
                  bd=0, relief=tk.FLAT, cursor='hand2', pady=5
                  ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        tk.Button(bf, text="✕ Delete", command=self.delete_playlist,
                  font=('Arial', 9), bg=C['danger'], fg='white',
                  bd=0, relief=tk.FLAT, cursor='hand2', pady=5
                  ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Button(
            sb, text="📤  Export M3U", command=self.export_m3u,
            font=('Arial', 9), bg=C['surface2'], fg=C['subtext'],
            bd=0, relief=tk.FLAT, cursor='hand2', pady=6
        ).pack(fill=tk.X, padx=10, pady=(2, 8))

    def _build_center(self, body):
        center = tk.Frame(body, bg=C['dark'])
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1)

        # Toolbar
        tb = tk.Frame(center, bg=C['dark'])
        tb.pack(fill=tk.X, padx=10, pady=8)

        for text, cmd, bg, fg in [
            ("➕  Add Songs",       self.add_songs,        C['primary'],  'black'),
            ("🗑  Remove",          self.remove_song,       C['danger'],   'white'),
            ("▶  Add to Playlist", self.add_to_playlist,  C['surface2'], C['text']),
        ]:
            tk.Button(tb, text=text, command=cmd, font=('Arial', 10, 'bold'),
                      bg=bg, fg=fg, bd=0, relief=tk.FLAT, cursor='hand2',
                      padx=12, pady=5).pack(side=tk.LEFT, padx=2)

        self.view_label = tk.Label(tb, text="All Songs",
                                   font=('Arial', 12, 'bold'),
                                   bg=C['dark'], fg=C['text'])
        self.view_label.pack(side=tk.RIGHT, padx=10)

        # Sort bar
        sf = tk.Frame(center, bg=C['dark'])
        sf.pack(fill=tk.X, padx=10, pady=(0, 6))
        tk.Label(sf, text="Sort by:", font=('Arial', 9),
                 bg=C['dark'], fg=C['subtext']).pack(side=tk.LEFT)
        self.sort_var = tk.StringVar(value="Title")
        for s in ["Title", "Artist", "Album", "Year", "Rating", "Plays"]:
            tk.Radiobutton(
                sf, text=s, variable=self.sort_var, value=s,
                command=self.apply_sort,
                font=('Arial', 9), bg=C['dark'], fg=C['subtext'],
                selectcolor=C['surface'], activebackground=C['dark'],
                activeforeground=C['primary']
            ).pack(side=tk.LEFT, padx=6)

        # Table
        tf = tk.Frame(center, bg=C['dark'])
        tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 5))

        vsb = tk.Scrollbar(tf)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        cols = ('Title', 'Artist', 'Album', 'Year', 'Dur', 'Rating', 'Plays', 'Mood')
        self.music_tree = ttk.Treeview(
            tf, columns=cols, show='headings',
            yscrollcommand=vsb.set, selectmode='browse'
        )
        self.music_tree.pack(fill=tk.BOTH, expand=True)
        vsb.config(command=self.music_tree.yview)

        widths = {'Title': 220, 'Artist': 140, 'Album': 120,
                  'Year': 52, 'Dur': 65, 'Rating': 72, 'Plays': 48, 'Mood': 120}
        for col in cols:
            self.music_tree.heading(col, text=col)
            self.music_tree.column(col, width=widths[col], minwidth=40)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
                        background=C['surface'], foreground=C['text'],
                        rowheight=28, fieldbackground=C['surface'], borderwidth=0)
        style.configure("Treeview.Heading",
                        font=('Arial', 9, 'bold'),
                        background=C['surface2'], foreground=C['subtext'],
                        relief=tk.FLAT)
        style.map('Treeview',
                  background=[('selected', C['primary'])],
                  foreground=[('selected', 'black')])

        self.music_tree.bind('<Double-Button-1>', self.on_double_click)
        self.music_tree.bind('<<TreeviewSelect>>', self.on_select_song)

    def _build_right_panel(self, body):
        rp = tk.Frame(body, bg=C['surface'], width=225)
        rp.pack(side=tk.RIGHT, fill=tk.Y)
        rp.pack_propagate(False)

        def section(text):
            tk.Label(rp, text=text, font=('Arial', 8, 'bold'),
                     bg=C['surface'], fg=C['subtext']
                     ).pack(anchor='w', padx=15, pady=(14, 4))

        section("SONG INFO")
        self.details_text = tk.Text(
            rp, font=('Arial', 9), bg=C['surface2'], fg=C['text'],
            wrap=tk.WORD, bd=0, padx=10, pady=8, state='disabled',
            height=8, relief=tk.FLAT
        )
        self.details_text.pack(fill=tk.X, padx=10)
