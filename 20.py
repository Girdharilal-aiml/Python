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
        
