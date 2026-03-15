"""
Pong Game - Simple & Perfect UI
Classic 2-player paddle game with AI opponent
"""

import tkinter as tk
from tkinter import messagebox
import random

class Pong:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong")
        self.root.geometry("800x600")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(600, 450)

        # Game settings (will be updated on resize)
        self.canvas_width = 800
        self.canvas_height = 500
        
        # Paddle settings
        self.paddle_width = 15
        self.paddle_height = 100
        self.paddle_speed = 20
        
        # Ball settings
        self.ball_size = 15
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        
        # Game state
        self.game_running = False
        self.game_mode = 'ai'  # 'ai' or '2player'
        self.player1_score = 0
        self.player2_score = 0

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Scores
        score_frame = tk.Frame(header, bg='#f5f5f5')
        score_frame.pack(expand=True)

        self.p1_score_label = tk.Label(
            score_frame,
            text="0",
            font=('Arial', 28, 'bold'),
            bg='#f5f5f5',
            fg='#2196F3'
        )
        self.p1_score_label.pack(side=tk.LEFT, padx=50)

        tk.Label(
            score_frame,
            text="🏓",
            font=('Arial', 24),
            bg='#f5f5f5'
        ).pack(side=tk.LEFT, padx=20)

        self.p2_score_label = tk.Label(
            score_frame,
            text="0",
            font=('Arial', 28, 'bold'),
            bg='#f5f5f5',
            fg='#f44336'
        )
        self.p2_score_label.pack(side=tk.LEFT, padx=50)

        # Canvas
        self.canvas = tk.Canvas(
            root,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind resize event
        self.canvas.bind('<Configure>', self.on_resize)

        # Center line (will be drawn on resize)
        self.center_lines = []

        # Controls info
        controls = tk.Frame(root, bg='white', height=40)
        controls.pack(fill=tk.X)

        # Mode selection
        mode_frame = tk.Frame(controls, bg='white')
        mode_frame.pack(side=tk.LEFT, padx=20, pady=5)

        tk.Label(
            mode_frame,
            text="Mode:",
            font=('Arial', 10, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT, padx=5)

        self.ai_btn = tk.Button(
            mode_frame,
            text="vs AI",
            command=lambda: self.set_mode('ai'),
            font=('Arial', 9, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=10,
            pady=3
        )
        self.ai_btn.pack(side=tk.LEFT, padx=2)

        self.two_player_btn = tk.Button(
            mode_frame,
            text="2 Players",
            command=lambda: self.set_mode('2player'),
            font=('Arial', 9, 'bold'),
            bg='#e0e0e0',
            fg='#333',
            bd=0,
            cursor='hand2',
            padx=10,
            pady=3
        )
        self.two_player_btn.pack(side=tk.LEFT, padx=2)

        # Start button
        self.start_btn = tk.Button(
            controls,
            text="▶ START",
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            cursor='hand2',
            padx=20,
            pady=8
        )
        self.start_btn.pack(side=tk.RIGHT, padx=20, pady=5)

        # Controls label
        self.controls_label = tk.Label(
            controls,
            text="Player 1: W/S  |  AI: Auto",
            font=('Arial', 9),
            bg='white',
            fg='#666'
        )
        self.controls_label.pack(side=tk.RIGHT, padx=10)

        # Bind keys (both lowercase and uppercase)
        self.root.bind('<w>', lambda e: self.move_paddle1('up'))
        self.root.bind('<W>', lambda e: self.move_paddle1('up'))
        self.root.bind('<s>', lambda e: self.move_paddle1('down'))
        self.root.bind('<S>', lambda e: self.move_paddle1('down'))
        self.root.bind('<Up>', lambda e: self.move_paddle2('up'))
        self.root.bind('<Down>', lambda e: self.move_paddle2('down'))
        
        # Allow continuous movement
        self.keys_pressed = {'w': False, 's': False, 'up': False, 'down': False}
        self.root.bind('<KeyPress-w>', lambda e: self.key_press('w'))
        self.root.bind('<KeyPress-W>', lambda e: self.key_press('w'))
        self.root.bind('<KeyPress-s>', lambda e: self.key_press('s'))
        self.root.bind('<KeyPress-S>', lambda e: self.key_press('s'))
        self.root.bind('<KeyRelease-w>', lambda e: self.key_release('w'))
        self.root.bind('<KeyRelease-W>', lambda e: self.key_release('w'))
        self.root.bind('<KeyRelease-s>', lambda e: self.key_release('s'))
        self.root.bind('<KeyRelease-S>', lambda e: self.key_release('s'))
        self.root.bind('<KeyPress-Up>', lambda e: self.key_press('up'))
        self.root.bind('<KeyPress-Down>', lambda e: self.key_press('down'))
        self.root.bind('<KeyRelease-Up>', lambda e: self.key_release('up'))
        self.root.bind('<KeyRelease-Down>', lambda e: self.key_release('down'))

        # Initialize game objects
        self.paddle1 = None
        self.paddle2 = None
        self.ball = None
        
        # Update canvas size after window is ready
        self.root.after(100, self.initialize_game)

    def set_mode(self, mode):
        if self.game_running:
            return
        
        self.game_mode = mode
        
        if mode == 'ai':
            self.ai_btn.config(bg='#4CAF50', fg='white')
            self.two_player_btn.config(bg='#e0e0e0', fg='#333')
            self.controls_label.config(text="Player 1: W/S  |  AI: Auto")
        else:
            self.ai_btn.config(bg='#e0e0e0', fg='#333')
            self.two_player_btn.config(bg='#4CAF50', fg='white')
            self.controls_label.config(text="Player 1: W/S  |  Player 2: ↑/↓")

    def initialize_game(self):
        """Initialize game after window is ready"""
        self.update_canvas_size()
        self.setup_game()
    
    def on_resize(self, event):
        """Handle window resize"""
        if event.width != self.canvas_width or event.height != self.canvas_height:
            self.update_canvas_size()
            if self.paddle1 and self.paddle2 and self.ball:
                self.reposition_game_elements()
    
    def update_canvas_size(self):
        """Update canvas dimensions"""
        self.canvas.update_idletasks()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        
        # Redraw center line
        for line in self.center_lines:
            self.canvas.delete(line)
        self.center_lines = []
        
        for i in range(0, self.canvas_height, 20):
            line = self.canvas.create_rectangle(
                self.canvas_width // 2 - 2, i,
                self.canvas_width // 2 + 2, i + 10,
                fill='white',
                outline=''
            )
            self.center_lines.append(line)
    
    def reposition_game_elements(self):
        """Reposition paddles and ball to maintain relative positions"""
        if not self.game_running:
            # Reposition paddle 1 (left)
            self.canvas.coords(
                self.paddle1,
                30, self.canvas_height // 2 - self.paddle_height // 2,
                30 + self.paddle_width, self.canvas_height // 2 + self.paddle_height // 2
            )
            
        
        
