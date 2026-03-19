"""
Contact Manager - Simple & Perfect UI
Manage contacts with search and vCard export
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(800, 600)

