"""
Language Quiz - Modern UI (Responsive)
Practice vocabulary with multiple languages
"""

import tkinter as tk
from tkinter import font as tkfont
import random

class LanguageQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Quiz")
        self.root.geometry("700x800")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Vocabulary database
        self.vocabularies = {
            "Spanish": [
                ("Hello", "Hola"),
                ("Goodbye", "Adiós"),
                ("Please", "Por favor"),
                ("Thank you", "Gracias"),
                ("Yes", "Sí"),
                ("No", "No"),
                ("Good morning", "Buenos días"),
                ("Good night", "Buenas noches"),
                ("Water", "Agua"),
                ("Food", "Comida"),
                ("Friend", "Amigo"),
                ("Family", "Familia"),
                ("Love", "Amor"),
                ("House", "Casa"),
                ("Book", "Libro"),
                ("Time", "Tiempo"),
                ("Day", "Día"),
                ("Night", "Noche"),
                ("Sun", "Sol"),
                ("Moon", "Luna"),
            ],

