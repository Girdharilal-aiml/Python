"""
Snake Game - Simple & Perfect UI
Classic snake with score and speed increase
"""

import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(False, False)

        # Game settings
        self.canvas_width = 600
        self.canvas_height = 600
        self.grid_size = 20
        self.cell_size = self.canvas_width // self.grid_size
        
        # Game state
        self.snake = []
        self.direction = 'Right'
        self.next_direction = 'Right'
        self.food = None
        self.score = 0
        self.high_score = 0
        self.game_running = False
        self.speed = 150  # milliseconds

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Score display
        score_frame = tk.Frame(header, bg='#f5f5f5')
        score_frame.pack(expand=True)

        # Current score
        score_container = tk.Frame(score_frame, bg='#f5f5f5')
        score_container.pack(side=tk.LEFT, padx=30)

        tk.Label(
            score_container,
            text="SCORE:",
            font=('Arial', 11, 'bold'),
            bg='#f5f5f5',
            fg='#666'
        ).pack()

        self.score_label = tk.Label(
            score_container,
            text="0",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#4CAF50'
        )
        self.score_label.pack()

        # High score
        high_score_container = tk.Frame(score_frame, bg='#f5f5f5')
        high_score_container.pack(side=tk.LEFT, padx=30)

        tk.Label(
            high_score_container,
            text="HIGH SCORE:",
            font=('Arial', 11, 'bold'),
            bg='#f5f5f5',
            fg='#666'
        ).pack()

        self.high_score_label = tk.Label(
            high_score_container,
            text="0",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#FF9800'
        )
        self.high_score_label.pack()

        # Canvas
        self.canvas = tk.Canvas(
            root,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#1a1a2e',
            highlightthickness=0
        )
        self.canvas.pack()

        # Draw grid
        self.draw_grid()

        # Controls
        controls = tk.Frame(root, bg='white', height=30)
        controls.pack(fill=tk.X)

        tk.Label(
            controls,
            text="Controls: Arrow Keys or WASD  |  Press SPACE to start/pause",
            font=('Arial', 10),
            bg='white',
            fg='#666'
        ).pack(pady=5)

        # Bind keys
        self.root.bind('<Up>', lambda e: self.change_direction('Up'))
        self.root.bind('<Down>', lambda e: self.change_direction('Down'))
        self.root.bind('<Left>', lambda e: self.change_direction('Left'))
        self.root.bind('<Right>', lambda e: self.change_direction('Right'))
        self.root.bind('<w>', lambda e: self.change_direction('Up'))
        self.root.bind('<s>', lambda e: self.change_direction('Down'))
        self.root.bind('<a>', lambda e: self.change_direction('Left'))
        self.root.bind('<d>', lambda e: self.change_direction('Right'))
        self.root.bind('<space>', lambda e: self.toggle_pause())

        # Show start message
        self.show_message("Press SPACE to start")

    def draw_grid(self):
        # Draw light grid lines
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_height,
                fill='#2a2a3e',
                width=1
            )
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(
                0, i, self.canvas_width, i,
                fill='#2a2a3e',
                width=1
            )

    def show_message(self, text):
        self.canvas.delete('message')
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=text,
            font=('Arial', 24, 'bold'),
            fill='white',
            tags='message'
        )

    def new_game(self):
        # Reset snake
        start_x = self.grid_size // 2
        start_y = self.grid_size // 2
        self.snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        
        # Reset direction
        self.direction = 'Right'
        self.next_direction = 'Right'
        
        # Reset score
        self.score = 0
        self.score_label.config(text="0")
        
        # Reset speed
        self.speed = 150
        
        # Clear canvas
        self.canvas.delete('all')
        self.draw_grid()
        
        # Spawn food
        self.spawn_food()
        
        # Draw snake
        self.draw_snake()
        
        # Start game
        self.game_running = True
        self.move_snake()

    def spawn_food(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
        
        # Draw food
        self.canvas.delete('food')
        self.canvas.create_oval(
            self.food[0] * self.cell_size + 2,
            self.food[1] * self.cell_size + 2,
            (self.food[0] + 1) * self.cell_size - 2,
            (self.food[1] + 1) * self.cell_size - 2,
            fill='#f44336',
            outline='#ff5252',
            width=2,
            tags='food'
        )

