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
            
            self.particles.append(Particle(
                self.drag_start_x, self.drag_start_y,
                vx, vy,
                radius=random.randint(5, 10),
                color=color
            ))
            
            # Remove preview line
            if self.preview_line:
                self.canvas.delete(self.preview_line)
                self.preview_line = None
                
        self.mouse_pressed = False
    
    def toggle_pause(self):
        self.paused = not self.paused
        
    def reset(self):
        self.particles.clear()
        self.create_initial_particles()
        self.gravity = 500
        
    def clear_particles(self):
        self.particles.clear()
        
    def change_gravity(self, delta):
        self.gravity += delta
        self.gravity = max(0, min(2000, self.gravity))  # Limit gravity
    
    def handle_collisions(self):
        # Wall collisions
        for p in self.particles:
            # Bottom
            if p.y + p.radius >= self.height:
                p.y = self.height - p.radius
                p.vy = -abs(p.vy) * self.restitution
                p.vx *= 0.98  # Friction
                
            # Top
            if p.y - p.radius <= 0:
                p.y = p.radius
                p.vy = abs(p.vy) * self.restitution
                
            # Left
            if p.x - p.radius <= 0:
                p.x = p.radius
                p.vx = abs(p.vx) * self.restitution
                
            # Right
            if p.x + p.radius >= self.width:
                p.x = self.width - p.radius
                p.vx = -abs(p.vx) * self.restitution
        
        # Particle-particle collisions
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist = math.sqrt(dx*dx + dy*dy)
                min_dist = p1.radius + p2.radius
                
                if dist < min_dist and dist > 0:
                    # Separate particles
                    overlap = min_dist - dist
                    angle = math.atan2(dy, dx)
                    
                    p1.x -= overlap * math.cos(angle) / 2
                    p1.y -= overlap * math.sin(angle) / 2
                    p2.x += overlap * math.cos(angle) / 2
                    p2.y += overlap * math.sin(angle) / 2
                    
                    # Simple velocity exchange
                    p1.vx, p2.vx = p2.vx * 0.9, p1.vx * 0.9
                    p1.vy, p2.vy = p2.vy * 0.9, p1.vy * 0.9
    
    def update(self):
        if not self.paused:
            # Update physics
            for p in self.particles:
                p.update(self.dt, self.gravity)
            
            self.handle_collisions()
        
        # Render
        self.canvas.delete('particle')
        for p in self.particles:
            self.canvas.create_oval(
                p.x - p.radius, p.y - p.radius,
                p.x + p.radius, p.y + p.radius,
                fill=p.color, outline='white', tags='particle'
            )
        
