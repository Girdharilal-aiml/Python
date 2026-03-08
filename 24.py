"""
Breakout Game - Simple & Perfect UI
Classic brick-breaking game
"""

import tkinter as tk
from tkinter import messagebox
import random

class Breakout:
    def __init__(self, root):
        self.root = root
        self.root.title("Breakout")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Game settings
        self.canvas_width = 600
        self.canvas_height = 600
        
        # Paddle
        self.paddle_width = 100
        self.paddle_height = 15
        self.paddle_speed = 20
        
        # Ball
        self.ball_radius = 8
        self.ball_speed_x = 4
        self.ball_speed_y = -4
        
        # Bricks
        self.brick_rows = 5
        self.brick_cols = 10
        self.brick_width = 58
        self.brick_height = 20
        self.brick_padding = 2
        
        # Game state
        self.score = 0
        self.lives = 3
        self.game_running = False
        self.bricks = []
        
        # Colors
        self.brick_colors = ['#f44336', '#FF9800', '#FFC107', '#4CAF50', '#2196F3']

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Score
        score_frame = tk.Frame(header, bg='#f5f5f5')
        score_frame.pack(side=tk.LEFT, padx=20, pady=15)

        tk.Label(
            score_frame,
            text="SCORE:",
            font=('Arial', 11, 'bold'),
            bg='#f5f5f5',
            fg='#666'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.score_label = tk.Label(
            score_frame,
            text="0",
            font=('Arial', 18, 'bold'),
            bg='#f5f5f5',
            fg='#4CAF50'
        )
        self.score_label.pack(side=tk.LEFT)

        # Lives
        lives_frame = tk.Frame(header, bg='#f5f5f5')
        lives_frame.pack(side=tk.RIGHT, padx=20, pady=15)

        tk.Label(
            lives_frame,
            text="LIVES:",
            font=('Arial', 11, 'bold'),
            bg='#f5f5f5',
            fg='#666'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.lives_label = tk.Label(
            lives_frame,
            text="❤️ ❤️ ❤️",
            font=('Arial', 14),
            bg='#f5f5f5'
        )
        self.lives_label.pack(side=tk.LEFT)

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack()

        # Controls
        controls = tk.Frame(root, bg='white', height=40)
        controls.pack(fill=tk.X)

        self.start_btn = tk.Button(
            controls,
            text="▶ START",
            command=self.start_game,
            font=('Arial', 12, 'bold'),
            bg='#4CAF50',
            fg='white',
            bd=0,
            width=15,
            height=2,
            cursor='hand2',
            activebackground='#45a049'
        )
        self.start_btn.pack(pady=10)

        # Bind keys
        self.root.bind('<Left>', self.move_paddle_left)
        self.root.bind('<Right>', self.move_paddle_right)
        self.root.bind('<a>', self.move_paddle_left)
        self.root.bind('<d>', self.move_paddle_right)
        
        # Bind resize
        self.root.bind('<Configure>', self.on_resize)

        # Initialize game
        self.setup_game()
    
    def on_resize(self, event):
        # Update canvas size if window is resized
        if event.widget == self.root:
            new_width = max(500, self.root.winfo_width())
            new_height = max(600, self.root.winfo_height() - 100)
            
            if new_width != self.canvas_width or new_height != self.canvas_height:
                self.canvas.config(width=new_width, height=new_height)
                self.canvas_width = new_width
                self.canvas_height = new_height

    def setup_game(self):
        # Clear canvas
        self.canvas.delete("all")
        self.bricks = []
        
        # Create bricks
        offset_x = 10
        offset_y = 50
        
        for row in range(self.brick_rows):
            brick_row = []
            for col in range(self.brick_cols):
                x1 = offset_x + col * (self.brick_width + self.brick_padding)
                y1 = offset_y + row * (self.brick_height + self.brick_padding)
                x2 = x1 + self.brick_width
                y2 = y1 + self.brick_height
                
                color = self.brick_colors[row]
                
                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline='white',
                    width=2,
                    tags='brick'
                )
                brick_row.append(brick)
            self.bricks.append(brick_row)
        
        # Create paddle
        paddle_x = self.canvas_width // 2 - self.paddle_width // 2
        paddle_y = self.canvas_height - 50
        
        self.paddle = self.canvas.create_rectangle(
            paddle_x, paddle_y,
            paddle_x + self.paddle_width, paddle_y + self.paddle_height,
            fill='#fff',
            outline='',
            tags='paddle'
        )
        
        # Create ball
        ball_x = self.canvas_width // 2
        ball_y = self.canvas_height - 70
        
        self.ball = self.canvas.create_oval(
            ball_x - self.ball_radius, ball_y - self.ball_radius,
            ball_x + self.ball_radius, ball_y + self.ball_radius,
            fill='#FFC107',
            outline='',
            tags='ball'
        )

