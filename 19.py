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
        
    
