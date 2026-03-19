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

        # Data
        self.contacts_file = "contacts.json"
        self.contacts = []
        self.current_contact = None
        self.load_contacts()

        # Header
        header = tk.Frame(root, bg='#3F51B5', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

