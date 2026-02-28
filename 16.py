"""
Typing Speed Test - Modern UI
Test your typing speed (WPM) and accuracy
"""

import tkinter as tk
from tkinter import font as tkfont
import random
import time

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x700")
        self.root.configure(bg='#0d1117')
        self.root.resizable(True, True)  # Allow resizing
        self.root.minsize(600, 500)  # Set minimum size

        # Test paragraphs
        self.paragraphs = [
            "The quick brown fox jumps over the lazy dog near the riverbank.",
            "Programming is the art of telling a computer what to do through code.",
            "Practice makes perfect when learning to type faster and more accurately.",
            "Technology has changed the way we communicate and share information.",
            "Typing speed is measured in words per minute and accuracy percentage.",
            "The best time to plant a tree was twenty years ago. The second best time is now.",
            "Success is not final, failure is not fatal. It is the courage to continue that counts.",
            "Life is what happens when you are busy making other plans for the future.",
            "The only way to do great work is to love what you do every single day.",
            "Innovation distinguishes between a leader and a follower in any field.",
        ]

        # Test state
        self.current_text = ""
        self.start_time = None
        self.test_running = False
        self.test_completed = False

        # Custom fonts
        self.title_font = tkfont.Font(family='Arial', size=28, weight='bold')
        self.text_font = tkfont.Font(family='Georgia', size=16)
        self.input_font = tkfont.Font(family='Courier New', size=14)

        # Main container
        main_frame = tk.Frame(root, bg='#0d1117')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="⌨️",
            font=('Arial', 40),
            bg='#161b22',
            fg='#58a6ff'
        ).pack(side=tk.LEFT, padx=(20, 10), pady=15)
        
        tk.Label(
            title_frame,
            text="Typing Speed Test",
            font=self.title_font,
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(side=tk.LEFT, pady=15)

        # Instructions
        instructions_frame = tk.Frame(main_frame, bg='#161b22')
        instructions_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(
            instructions_frame,
            text="📝 Type the text below as fast and accurately as you can!",
            font=('Arial', 12),
            bg='#161b22',
            fg='#8b949e'
        ).pack(pady=12)

        # Text to type card
        text_card = tk.Frame(main_frame, bg='#161b22', relief=tk.FLAT)
        text_card.pack(fill=tk.X, pady=10)

        tk.Label(
            text_card,
            text="Text to Type:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', padx=20, pady=(15, 10))

        self.text_label = tk.Label(
            text_card,
            text="Click 'Start Test' to begin",
            font=self.text_font,
            bg='#161b22',
            fg='#58a6ff',
            wraplength=700,
            justify='left'
        )
        self.text_label.pack(padx=20, pady=(0, 20), anchor='w', fill=tk.X)
        
        # Bind resize event to update wraplength
        self.root.bind('<Configure>', self.on_resize)

        # Input area
        input_card = tk.Frame(main_frame, bg='#161b22')
        input_card.pack(fill=tk.X, pady=10)

        tk.Label(
            input_card,
            text="Your Typing:",
            font=('Arial', 13, 'bold'),
            bg='#161b22',
            fg='#c9d1d9'
        ).pack(anchor='w', padx=20, pady=(15, 10))

        self.input_text = tk.Text(
            input_card,
            font=self.input_font,
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#58a6ff',
            relief=tk.FLAT,
            bd=0,
            height=4,
            wrap=tk.WORD,
            state='disabled'
        )
        self.input_text.pack(padx=20, pady=(0, 15), fill=tk.X)
        self.input_text.bind('<KeyRelease>', self.on_type)

        # Timer and stats
        self.stats_frame = tk.Frame(main_frame, bg='#0d1117')
        self.stats_frame.pack(pady=15, fill=tk.X)

        # Create stats cards with grid for better responsiveness
        self.stats_container = tk.Frame(self.stats_frame, bg='#0d1117')
        self.stats_container.pack()

        # Timer
        timer_card = tk.Frame(self.stats_container, bg='#161b22')
        timer_card.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        tk.Label(
            timer_card,
            text="⏱️ Time",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#8b949e'
        ).pack(pady=(10, 5))

        self.timer_label = tk.Label(
            timer_card,
            text="0.0s",
            font=('Arial', 20, 'bold'),
            bg='#161b22',
            fg='#58a6ff'
        )
        self.timer_label.pack(pady=(0, 10), padx=20)

        # WPM
        wpm_card = tk.Frame(self.stats_container, bg='#161b22')
        wpm_card.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        tk.Label(
            wpm_card,
            text="⚡ WPM",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#8b949e'
        ).pack(pady=(10, 5))

        self.wpm_label = tk.Label(
            wpm_card,
            text="0",
            font=('Arial', 20, 'bold'),
            bg='#161b22',
            fg='#3fb950'
        )
        self.wpm_label.pack(pady=(0, 10), padx=20)

        # Accuracy
        accuracy_card = tk.Frame(self.stats_container, bg='#161b22')
        accuracy_card.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

        tk.Label(
            accuracy_card,
            text="🎯 Accuracy",
            font=('Arial', 11, 'bold'),
            bg='#161b22',
            fg='#8b949e'
        ).pack(pady=(10, 5))

        self.accuracy_label = tk.Label(
            accuracy_card,
            text="0%",
            font=('Arial', 20, 'bold'),
            bg='#161b22',
            fg='#d29922'
        )
        self.accuracy_label.pack(pady=(0, 10), padx=20)
        
        # Make columns expand equally
        self.stats_container.grid_columnconfigure(0, weight=1)
        self.stats_container.grid_columnconfigure(1, weight=1)
        self.stats_container.grid_columnconfigure(2, weight=1)

        # Buttons
        btn_frame = tk.Frame(main_frame, bg='#0d1117')
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(
            btn_frame,
            text="Start Test",
            command=self.start_test,
            bg='#238636',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            width=15,
            height=2,
            activebackground='#2ea043',
            activeforeground='white'
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Reset",
            command=self.reset_test,
            bg='#21262d',
            fg='#c9d1d9',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            relief=tk.FLAT,
            width=15,
            height=2,
            activebackground='#30363d',
            activeforeground='white'
        ).pack(side=tk.LEFT, padx=10)

        # Result message
        self.result_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 12, 'bold'),
            bg='#0d1117',
            fg='#3fb950'
        )
        self.result_label.pack(pady=10)

    def on_resize(self, event):
        # Update text wraplength based on window width
        if event.widget == self.root:
            new_width = self.root.winfo_width()
            # Set wraplength to window width minus padding
            wrap_width = max(300, new_width - 120)
            self.text_label.config(wraplength=wrap_width)
            
            # Stack stats vertically on narrow screens
            if new_width < 700:
                # Reconfigure to vertical layout
                for i, widget in enumerate(self.stats_container.winfo_children()):
                    widget.grid(row=i, column=0, padx=10, pady=5, sticky='ew')
            else:
                # Reconfigure to horizontal layout
                for i, widget in enumerate(self.stats_container.winfo_children()):
                    widget.grid(row=0, column=i, padx=10, pady=5, sticky='ew')

    def start_test(self):
        # Reset state
        self.test_running = True
        self.test_completed = False
        self.start_time = time.time()
        
        # Select random text
        self.current_text = random.choice(self.paragraphs)
        self.text_label.config(text=self.current_text, fg='#c9d1d9')
        
        # Enable input
        self.input_text.config(state='normal')
        self.input_text.delete('1.0', tk.END)
        self.input_text.focus()
        
        # Update button
        self.start_btn.config(state='disabled', bg='#21262d')
        
        # Reset stats
        self.timer_label.config(text="0.0s")
        self.wpm_label.config(text="0")
        self.accuracy_label.config(text="0%")
        self.result_label.config(text="")
        
        # Start timer
        self.update_timer()

    def reset_test(self):
        self.test_running = False
        self.test_completed = False
        self.start_time = None
        
        self.text_label.config(text="Click 'Start Test' to begin", fg='#58a6ff')
        self.input_text.config(state='disabled')
        self.input_text.delete('1.0', tk.END)
        
        self.start_btn.config(state='normal', bg='#238636')
        
        self.timer_label.config(text="0.0s")
        self.wpm_label.config(text="0")
        self.accuracy_label.config(text="0%")
        self.result_label.config(text="")

    def update_timer(self):
        if self.test_running and not self.test_completed:
            elapsed = time.time() - self.start_time
            self.timer_label.config(text=f"{elapsed:.1f}s")
            self.root.after(100, self.update_timer)

    def on_type(self, event):
        if not self.test_running or self.test_completed:
            return

        typed_text = self.input_text.get('1.0', 'end-1c')
        
        # Calculate WPM
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            words_typed = len(typed_text.split())
            minutes = elapsed_time / 60
            wpm = int(words_typed / minutes) if minutes > 0 else 0
            self.wpm_label.config(text=str(wpm))

        # Calculate accuracy
        correct_chars = 0
        total_chars = len(typed_text)
        
        for i in range(min(len(typed_text), len(self.current_text))):
            if typed_text[i] == self.current_text[i]:
                correct_chars += 1
        
        if total_chars > 0:
            accuracy = int((correct_chars / total_chars) * 100)
            self.accuracy_label.config(text=f"{accuracy}%")
            
            # Color code accuracy
            if accuracy >= 95:
                self.accuracy_label.config(fg='#3fb950')
            elif accuracy >= 80:
                self.accuracy_label.config(fg='#d29922')
            else:
                self.accuracy_label.config(fg='#f85149')

        # Check if test is complete
        if typed_text == self.current_text:
            self.complete_test()

    def complete_test(self):
        self.test_completed = True
        self.test_running = False
        
        # Disable input
        self.input_text.config(state='disabled')
        
        # Calculate final stats
        elapsed_time = time.time() - self.start_time
        words = len(self.current_text.split())
        minutes = elapsed_time / 60
        wpm = int(words / minutes)
        
        # Show result message
        if wpm >= 80:
            message = "🏆 Excellent! You're a typing master!"
            color = '#3fb950'
        elif wpm >= 60:
            message = "🎉 Great job! Very good typing speed!"
            color = '#58a6ff'
        elif wpm >= 40:
            message = "👍 Good work! Keep practicing!"
            color = '#d29922'
        else:
            message = "💪 Keep practicing to improve your speed!"
            color = '#8b949e'
        
        self.result_label.config(text=message, fg=color)
        self.start_btn.config(state='normal', bg='#238636')

def main():
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()

if __name__ == "__main__":
    main()