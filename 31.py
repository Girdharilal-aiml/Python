"""
Memory Card Game - Simple & Perfect UI
Flip cards and match pairs
"""

import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Game")
        self.root.geometry("700x800")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(600, 700)

        # Game state
        self.cards = []
        self.card_buttons = []
        self.flipped = []
        self.matched = []
        self.moves = 0
        self.pairs_found = 0
        self.game_active = False

        # Card emojis
        self.symbols = ['🍎', '🍌', '🍇', '🍊', '🍓', '🍒', '🍑', '🍍',
                       '🥝', '🥥', '🍉', '🍋', '🥭', '🍏', '🫐', '🍈']

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🃏 Memory Card Game",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=20)

        # Score panel
        score_frame = tk.Frame(root, bg='white')
        score_frame.pack(pady=15)

        # Moves
        moves_container = tk.Frame(score_frame, bg='white')
        moves_container.pack(side=tk.LEFT, padx=20)

        tk.Label(
            moves_container,
            text="MOVES:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#666'
        ).pack()

        self.moves_label = tk.Label(
            moves_container,
            text="0",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#2196F3'
        )
        self.moves_label.pack()

        # Pairs
        pairs_container = tk.Frame(score_frame, bg='white')
        pairs_container.pack(side=tk.LEFT, padx=20)

        tk.Label(
            pairs_container,
            text="PAIRS:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#666'
        ).pack()

        self.pairs_label = tk.Label(
            pairs_container,
            text="0 / 8",
            font=('Arial', 20, 'bold'),
            bg='white',
            fg='#4CAF50'
        )
        self.pairs_label.pack()

        # Difficulty selection
        diff_frame = tk.Frame(root, bg='white')
        diff_frame.pack(pady=10)

        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT, padx=10)

        self.difficulty = tk.StringVar(value='4x4')
        
        difficulties = [('4x4 (Easy)', '4x4'), ('4x6 (Medium)', '4x6'), ('4x8 (Hard)', '4x8')]
        for text, value in difficulties:
            tk.Radiobutton(
                diff_frame,
                text=text,
                variable=self.difficulty,
                value=value,
                font=('Arial', 10),
                bg='white',
                fg='#333',
                selectcolor='white',
                command=self.change_difficulty
            ).pack(side=tk.LEFT, padx=5)

        # Game board
        self.board_frame = tk.Frame(root, bg='white')
        self.board_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Buttons
        btn_frame = tk.Frame(root, bg='white')
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="🔄 New Game",
            command=self.new_game,
            font=('Arial', 14, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=25,
            pady=12
        ).pack()

        # Initialize game
        self.new_game()

    def change_difficulty(self):
        if self.game_active:
            if messagebox.askyesno("Change Difficulty", "Start a new game with new difficulty?"):
                self.new_game()

    def new_game(self):
        # Clear board
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Reset state
        self.cards = []
        self.card_buttons = []
        self.flipped = []
        self.matched = []
        self.moves = 0
        self.pairs_found = 0
        self.game_active = True

        # Update labels
        self.moves_label.config(text="0")
        
        # Get grid size
        diff = self.difficulty.get()
        if diff == '4x4':
            rows, cols = 4, 4
            num_pairs = 8
        elif diff == '4x6':
            rows, cols = 4, 6
            num_pairs = 12
        else:  # 4x8
            rows, cols = 4, 8
            num_pairs = 16

        self.pairs_label.config(text=f"0 / {num_pairs}")

        # Create card pairs
        selected_symbols = self.symbols[:num_pairs]
        self.cards = selected_symbols * 2  # Create pairs
        random.shuffle(self.cards)

        # Create card buttons
        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                
                btn = tk.Button(
                    self.board_frame,
                    text="?",
                    font=('Arial', 32),
                    bg='#2196F3',
                    fg='white',
                    bd=0,
                    cursor='hand2',
                    command=lambda idx=index: self.flip_card(idx)
                )
                btn.grid(row=i, column=j, padx=3, pady=3, sticky='nsew')
                self.card_buttons.append(btn)

        # Configure grid weights for responsive sizing
        for i in range(rows):
            self.board_frame.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.board_frame.grid_columnconfigure(j, weight=1)

    def flip_card(self, index):
        # Ignore if already flipped or matched
        if index in self.flipped or index in self.matched:
            return

        # Ignore if 2 cards already flipped
        if len(self.flipped) >= 2:
            return

        # Flip the card
        self.flipped.append(index)
        self.card_buttons[index].config(
            text=self.cards[index],
            bg='white',
            state='disabled'
        )

        # Check if 2 cards are flipped
        if len(self.flipped) == 2:
            self.moves += 1
            self.moves_label.config(text=str(self.moves))
            self.root.after(1000, self.check_match)

    def check_match(self):
        idx1, idx2 = self.flipped

        if self.cards[idx1] == self.cards[idx2]:
            # Match found!
            self.matched.extend(self.flipped)
            self.pairs_found += 1
            
            # Get total pairs
            diff = self.difficulty.get()
            total_pairs = 8 if diff == '4x4' else (12 if diff == '4x6' else 16)
            
            self.pairs_label.config(text=f"{self.pairs_found} / {total_pairs}")
            
            # Keep cards face up, change color
            for idx in self.flipped:
                self.card_buttons[idx].config(bg='#4CAF50')
            
            # Check if game is won
            if self.pairs_found == total_pairs:
                self.win_game()
        else:
            # No match - flip back
            for idx in self.flipped:
                self.card_buttons[idx].config(
                    text="?",
                    bg='#2196F3',
                    state='normal'
                )

        # Clear flipped list
        self.flipped = []

    def win_game(self):
        self.game_active = False
        
        # Show win message
        message = f"🎉 Congratulations!\n\nYou won in {self.moves} moves!"
        
        if messagebox.askyesno("You Win!", message + "\n\nPlay again?"):
            self.new_game()

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()