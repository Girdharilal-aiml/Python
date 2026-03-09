"""
Music Player - Simple & Perfect UI
Play audio files with playlist and controls
Requires: pip install pygame-ce
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pygame

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        self.root.minsize(500, 600)

        # Initialize pygame mixer
        pygame.mixer.init()

        # State
        self.playlist = []
        self.current_index = -1
        self.is_playing = False
        self.is_paused = False
        self.start_position = 0  # Track where playback started (in seconds)

        # Header
        header = tk.Frame(root, bg='#f5f5f5', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🎵 Music Player",
            font=('Arial', 24, 'bold'),
            bg='#f5f5f5',
            fg='#333'
        ).pack(pady=20)

        # Now playing
        now_playing_frame = tk.Frame(root, bg='white')
        now_playing_frame.pack(fill=tk.X, pady=15)

        tk.Label(
            now_playing_frame,
            text="Now Playing:",
            font=('Arial', 11),
            bg='white',
            fg='#666'
        ).pack()

        self.current_song_label = tk.Label(
            now_playing_frame,
            text="No song selected",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#333',
            wraplength=500
        )
        self.current_song_label.pack(pady=5)

        # Playback controls - Main row
        controls_frame = tk.Frame(root, bg='white')
        controls_frame.pack(pady=10)

        tk.Button(
            controls_frame,
            text="⏮",
            command=self.previous_song,
            font=('Arial', 20),
            bg='#f5f5f5',
            fg='#333',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#e0e0e0'
        ).pack(side=tk.LEFT, padx=5)

        self.play_btn = tk.Button(
            controls_frame,
            text="▶",
            command=self.play_pause,
            font=('Arial', 24),
            bg='#4CAF50',
            fg='white',
            width=3,
            height=1,
            bd=0,
            cursor='hand2',
            activebackground='#45a049'
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="⏹",
            command=self.stop_song,
            font=('Arial', 20),
            bg='#f44336',
            fg='white',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#da190b'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            controls_frame,
            text="⏭",
            command=self.next_song,
            font=('Arial', 20),
            bg='#f5f5f5',
            fg='#333',
            width=3,
            bd=0,
            cursor='hand2',
            activebackground='#e0e0e0'
        ).pack(side=tk.LEFT, padx=5)

        # Skip controls - Second row
        skip_frame = tk.Frame(root, bg='white')
        skip_frame.pack(pady=5)

        tk.Button(
            skip_frame,
            text="⏪ 10s",
            command=self.skip_backward,
            font=('Arial', 10, 'bold'),
            bg='#FF9800',
            fg='white',
            width=8,
            bd=0,
            cursor='hand2',
            activebackground='#F57C00',
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            skip_frame,
            text="10s ⏩",
            command=self.skip_forward,
            font=('Arial', 10, 'bold'),
            bg='#FF9800',
            fg='white',
            width=8,
            bd=0,
            cursor='hand2',
            activebackground='#F57C00',
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        # Playlist
        playlist_label_frame = tk.Frame(root, bg='white')
        playlist_label_frame.pack(fill=tk.X, padx=20, pady=(20, 5))

        tk.Label(
            playlist_label_frame,
            text="Playlist:",
            font=('Arial', 13, 'bold'),
            bg='white',
            fg='#333'
        ).pack(side=tk.LEFT)

        tk.Button(
            playlist_label_frame,
            text="+ Add Files",
            command=self.add_songs,
            font=('Arial', 10, 'bold'),
            bg='#2196F3',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#0b7dda'
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            playlist_label_frame,
            text="Clear",
            command=self.clear_playlist,
            font=('Arial', 10, 'bold'),
            bg='#f44336',
            fg='white',
            bd=0,
            padx=10,
            pady=5,
            cursor='hand2',
            activebackground='#da190b'
        ).pack(side=tk.RIGHT)

        # Playlist listbox
        list_frame = tk.Frame(root, bg='white')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.playlist_box = tk.Listbox(
            list_frame,
            font=('Arial', 10),
            bg='#f5f5f5',
            fg='#333',
            selectbackground='#2196F3',
            selectforeground='white',
            bd=1,
            relief=tk.SOLID,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_box.yview)

        self.playlist_box.bind('<Double-Button-1>', self.play_selected)

        # Status bar
        status_frame = tk.Frame(root, bg='#f5f5f5', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)

        self.song_count_label = tk.Label(
            status_frame,
            text="0 songs",
            font=('Arial', 9),
            bg='#f5f5f5',
            fg='#666',
            anchor='e'
        )
        self.song_count_label.pack(side=tk.RIGHT, padx=15, pady=5)

    def add_songs(self):
        files = filedialog.askopenfilenames(
            title="Select Music Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
                ("All Files", "*.*")
            ]
        )

        for file in files:
            if file not in self.playlist:
                self.playlist.append(file)
                filename = os.path.basename(file)
                self.playlist_box.insert(tk.END, filename)

        self.update_song_count()

    def play_selected(self, event):
        selection = self.playlist_box.curselection()
        if selection:
            self.current_index = selection[0]
            self.play_song()

    def play_song(self, start_pos=0):
        if not self.playlist or self.current_index < 0:
            return

        try:
            song_path = self.playlist[self.current_index]
            
            # Stop current song if playing
            pygame.mixer.music.stop()
            
            # Load and play new song from specified position
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(start=start_pos)
            
            self.start_position = start_pos
            
            filename = os.path.basename(song_path)
            self.current_song_label.config(text=filename)
            self.play_btn.config(text="⏸")
            
            # Highlight current song
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
            self.playlist_box.see(self.current_index)
            
            self.status_label.config(text="Playing...")
            self.is_playing = True
            self.is_paused = False
            
            # Check for song end
            self.check_song_end()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not play file:\n{str(e)}")

    def play_pause(self):
        if not self.playlist:
            messagebox.showwarning("No Songs", "Add songs to the playlist first!")
            return

        if not self.is_playing:
            # Start playing
            if self.current_index < 0:
                self.current_index = 0
            self.play_song()
        elif self.is_paused:
            # Resume playing
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.play_btn.config(text="⏸")
            self.status_label.config(text="Playing...")
        else:
            # Pause playing
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_btn.config(text="▶")
            self.status_label.config(text="Paused")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.start_position = 0
        self.play_btn.config(text="▶")
        self.current_song_label.config(text="Stopped")
        self.status_label.config(text="Stopped")

    def skip_forward(self):
        if not self.is_playing or self.is_paused:
            return
        try:
            # Calculate current position: start_position + time elapsed
            elapsed = pygame.mixer.music.get_pos() / 1000  # milliseconds to seconds
            current_pos = self.start_position + elapsed
            new_pos = current_pos + 10
            
            # Replay from new position
            self.play_song(start_pos=new_pos)
            self.status_label.config(text=f"Skipped +10s")
        except Exception as e:
            # If skip fails, show message
            self.status_label.config(text="Skip not supported for this format")

    def skip_backward(self):
        if not self.is_playing or self.is_paused:
            return
        try:
            # Calculate current position: start_position + time elapsed
            elapsed = pygame.mixer.music.get_pos() / 1000  # milliseconds to seconds
            current_pos = self.start_position + elapsed
            new_pos = max(0, current_pos - 10)
            
            # Replay from new position
            self.play_song(start_pos=new_pos)
            self.status_label.config(text=f"Skipped -10s")
        except Exception as e:
            # If skip fails, show message
            self.status_label.config(text="Skip not supported for this format")

    def check_song_end(self):
        """Check if song has ended and play next"""
        if self.is_playing and not self.is_paused:
            if not pygame.mixer.music.get_busy():
                # Song ended, play next
                self.next_song()
            else:
                # Check again after 100ms
                self.root.after(100, self.check_song_end)

    def next_song(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play_song()

    def previous_song(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play_song()

    def clear_playlist(self):
        if messagebox.askyesno("Clear Playlist", "Remove all songs from playlist?"):
            self.stop_song()
            self.playlist.clear()
            self.playlist_box.delete(0, tk.END)
            self.current_index = -1
            self.current_song_label.config(text="No song selected")
            self.update_song_count()

    def update_song_count(self):
        count = len(self.playlist)
        self.song_count_label.config(text=f"{count} song{'s' if count != 1 else ''}")

def main():
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()