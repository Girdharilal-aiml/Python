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

        # Title
        title_container = tk.Frame(header_frame, bg='#161b22')
        title_container.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(
            title_container,
            text="🗣️",
            font=('Arial', 35),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            title_container,
            text="Language Quiz",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT)

        # Score display
        score_container = tk.Frame(header_frame, bg='#161b22')
        score_container.pack(side=tk.RIGHT, padx=20, pady=15)

        tk.Label(
            score_container,
            text="SCORE",
            font=('Arial', 10, 'bold'),
            bg='#161b22',
            fg='#8b949e'
        ).pack()

        self.score_label = tk.Label(
            score_container,
            text="0 / 0",
            font=self.score_font,
            bg='#161b22',
            fg='#3fb950'
        )
        self.score_label.pack()

        # Language selector
        lang_frame = tk.Frame(main_frame, bg='#161b22')
        lang_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(
            lang_frame,
            text="Select Language:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, padx=20, pady=15)

        lang_buttons = tk.Frame(lang_frame, bg='#161b22')
        lang_buttons.pack(side=tk.LEFT, pady=15)

        for lang in self.vocabularies.keys():
            btn = tk.Button(
                lang_buttons,
                text=lang,
                command=lambda l=lang: self.select_language(l),
                bg='#21262d' if lang != self.current_language else '#1f6feb',
                fg='#c9d1d9',
                font=('Arial', 11, 'bold'),
                cursor='hand2',
                bd=0,
                width=10,
                activebackground='#30363d'
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Question card (scrollable container)
        self.question_container = tk.Frame(main_frame, bg='#0d1117')
        self.question_container.pack(fill=tk.BOTH, expand=True, pady=10)

        # Canvas for scrolling
        canvas = tk.Canvas(self.question_container, bg='#0d1117', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.question_container, orient='vertical', command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg='#0d1117')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Question content
        question_card = tk.Frame(scrollable_frame, bg='#161b22')
        question_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Instruction/Word display
        self.instruction_label = tk.Label(
            question_card,
            text="Translate to " + self.current_language + ":",
            font=('Arial', 14, 'bold'),
            bg='#161b22',
            fg='#8b949e'
        )
        self.instruction_label.pack(pady=(30, 10))

        self.word_label = tk.Label(
            question_card,
            text="Click 'Start Quiz' to begin",
            font=self.word_font,
            bg='#161b22',
            fg='#58a6ff',
            wraplength=600
        )
        self.word_label.pack(pady=20)

        # Options buttons container
        self.options_frame = tk.Frame(question_card, bg='#161b22')
        self.options_frame.pack(pady=20, fill=tk.X, padx=40)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_frame,
                text="",
                font=('Arial', 14),
                bg='#21262d',
                fg='#c9d1d9',
                cursor='hand2',
                bd=0,
                relief=tk.FLAT,
                activebackground='#30363d',
                wraplength=500,
                state='disabled',
                height=2
            )
            btn.pack(fill=tk.X, pady=8)
            self.option_buttons.append(btn)

        # Result message
        self.result_label = tk.Label(
            question_card,
            text="",
            font=('Arial', 14, 'bold'),
            bg='#161b22',
            fg='#3fb950'
        )
        self.result_label.pack(pady=10)

        # Progress
        self.progress_label = tk.Label(
            question_card,
            text="",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e'
        )
        self.progress_label.pack(pady=(10, 30))

        # Control buttons
        btn_frame = tk.Frame(main_frame, bg='#0d1117')
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="Start Quiz",
            command=self.start_quiz,
            bg='#238636',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            width=15,
            height=2,
            activebackground='#2ea043'
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.next_btn = tk.Button(
            btn_frame,
            text="Next Question",
            command=self.next_question,
            bg='#1f6feb',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            width=15,
            height=2,
            state='disabled',
            activebackground='#388bfd'
        )
        self.next_btn.pack(side=tk.LEFT, padx=10)

        # Bind resize
        self.root.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        if event.widget == self.root:
            # Update word wraplength based on window width
            new_width = self.root.winfo_width()
            wrap_width = max(300, new_width - 150)
            self.word_label.config(wraplength=wrap_width)
            
            for btn in self.option_buttons:
                btn.config(wraplength=max(300, new_width - 250))

    def select_language(self, language):
        self.current_language = language
        self.instruction_label.config(text=f"Translate to {language}:")
        
        # Update language button colors
        for widget in self.root.winfo_children():
            self.update_language_buttons(widget, language)
        
        # Reset quiz if active
        if self.quiz_active:
            self.quiz_active = False
            self.start_btn.config(state='normal')
            self.word_label.config(text="Click 'Start Quiz' to begin")

    def update_language_buttons(self, widget, current_lang):
        for child in widget.winfo_children():
            if isinstance(child, tk.Button) and child.cget('text') in self.vocabularies.keys():
                if child.cget('text') == current_lang:
                    child.config(bg='#1f6feb')
                else:
                    child.config(bg='#21262d')
            self.update_language_buttons(child, current_lang)

    def start_quiz(self):
        self.quiz_active = True
        self.score = 0
        self.total_questions = 0
        self.start_btn.config(state='disabled')
        self.next_btn.config(state='disabled')
        
        self.score_label.config(text=f"{self.score} / {self.total_questions}")
        self.result_label.config(text="")
        
        self.load_question()

    def load_question(self):
        if self.total_questions >= self.questions_per_quiz:
            self.end_quiz()
            return

        # Get random word
        vocab = self.vocabularies[self.current_language]
        self.current_word, self.current_answer = random.choice(vocab)
        
        # Generate options (1 correct + 3 wrong)
        self.options = [self.current_answer]
        
        other_words = [answer for _, answer in vocab if answer != self.current_answer]
        wrong_options = random.sample(other_words, min(3, len(other_words)))
        self.options.extend(wrong_options)
        
        random.shuffle(self.options)
        
        # Update UI
        self.word_label.config(text=self.current_word, fg='#58a6ff')
        self.result_label.config(text="")
        self.progress_label.config(text=f"Question {self.total_questions + 1} of {self.questions_per_quiz}")
        
        # Update option buttons
        for i, btn in enumerate(self.option_buttons):
            if i < len(self.options):
                btn.config(
                    text=self.options[i],
                    state='normal',
                    bg='#21262d',
                    command=lambda opt=self.options[i]: self.check_answer(opt)
                )
            else:
                btn.config(text="", state='disabled')

    def check_answer(self, selected):
        self.total_questions += 1
        
        # Disable all buttons
        for btn in self.option_buttons:
            btn.config(state='disabled')
            
            # Color code the buttons
            if btn.cget('text') == self.current_answer:
                btn.config(bg='#238636')  # Correct answer in green
            elif btn.cget('text') == selected and selected != self.current_answer:
                btn.config(bg='#da3633')  # Wrong selection in red
        
        # Check if correct
        if selected == self.current_answer:
            self.score += 1
            self.result_label.config(text="✓ Correct!", fg='#3fb950')
        else:
