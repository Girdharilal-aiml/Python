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
