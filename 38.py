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


