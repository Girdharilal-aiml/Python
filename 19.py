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
        
    
