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
