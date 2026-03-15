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
            
            # Reposition paddle 2 (right)
            self.canvas.coords(
                self.paddle2,
                self.canvas_width - 30 - self.paddle_width,
                self.canvas_height // 2 - self.paddle_height // 2,
                self.canvas_width - 30,
                self.canvas_height // 2 + self.paddle_height // 2
            )
            
            # Reposition ball
            ball_x = self.canvas_width // 2
            ball_y = self.canvas_height // 2
            self.canvas.coords(
                self.ball,
                ball_x - self.ball_size, ball_y - self.ball_size,
                ball_x + self.ball_size, ball_y + self.ball_size
            )

    def setup_game(self):
        # Create or update paddles
        if self.paddle1 is None:
            self.paddle1 = self.canvas.create_rectangle(
                30, self.canvas_height // 2 - self.paddle_height // 2,
                30 + self.paddle_width, self.canvas_height // 2 + self.paddle_height // 2,
                fill='#2196F3',
                outline=''
            )
        else:
            self.canvas.coords(
                self.paddle1,
                30, self.canvas_height // 2 - self.paddle_height // 2,
                30 + self.paddle_width, self.canvas_height // 2 + self.paddle_height // 2
            )

        if self.paddle2 is None:
            self.paddle2 = self.canvas.create_rectangle(
                self.canvas_width - 30 - self.paddle_width,
                self.canvas_height // 2 - self.paddle_height // 2,
                self.canvas_width - 30,
                self.canvas_height // 2 + self.paddle_height // 2,
                fill='#f44336',
                outline=''
            )
        else:
            self.canvas.coords(
                self.paddle2,
                self.canvas_width - 30 - self.paddle_width,
                self.canvas_height // 2 - self.paddle_height // 2,
                self.canvas_width - 30,
                self.canvas_height // 2 + self.paddle_height // 2
            )

        # Create or update ball
        ball_x = self.canvas_width // 2
        ball_y = self.canvas_height // 2

        if self.ball is None:
            self.ball = self.canvas.create_oval(
                ball_x - self.ball_size, ball_y - self.ball_size,
                ball_x + self.ball_size, ball_y + self.ball_size,
                fill='white',
                outline=''
            )
        else:
            self.canvas.coords(
                self.ball,
                ball_x - self.ball_size, ball_y - self.ball_size,
                ball_x + self.ball_size, ball_y + self.ball_size
            )

    def key_press(self, key):
        self.keys_pressed[key] = True
    
    def key_release(self, key):
        self.keys_pressed[key] = False
    
    def handle_continuous_movement(self):
        """Handle continuous paddle movement when keys are held"""
        if not self.game_running:
            self.root.after(16, self.handle_continuous_movement)
            return
            
        if self.keys_pressed['w']:
            self.move_paddle1('up')
        if self.keys_pressed['s']:
            self.move_paddle1('down')
            
        if self.game_mode == '2player':
            if self.keys_pressed['up']:
                self.move_paddle2('up')
            if self.keys_pressed['down']:
                self.move_paddle2('down')
        
        self.root.after(16, self.handle_continuous_movement)

    def start_game(self):
        if not self.game_running:
            self.game_running = True
            self.start_btn.config(state='disabled')
            
            # Random ball direction
            self.ball_speed_x = random.choice([-7, 7])
            self.ball_speed_y = random.choice([-7, -5, 5, 7])
            
            self.handle_continuous_movement()
            self.move_ball()
            if self.game_mode == 'ai':
                self.ai_move()

    def move_paddle1(self, direction):
        if not self.game_running:
            return
            
        coords = self.canvas.coords(self.paddle1)
        
        if direction == 'up' and coords[1] > 0:
            self.canvas.move(self.paddle1, 0, -self.paddle_speed)
        elif direction == 'down' and coords[3] < self.canvas_height:
            self.canvas.move(self.paddle1, 0, self.paddle_speed)

    def move_paddle2(self, direction):
        if self.game_mode == 'ai' or not self.game_running:
            return
        
        coords = self.canvas.coords(self.paddle2)
        
        if direction == 'up' and coords[1] > 0:
            self.canvas.move(self.paddle2, 0, -self.paddle_speed)
        elif direction == 'down' and coords[3] < self.canvas_height:
            self.canvas.move(self.paddle2, 0, self.paddle_speed)

    def ai_move(self):
        if not self.game_running or self.game_mode != 'ai':
            return

        # Get positions
        ball_coords = self.canvas.coords(self.ball)
        ball_y = (ball_coords[1] + ball_coords[3]) / 2
        
        paddle_coords = self.canvas.coords(self.paddle2)
        paddle_y = (paddle_coords[1] + paddle_coords[3]) / 2

        # Improved AI - faster and more accurate
        ai_speed = 15  # Increased from 8 to 15
        reaction_threshold = 5  # Reduced from 10 to 5 for faster reaction
        
        if ball_y < paddle_y - reaction_threshold and paddle_coords[1] > 0:
            self.canvas.move(self.paddle2, 0, -ai_speed)
        elif ball_y > paddle_y + reaction_threshold and paddle_coords[3] < self.canvas_height:
            self.canvas.move(self.paddle2, 0, ai_speed)

        # Continue AI movement with faster update rate
        self.root.after(20, self.ai_move)  # Changed from 50ms to 20ms

    def move_ball(self):
        if not self.game_running:
            return

        # Move ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        # Get ball position
        ball_coords = self.canvas.coords(self.ball)
        ball_x1, ball_y1, ball_x2, ball_y2 = ball_coords

        # Top/bottom wall collision
        if ball_y1 <= 0 or ball_y2 >= self.canvas_height:
            self.ball_speed_y = -self.ball_speed_y

        # Paddle collision
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        # Left paddle collision
        if (ball_x1 <= paddle1_coords[2] and 
            ball_y2 >= paddle1_coords[1] and 
            ball_y1 <= paddle1_coords[3] and
            self.ball_speed_x < 0):
            self.ball_speed_x = -self.ball_speed_x
            # Add spin based on hit position
            paddle_center = (paddle1_coords[1] + paddle1_coords[3]) / 2
            ball_center = (ball_y1 + ball_y2) / 2
            offset = (ball_center - paddle_center) / (self.paddle_height / 2)
            self.ball_speed_y += offset * 2

        # Right paddle collision
        if (ball_x2 >= paddle2_coords[0] and 
            ball_y2 >= paddle2_coords[1] and 
            ball_y1 <= paddle2_coords[3] and
            self.ball_speed_x > 0):
            self.ball_speed_x = -self.ball_speed_x
            # Add spin
            paddle_center = (paddle2_coords[1] + paddle2_coords[3]) / 2
            ball_center = (ball_y1 + ball_y2) / 2
            offset = (ball_center - paddle_center) / (self.paddle_height / 2)
            self.ball_speed_y += offset * 2

        # Score points
        if ball_x2 < 0:
            # Player 2 scores
            self.player2_score += 1
            self.p2_score_label.config(text=str(self.player2_score))
            self.reset_ball()
        elif ball_x1 > self.canvas_width:
            # Player 1 scores
            self.player1_score += 1
            self.p1_score_label.config(text=str(self.player1_score))
            self.reset_ball()

        # Check win condition
        if self.player1_score >= 5 or self.player2_score >= 5:
            self.end_game()
            return

        # Continue game loop
        self.root.after(16, self.move_ball)  # ~60 FPS

    def reset_ball(self):
        # Reset ball to center
        self.canvas.coords(
            self.ball,
            self.canvas_width // 2 - self.ball_size,
            self.canvas_height // 2 - self.ball_size,
            self.canvas_width // 2 + self.ball_size,
            self.canvas_height // 2 + self.ball_size
        )
        
        # Random direction
        self.ball_speed_x = random.choice([-7, 7])
        self.ball_speed_y = random.choice([-7, -5, 5, 7])

    def end_game(self):
        self.game_running = False
        
        winner = "Player 1" if self.player1_score >= 5 else ("AI" if self.game_mode == 'ai' else "Player 2")
        
        if messagebox.askyesno("Game Over", f"{winner} wins!\n\nPlay again?"):
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        self.player1_score = 0
        self.player2_score = 0
        self.p1_score_label.config(text="0")
        self.p2_score_label.config(text="0")
        self.start_btn.config(state='normal')
        self.reset_ball()

def main():
    root = tk.Tk()
    game = Pong(root)
    root.mainloop()

if __name__ == "__main__":
    main()