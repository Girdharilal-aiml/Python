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
