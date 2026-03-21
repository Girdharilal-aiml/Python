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

