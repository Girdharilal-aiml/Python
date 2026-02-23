"""
QR Code Generator
Generate QR codes from text/URLs
Requires: pip install qrcode pillow
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import io

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("550x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(False, False)

        self.qr_image = None
        self.qr_photo = None

        # Title
        tk.Label(
            root,
            text="📱 QR Code Generator",
            font=('Arial', 24, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(pady=20)

        # Input frame
        input_frame = tk.Frame(root, bg='#1a1a2e')
        input_frame.pack(pady=15, padx=30, fill=tk.X)

        tk.Label(
            input_frame,
            text="Enter Text or URL:",
            font=('Arial', 12, 'bold'),
            bg='#1a1a2e',
            fg='white'
        ).pack(anchor='w', pady=(0, 5))

        self.text_input = tk.Text(
            input_frame,
            font=('Arial', 11),
            bg='#16213e',
            fg='white',
            height=4,
            relief=tk.SUNKEN,
            bd=3,
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.X, pady=5)

        # Quick examples
        examples_frame = tk.Frame(root, bg='#1a1a2e')
        examples_frame.pack(pady=10)

        tk.Label(
            examples_frame,
            text="Quick Examples:",
            font=('Arial', 9),
            bg='#1a1a2e',
            fg='#95a5a6'
        ).pack(side=tk.LEFT, padx=5)

        examples = [
            ("Website", "https://www.example.com"),
            ("Email", "mailto:hello@example.com"),
            ("Phone", "tel:+1234567890"),
            ("WiFi", "WIFI:T:WPA;S:NetworkName;P:Password;;")
        ]

        for name, text in examples:
            tk.Button(
                examples_frame,
                text=name,
                command=lambda t=text: self.insert_example(t),
                bg='#34495e',
                fg='white',
                font=('Arial', 8),
                cursor='hand2',
                bd=0,
                width=8
            ).pack(side=tk.LEFT, padx=2)

        # Generate button
        tk.Button(
            root,
            text="🔄 Generate QR Code",
            command=self.generate_qr,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            cursor='hand2',
            bd=0,
            width=20,
            height=2
        ).pack(pady=20)

        # QR code display
        self.qr_frame = tk.Frame(root, bg='white', relief=tk.SUNKEN, bd=5)
        self.qr_frame.pack(pady=10)

        self.qr_label = tk.Label(
            self.qr_frame,
            text="QR code will appear here",
            font=('Arial', 11),
            bg='white',
