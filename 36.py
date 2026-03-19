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

        tk.Label(
            header,
            text="🗂️ Contact Manager",
            font=('Arial', 24, 'bold'),
            bg='#3F51B5',
            fg='white'
        ).pack(pady=18)

        # Main container
        main_container = tk.Frame(root, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar - Contact list
        sidebar = tk.Frame(main_container, bg='#f5f5f5', width=300, relief=tk.SOLID, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Search bar
        search_frame = tk.Frame(sidebar, bg='#f5f5f5')
        search_frame.pack(fill=tk.X, padx=10, pady=10)

