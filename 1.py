"""
Lightweight Physics Simulator - Perfect for low-spec laptops
Uses tkinter (built-in, no installation needed)

CONTROLS:
- Click and drag to create particles
- SPACE: Pause/Resume
- R: Reset simulation
- +/-: Increase/Decrease gravity
- C: Clear all particles
- Q: Quit
"""

import tkinter as tk
import math
import random

class Particle:
    def __init__(self, x, y, vx, vy, radius=5, color='blue'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        
    def update(self, dt, gravity):
        self.vy += gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

class PhysicsSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Physics Simulator - Click and Drag to Create Particles")
        
        # Canvas
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        
        # Physics settings
        self.particles = []
        self.gravity = 500  # pixels per second^2
        self.restitution = 0.85  # bounciness
        self.paused = False
        self.dt = 0.016  # ~60 FPS
        
        # Mouse tracking for particle creation
        self.mouse_pressed = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.preview_line = None
        
        # Bind controls
        self.canvas.bind('<ButtonPress-1>', self.on_mouse_press)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_release)
        self.root.bind('<space>', lambda e: self.toggle_pause())
        self.root.bind('r', lambda e: self.reset())
        self.root.bind('c', lambda e: self.clear_particles())
        self.root.bind('q', lambda e: self.root.quit())
        self.root.bind('+', lambda e: self.change_gravity(50))
        self.root.bind('=', lambda e: self.change_gravity(50))
        self.root.bind('-', lambda e: self.change_gravity(-50))
        
        # Info label
        self.info_label = tk.Label(root, text="", bg='white', fg='black')
        self.info_label.pack(fill=tk.X)
        
        # Start with some particles
        self.create_initial_particles()
        
        # Start animation
        self.update()
        
    def create_initial_particles(self):
        colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'orange']
        for _ in range(5):
            x = random.randint(100, self.width - 100)
            y = random.randint(50, 200)
            vx = random.uniform(-150, 150)
            vy = random.uniform(-100, 100)
            color = random.choice(colors)
            self.particles.append(Particle(x, y, vx, vy, radius=8, color=color))
    
    def on_mouse_press(self, event):
        self.mouse_pressed = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
    def on_mouse_drag(self, event):
        if self.mouse_pressed:
            # Draw preview line
            if self.preview_line:
                self.canvas.delete(self.preview_line)
            self.preview_line = self.canvas.create_line(
                self.drag_start_x, self.drag_start_y,
                event.x, event.y,
                fill='white', width=2, arrow=tk.LAST
            )
    
    def on_mouse_release(self, event):
        if self.mouse_pressed:
            # Create particle with velocity based on drag
            vx = (event.x - self.drag_start_x) * 2
            vy = (event.y - self.drag_start_y) * 2
            
            colors = ['red', 'blue', 'green', 'yellow', 'cyan', 'magenta', 'orange', 'white']
            color = random.choice(colors)
            
