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
    
