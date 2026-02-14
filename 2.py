"""
To-Do List App
Lightweight GUI app using tkinter

FEATURES:
- Add, delete, and mark tasks as complete
- Tasks save automatically to a file
- Priority levels (High, Medium, Low)
- Search/filter tasks
- Clean, simple interface
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime
