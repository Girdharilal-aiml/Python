"""
Unit Converter - Modern UI
Convert between different units (temperature, length, weight, volume)
"""

import tkinter as tk
from tkinter import ttk, font as tkfont

class UnitConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Unit Converter")
        self.root.geometry("550x650")
        self.root.configure(bg='#0d1117')
        self.root.resizable(False, False)

        # Conversion data
        self.conversions = {
            "Temperature": {
                "units": ["Celsius", "Fahrenheit", "Kelvin"],
                "formulas": {
                    ("Celsius", "Fahrenheit"): lambda x: x * 9/5 + 32,
                    ("Celsius", "Kelvin"): lambda x: x + 273.15,
                    ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
                    ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
                    ("Kelvin", "Celsius"): lambda x: x - 273.15,
                    ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32,
                }
            },
            "Length": {
                "units": ["Meters", "Kilometers", "Miles", "Feet", "Inches", "Centimeters"],
                "to_meters": {
                    "Meters": 1,
                    "Kilometers": 1000,
                    "Miles": 1609.34,
                    "Feet": 0.3048,
                    "Inches": 0.0254,
                    "Centimeters": 0.01
                }
            },
            "Weight": {
                "units": ["Kilograms", "Grams", "Pounds", "Ounces", "Tons"],
                "to_kg": {
                    "Kilograms": 1,
                    "Grams": 0.001,
                    "Pounds": 0.453592,
                    "Ounces": 0.0283495,
                    "Tons": 1000
                }
            },
            "Volume": {
                "units": ["Liters", "Milliliters", "Gallons", "Cups", "Fluid Ounces"],
                "to_liters": {
                    "Liters": 1,
                    "Milliliters": 0.001,
                    "Gallons": 3.78541,
                    "Cups": 0.236588,
                    "Fluid Ounces": 0.0295735
                }
            }
        }

        self.current_category = "Temperature"

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🔄",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Unit Converter",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Category selector
        category_frame = tk.Frame(main_frame, bg='#161b22')
        category_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            category_frame,
            text="Category:",
            font=('Arial', 12, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', padx=20, pady=(15, 10))
