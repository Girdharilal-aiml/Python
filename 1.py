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
