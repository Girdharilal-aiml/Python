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
