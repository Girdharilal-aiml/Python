"""
Simple Budget Calculator
Track income, expenses, and see monthly totals
"""

import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Calculator")
        self.root.geometry("700x550")
        self.root.configure(bg="#f0f0f0")
        
        self.data_file = "budget.json"
        self.data = self.load_data()
        
        self.categories = ["Food", "Transport", "Bills", "Entertainment", "Shopping", "Other"]
        
        self.setup_ui()
        self.update_summary()
    
    def load_data(self):
        """Load saved data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {"income": 0, "expenses": []}
        return {"income": 0, "expenses": []}
    
    def save_data(self):
        """Save data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def setup_ui(self):
        """Create the interface"""
        # Title
        tk.Label(self.root, text="💰 Budget Calculator", font=("Arial", 20, "bold"),
                bg="#f0f0f0", fg="#333").pack(pady=15)
        
        # Income section
        income_frame = tk.LabelFrame(self.root, text="Monthly Income", font=("Arial", 12, "bold"),
                                     bg="#e8f5e9", fg="#2e7d32", padx=20, pady=15)
        income_frame.pack(fill=tk.X, padx=20, pady=10)
        
        entry_frame = tk.Frame(income_frame, bg="#e8f5e9")
        entry_frame.pack()
        
        tk.Label(entry_frame, text="Enter Income: $", font=("Arial", 11),
                bg="#e8f5e9").pack(side=tk.LEFT, padx=5)
        
        self.income_entry = tk.Entry(entry_frame, font=("Arial", 11), width=15)
        self.income_entry.pack(side=tk.LEFT, padx=5)
        self.income_entry.insert(0, str(self.data.get("income", 0)))
        
        tk.Button(entry_frame, text="Save Income", font=("Arial", 10), bg="#4caf50",
                 fg="white", padx=15, pady=5, command=self.save_income).pack(side=tk.LEFT, padx=10)
        
        # Add expense section
        expense_frame = tk.LabelFrame(self.root, text="Add Expense", font=("Arial", 12, "bold"),
                                      bg="#fff3e0", fg="#e65100", padx=20, pady=15)
        expense_frame.pack(fill=tk.X, padx=20, pady=10)
        
        row1 = tk.Frame(expense_frame, bg="#fff3e0")
        row1.pack(pady=5)
        
        tk.Label(row1, text="Category:", font=("Arial", 10), bg="#fff3e0").pack(side=tk.LEFT, padx=5)
        self.category_var = tk.StringVar(value=self.categories[0])
        category_menu = tk.OptionMenu(row1, self.category_var, *self.categories)
        category_menu.config(font=("Arial", 10), bg="white", width=12)
        category_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row1, text="Amount: $", font=("Arial", 10), bg="#fff3e0").pack(side=tk.LEFT, padx=10)
        self.amount_entry = tk.Entry(row1, font=("Arial", 10), width=12)
        self.amount_entry.pack(side=tk.LEFT, padx=5)
        
        row2 = tk.Frame(expense_frame, bg="#fff3e0")
        row2.pack(pady=5)
        
        tk.Label(row2, text="Description:", font=("Arial", 10), bg="#fff3e0").pack(side=tk.LEFT, padx=5)
        self.desc_entry = tk.Entry(row2, font=("Arial", 10), width=30)
        self.desc_entry.pack(side=tk.LEFT, padx=5)
        
