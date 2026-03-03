"""
Tic-Tac-Toe Game with AI (GUI Version)
Play against a computer using the Minimax algorithm
Uses tkinter - built-in, lightweight, no extra storage needed
"""

import tkinter as tk
from tkinter import messagebox


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.geometry("400x500")
        self.root.configure(bg="#2c3e50")
        
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Title
        title_label = tk.Label(root, text="TIC-TAC-TOE", font=("Arial", 24, "bold"),
                               bg="#2c3e50", fg="#ecf0f1")
        title_label.pack(pady=10)
        
        subtitle = tk.Label(root, text="You: X  |  AI: O", font=("Arial", 12),
                           bg="#2c3e50", fg="#95a5a6")
        subtitle.pack()
        
        # Game board frame
        board_frame = tk.Frame(root, bg="#34495e")
        board_frame.pack(pady=20)
        
        # Create buttons
        for i in range(3):
            for j in range(3):
                btn = tk.Button(board_frame, text=" ", font=("Arial", 20, "bold"),
                               width=5, height=2, bg="#3498db", fg="white",
                               command=lambda row=i, col=j: self.on_button_click(row, col),
                               activebackground="#2980b9", relief="raised", bd=2)
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = btn
        
        # Status label
        self.status_label = tk.Label(root, text="Your turn!", font=("Arial", 12),
                                     bg="#2c3e50", fg="#2ecc71")
        self.status_label.pack(pady=10)
        
        # Reset button
        reset_btn = tk.Button(root, text="New Game", font=("Arial", 11, "bold"),
                             bg="#e74c3c", fg="white", command=self.reset_game,
                             activebackground="#c0392b", padx=20)
        reset_btn.pack(pady=10)
    
    def on_button_click(self, row, col):
        """Handle player move"""
        if self.game_over:
            messagebox.showinfo("Game Over", "Start a new game!")
            return
        
        if self.board[row][col] != " ":
            messagebox.showwarning("Invalid Move", "Position already taken!")
            return
        
        # Player move
        self.board[row][col] = "X"
        self.update_button(row, col, "X", "#3498db")
        
        if self.is_winner("X"):
            self.end_game("🎉 You Won!")
            return
        
        if self.is_board_full():
            self.end_game("🤝 Draw!")
            return
        
        # AI move
        self.status_label.config(text="AI thinking...", fg="#f39c12")
        self.root.after(500, self.ai_move)
    
    def ai_move(self):
        """Execute AI move"""
        ai_row, ai_col = self.best_move()
        if ai_row is not None:
            self.board[ai_row][ai_col] = "O"
            self.update_button(ai_row, ai_col, "O", "#e74c3c")
            
            if self.is_winner("O"):
                self.end_game("🤖 AI Won!")
                return
            
            if self.is_board_full():
                self.end_game("🤝 Draw!")
                return
        
        self.status_label.config(text="Your turn!", fg="#2ecc71")
    
    def update_button(self, row, col, text, color):
        """Update button appearance"""
        btn = self.buttons[row][col]
        btn.config(text=text, fg="white", bg=color, state="disabled")
    
    def is_winner(self, player):
        """Check if player won"""
        # Check rows
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                return True
        
        # Check columns
        for j in range(3):
            if all(self.board[i][j] == player for i in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        """Check if board is full"""
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))
    
    def get_empty_positions(self):
        """Get empty positions"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
    
    def minimax(self, depth, is_maximizing):
        """Minimax algorithm"""
        if self.is_winner("O"):
            return 10 - depth
        if self.is_winner("X"):
            return depth - 10
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for row, col in self.get_empty_positions():
                self.board[row][col] = "O"
                score = self.minimax(depth + 1, False)
                self.board[row][col] = " "
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row, col in self.get_empty_positions():
                self.board[row][col] = "X"
                score = self.minimax(depth + 1, True)
                self.board[row][col] = " "
                best_score = min(score, best_score)
            return best_score
    
    def best_move(self):
        """Find best AI move"""
        best_score = -float('inf')
        best_pos = (None, None)
        
        for row, col in self.get_empty_positions():
            self.board[row][col] = "O"
            score = self.minimax(0, False)
            self.board[row][col] = " "
            
            if score > best_score:
                best_score = score
                best_pos = (row, col)
        
        return best_pos
    
    def end_game(self, message):
        """End the game"""
        self.game_over = True
        self.status_label.config(text=message, fg="#f39c12", font=("Arial", 14, "bold"))
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")
    
    def reset_game(self):
        """Reset for new game"""
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text="Your turn!", fg="#2ecc71")
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ", bg="#3498db", state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
