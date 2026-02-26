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
