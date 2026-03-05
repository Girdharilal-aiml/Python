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
            "French": [
                ("Hello", "Bonjour"),
                ("Goodbye", "Au revoir"),
                ("Please", "S'il vous plaît"),
                ("Thank you", "Merci"),
                ("Yes", "Oui"),
                ("No", "Non"),
                ("Good morning", "Bon matin"),
                ("Good night", "Bonne nuit"),
                ("Water", "Eau"),
                ("Food", "Nourriture"),
                ("Friend", "Ami"),
                ("Family", "Famille"),
                ("Love", "Amour"),
                ("House", "Maison"),
                ("Book", "Livre"),
                ("Time", "Temps"),
                ("Day", "Jour"),
                ("Night", "Nuit"),
                ("Sun", "Soleil"),
                ("Moon", "Lune"),
            ],
            "German": [
                ("Hello", "Hallo"),
                ("Goodbye", "Auf Wiedersehen"),
                ("Please", "Bitte"),
                ("Thank you", "Danke"),
                ("Yes", "Ja"),
                ("No", "Nein"),
                ("Good morning", "Guten Morgen"),
                ("Good night", "Gute Nacht"),
                ("Water", "Wasser"),
                ("Food", "Essen"),
                ("Friend", "Freund"),
                ("Family", "Familie"),
                ("Love", "Liebe"),
                ("House", "Haus"),
                ("Book", "Buch"),
                ("Time", "Zeit"),
                ("Day", "Tag"),
                ("Night", "Nacht"),
                ("Sun", "Sonne"),
                ("Moon", "Mond"),
            ],
        }

        # Quiz state
        self.current_language = "Spanish"
        self.quiz_active = False
        self.current_word = None
        self.current_answer = None
        self.options = []
        self.score = 0
        self.total_questions = 0
        self.questions_per_quiz = 10

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.word_font = tkfont.Font(family='Arial', size=36, weight='bold')
        self.score_font = tkfont.Font(family='Arial', size=18, weight='bold')

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg='#161b22')
        header_frame.pack(fill=tk.X, pady=(0, 20))

