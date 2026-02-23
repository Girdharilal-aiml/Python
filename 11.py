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
            fg='#7f8c8d',
            width=30,
            height=15
        )
        self.qr_label.pack(padx=10, pady=10)

        # Save button
        self.save_btn = tk.Button(
            root,
            text="💾 Save QR Code",
            command=self.save_qr,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12, 'bold'),
            cursor='hand2',
            bd=0,
            width=20,
            height=2,
            state='disabled'
        )
        self.save_btn.pack(pady=15)

        # Info label
        tk.Label(
            root,
            text="Tip: QR codes work best with URLs, text, phone numbers, or WiFi info",
            font=('Arial', 9, 'italic'),
            bg='#1a1a2e',
            fg='#7f8c8d',
            wraplength=500
        ).pack(pady=10)

    def insert_example(self, text):
        self.text_input.delete('1.0', tk.END)
        self.text_input.insert('1.0', text)

    def generate_qr(self):
        # Get input text
        data = self.text_input.get('1.0', tk.END).strip()

        if not data:
            messagebox.showwarning("Empty Input", "Please enter some text or a URL!")
            return

        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,  # Size of QR code
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create image
            self.qr_image = qr.make_image(fill_color="black", back_color="white")

            # Resize for display (300x300)
            display_image = self.qr_image.resize((300, 300), Image.Resampling.LANCZOS)

            # Convert to PhotoImage for tkinter
            self.qr_photo = ImageTk.PhotoImage(display_image)

            # Display
            self.qr_label.config(image=self.qr_photo, text="")
            self.save_btn.config(state='normal')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code:\n{str(e)}")

    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("No QR Code", "Generate a QR code first!")
            return

        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
