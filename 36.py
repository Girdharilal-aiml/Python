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

        tk.Label(
            search_frame,
            text="🔍",
            font=('Arial', 14),
            bg='#f5f5f5'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_contacts())

        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            bg='white',
            fg='#333',
            relief=tk.SOLID,
            bd=1
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        # Contact list
        list_frame = tk.Frame(sidebar, bg='#f5f5f5')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        scroll = tk.Scrollbar(list_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.contacts_listbox = tk.Listbox(
            list_frame,
            font=('Arial', 11),
            bg='white',
            fg='#333',
            selectbackground='#3F51B5',
            selectforeground='white',
            bd=1,
            relief=tk.SOLID,
            yscrollcommand=scroll.set
        )
        self.contacts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.contacts_listbox.yview)
        self.contacts_listbox.bind('<<ListboxSelect>>', self.select_contact)

        # Buttons
        btn_frame = tk.Frame(sidebar, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            btn_frame,
            text="➕ New Contact",
            command=self.new_contact,
            font=('Arial', 10, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=8
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_frame,
            text="🗑️ Delete",
            command=self.delete_contact,
            font=('Arial', 10, 'bold'),
            bg='#f44336',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=8
        ).pack(fill=tk.X, pady=2)

        tk.Button(
            btn_frame,
            text="📤 Export vCard",
            command=self.export_vcard,
            font=('Arial', 10, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            pady=8
        ).pack(fill=tk.X, pady=2)

        # Right side - Contact details
        details_frame = tk.Frame(main_container, bg='white')
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Form title
        self.form_title = tk.Label(
            details_frame,
            text="Contact Details",
            font=('Arial', 18, 'bold'),
            bg='white',
            fg='#333'
        )
        self.form_title.pack(pady=(0, 20))

        # Form container
        form_container = tk.Frame(details_frame, bg='white')
        form_container.pack(fill=tk.BOTH, expand=True)

        # Form fields
        fields = [
            ('First Name:', 'first_name'),
            ('Last Name:', 'last_name'),
            ('Phone:', 'phone'),
            ('Email:', 'email'),
            ('Company:', 'company'),
            ('Address:', 'address'),
            ('Notes:', 'notes')
        ]

        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            field_frame = tk.Frame(form_container, bg='white')
            field_frame.pack(fill=tk.X, pady=8)

            tk.Label(
                field_frame,
                text=label,
                font=('Arial', 11, 'bold'),
                bg='white',
                fg='#333',
                width=12,
                anchor='w'
            ).pack(side=tk.LEFT, padx=(0, 10))

            if field == 'notes':
                # Text widget for notes
                notes_frame = tk.Frame(field_frame, bg='white', relief=tk.SOLID, bd=1)
                notes_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                entry = tk.Text(
                    notes_frame,
                    font=('Arial', 10),
                    bg='white',
                    fg='#333',
                    wrap=tk.WORD,
                    height=4,
                    bd=0,
                    padx=5,
                    pady=5
                )
                entry.pack(fill=tk.BOTH, expand=True)
            else:
                entry = tk.Entry(
                    field_frame,
                    font=('Arial', 11),
                    bg='#f5f5f5',
                    fg='#333',
                    relief=tk.SOLID,
                    bd=1
                )
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

            self.entries[field] = entry

        # Save button
        tk.Button(
            details_frame,
            text="💾 Save Contact",
            command=self.save_contact,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=30,
            pady=12
        ).pack(pady=30)

        # Status bar
        self.status_label = tk.Label(
            root,
            text=f"{len(self.contacts)} contacts",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

        # Display contacts
        self.display_contacts()
        self.clear_form()

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            try:
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    self.contacts = json.load(f)
            except:
                self.contacts = []
