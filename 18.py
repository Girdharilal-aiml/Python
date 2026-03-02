"""
Image Editor - Modern UI (Responsive)
Edit images: crop, rotate, filters, brightness, contrast
Requires: pip install pillow
"""

import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import os

class ImageEditor:
