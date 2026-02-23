"""
Random Quote Display
Shows inspirational quotes with categories
"""

import tkinter as tk
from tkinter import font as tkfont
import random

class QuoteDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote")
        self.root.geometry("600x500")
        self.root.configure(bg='#0f0f23')
        self.root.resizable(False, False)

        # Quotes database
        self.quotes = {
            "Motivational": [
                ("The only way to do great work is to love what you do.", "Steve Jobs"),
                ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
                ("Success is not final, failure is not fatal.", "Winston Churchill"),
                ("The future belongs to those who believe in their dreams.", "Eleanor Roosevelt"),
                ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
                ("The harder you work, the luckier you get.", "Gary Player"),
                ("Dream big and dare to fail.", "Norman Vaughan"),
                ("It always seems impossible until it's done.", "Nelson Mandela"),
            ],
            "Wisdom": [
                ("The only true wisdom is in knowing you know nothing.", "Socrates"),
                ("In the middle of difficulty lies opportunity.", "Albert Einstein"),
                ("Life is 10% what happens to you and 90% how you react.", "Charles R. Swindoll"),
                ("The mind is everything. What you think you become.", "Buddha"),
                ("Knowledge speaks, but wisdom listens.", "Jimi Hendrix"),
                ("The journey of a thousand miles begins with one step.", "Lao Tzu"),
                ("Turn your wounds into wisdom.", "Oprah Winfrey"),
                ("Experience is the teacher of all things.", "Julius Caesar"),
            ],
            "Success": [
                ("Success is not the key to happiness. Happiness is the key to success.", "Albert Schweitzer"),
                ("Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
                ("Don't be afraid to give up the good to go for the great.", "John D. Rockefeller"),
                ("I find that the harder I work, the more luck I seem to have.", "Thomas Jefferson"),
                ("Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
                ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
                ("If you really look closely, most overnight successes took a long time.", "Steve Jobs"),
                ("Opportunities don't happen. You create them.", "Chris Grosser"),
            ],
            "Happiness": [
                ("Happiness is not something ready made. It comes from your own actions.", "Dalai Lama"),
                ("The best way to cheer yourself up is to cheer somebody else up.", "Mark Twain"),
                ("Happiness is when what you think, what you say, and what you do are in harmony.", "Mahatma Gandhi"),
                ("Be happy for this moment. This moment is your life.", "Omar Khayyam"),
                ("The purpose of our lives is to be happy.", "Dalai Lama"),
                ("Happiness depends upon ourselves.", "Aristotle"),
                ("Count your age by friends, not years. Count your life by smiles, not tears.", "John Lennon"),
                ("The happiest people don't have the best of everything, they make the best of everything.", "Unknown"),
            ],
            "Funny": [
                ("I'm not superstitious, but I am a little stitious.", "Michael Scott"),
                ("The elevator to success is out of order. You'll have to use the stairs.", "Joe Girard"),
                ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison"),
                ("If you think you are too small to make a difference, try sleeping with a mosquito.", "Dalai Lama"),
                ("Age is of no importance unless you're a cheese.", "Billie Burke"),
                ("Before you marry a person, make them use a computer with slow Internet.", "Will Ferrell"),
                ("The road to success is dotted with many tempting parking spaces.", "Will Rogers"),
                ("I used to think I was indecisive, but now I'm not so sure.", "Unknown"),
            ]
        }

        self.current_category = "Motivational"
        self.current_quote = None

        # Title
        tk.Label(
            root,
            text="✨ Daily Inspiration",
            font=('Arial', 26, 'bold'),
            bg='#0f0f23',
            fg='white'
        ).pack(pady=20)

        # Quote display frame
        quote_frame = tk.Frame(root, bg='#1a1a3e', relief=tk.RAISED, bd=5)
        quote_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

        # Quote text
        self.quote_label = tk.Label(
            quote_frame,
            text="Click 'New Quote' to get started!",
            font=('Georgia', 16, 'italic'),
            bg='#1a1a3e',
            fg='#ecf0f1',
            wraplength=500,
            justify='center',
            pady=20
        )
        self.quote_label.pack(expand=True)

        # Author label
        self.author_label = tk.Label(
            quote_frame,
            text="",
            font=('Arial', 13, 'bold'),
            bg='#1a1a3e',
            fg='#3498db',
            pady=10
        )
        self.author_label.pack()

        # Category selector
        category_frame = tk.Frame(root, bg='#0f0f23')
        category_frame.pack(pady=15)

        tk.Label(
            category_frame,
            text="Category:",
            font=('Arial', 11, 'bold'),
            bg='#0f0f23',
            fg='#bdc3c7'
        ).pack(side=tk.LEFT, padx=10)

        for category in self.quotes.keys():
            tk.Button(
                category_frame,
                text=category,
                command=lambda c=category: self.set_category(c),
                bg='#34495e',
                fg='white',
                font=('Arial', 9, 'bold'),
                cursor='hand2',
                bd=0,
                width=12,
                height=1
            ).pack(side=tk.LEFT, padx=3)

        # New quote button
        tk.Button(
            root,
            text="🔄 New Quote",
            command=self.show_random_quote,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            width=20,
            height=2
        ).pack(pady=15)

        # Category indicator
        self.category_label = tk.Label(
            root,
            text=f"Current: {self.current_category}",
            font=('Arial', 10),
            bg='#0f0f23',
            fg='#95a5a6'
        )
        self.category_label.pack(pady=5)

    def set_category(self, category):
        self.current_category = category
        self.category_label.config(text=f"Current: {category}")
        self.show_random_quote()

    def show_random_quote(self):
        # Get random quote from current category
        quotes_list = self.quotes[self.current_category]
        quote, author = random.choice(quotes_list)
        
        # Update display
        self.quote_label.config(text=f'"{quote}"')
        self.author_label.config(text=f"— {author}")
        
        # Change quote color based on category
        colors = {
            "Motivational": "#e74c3c",
            "Wisdom": "#3498db",
            "Success": "#2ecc71",
            "Happiness": "#f39c12",
            "Funny": "#9b59b6"
        }
        self.quote_label.config(fg=colors.get(self.current_category, "#ecf0f1"))

def main():
    root = tk.Tk()
    app = QuoteDisplay(root)
    root.mainloop()

if __name__ == "__main__":
    main()