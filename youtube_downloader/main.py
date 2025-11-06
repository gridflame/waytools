import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import re
import math
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Try to import PIL for logo handling
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("way.tools - YouTube Downloader")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg='#f5f5f5')
        
        # Center window on screen
        self.center_window()
        
        # Try to set icon if available
        self.setup_icon()
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.url = tk.StringVar()
        self.format_var = tk.StringVar(value="best")
        self.quality_var = tk.StringVar(value="best")
        self.audio_quality_var = tk.StringVar(value="320")  # MP3 bitrate: 192, 256, 320 (best)
        self.is_downloading = False
        
        self.setup_ui()
        self.check_ytdlp()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_icon(self):
        """Set application icon"""
        try:
            def set_icon_from_png(png_path):
                if HAS_PIL and os.path.exists(png_path):
                    try:
                        img = Image.open(png_path)
                        ico_path = png_path.replace('.png', '_temp.ico')
                        img.save(ico_path, format='ICO')
                        self.root.iconbitmap(ico_path)
                        try:
                            os.remove(ico_path)
                        except:
                            pass
                        return True
                    except:
                        pass
                return False
            
            if getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, "logo.png")
                if not set_icon_from_png(icon_path):
                    ico_path = os.path.join(sys._MEIPASS, "logo.ico")
                    if os.path.exists(ico_path):
                        self.root.iconbitmap(ico_path)
            else:
                if not set_icon_from_png("logo.png"):
                    if os.path.exists("logo.ico"):
                        self.root.iconbitmap("logo.ico")
        except:
            pass
    
    def setup_ui(self):
        """Setup professional UI"""
        # Main container with gradient-like background
        main_container = tk.Frame(self.root, bg='#f5f5f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section with professional styling
        header_frame = tk.Frame(main_container, bg='#ffffff', relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#ffffff')
        header_content.pack(fill=tk.X, padx=30, pady=25)
        
        # Logo and title frame
        logo_title_frame = tk.Frame(header_content, bg='#ffffff')
        logo_title_frame.pack(fill=tk.X)
        
        # Logo display
        self.logo_label = tk.Label(logo_title_frame, bg='#ffffff')
        self.logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Load logo image
        try:
            logo_path = None
            if getattr(sys, 'frozen', False):
                logo_path = os.path.join(sys._MEIPASS, "logo.png")
            else:
                logo_path = "logo.png"
            
            if os.path.exists(logo_path) and HAS_PIL:
                logo_img = Image.open(logo_path)
                # Resize logo to fit nicely (max 64px height)
                logo_img.thumbnail((64, 64), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                self.logo_label.config(image=self.logo_photo)
        except Exception as e:
            # If logo fails, just show text
            pass
        
        # Title with professional font
        title_frame = tk.Frame(logo_title_frame, bg='#ffffff')
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = tk.Label(title_frame, text="way.tools", 
                              font=("Segoe UI", 24, "bold"),
                              bg='#ffffff', fg='#2c3e50')
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame, text="YouTube Downloader",
                                 font=("Segoe UI", 11),
                                 bg='#ffffff', fg='#7f8c8d')
        subtitle_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Main content area
        content_frame = tk.Frame(main_container, bg='#ffffff', relief=tk.FLAT)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Content padding
        content_padding = tk.Frame(content_frame, bg='#ffffff')
        content_padding.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # URL Input Section
        url_section = tk.Frame(content_padding, bg='#ffffff')
        url_section.pack(fill=tk.X, pady=(0, 20))
        
        url_label = tk.Label(url_section, text="YouTube URL",
                            font=("Segoe UI", 10, "bold"),
                            bg='#ffffff', fg='#2c3e50', anchor='w')
        url_label.pack(fill=tk.X, pady=(0, 8))
        
        url_entry_frame = tk.Frame(url_section, bg='#ffffff')
        url_entry_frame.pack(fill=tk.X)
        
        self.url_entry = tk.Entry(url_entry_frame, textvariable=self.url,
                                  font=("Segoe UI", 10),
                                  relief=tk.SOLID, borderwidth=1,
                                  highlightthickness=1, highlightcolor='#3498db',
                                  highlightbackground='#e0e0e0')
        self.url_entry.pack(fill=tk.X, ipady=10, padx=(0, 10))
        self.url_entry.bind('<FocusIn>', lambda e: self.url_entry.config(highlightcolor='#3498db'))
        
        # Download Path Section
        path_section = tk.Frame(content_padding, bg='#ffffff')
        path_section.pack(fill=tk.X, pady=(0, 20))
        
        path_label = tk.Label(path_section, text="Download Location",
                              font=("Segoe UI", 10, "bold"),
                              bg='#ffffff', fg='#2c3e50', anchor='w')
        path_label.pack(fill=tk.X, pady=(0, 8))
        
        path_frame = tk.Frame(path_section, bg='#ffffff')
        path_frame.pack(fill=tk.X)
        
        self.path_entry = tk.Entry(path_frame, textvariable=self.download_path,
                                   font=("Segoe UI", 10),
                                   relief=tk.SOLID, borderwidth=1,
                                   highlightthickness=1, highlightcolor='#3498db',
                                   highlightbackground='#e0e0e0')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        
        browse_btn = tk.Button(path_frame, text="Browse",
                              command=self.browse_folder,
                              font=("Segoe UI", 10),
                              bg='#ecf0f1', fg='#2c3e50',
                              relief=tk.FLAT, padx=20, pady=10,
                              cursor='hand2', activebackground='#bdc3c7')
        browse_btn.pack(side=tk.RIGHT)
        
        # Options Section with modern styling
        options_frame = tk.LabelFrame(content_padding, text="Download Options",
                                     font=("Segoe UI", 10, "bold"),
                                     bg='#ffffff', fg='#2c3e50',
                                     relief=tk.FLAT, borderwidth=1,
                                     padx=20, pady=15)
        options_frame.pack(fill=tk.X, pady=(0, 25))
        
        options_inner = tk.Frame(options_frame, bg='#ffffff')
        options_inner.pack(fill=tk.X)
        
        # Format selection with better labels
        format_label = tk.Label(options_inner, text="File Format:",
                               font=("Segoe UI", 10, "bold"),
                               bg='#ffffff', fg='#34495e')
        format_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 5))
        
        # Format descriptions mapping
        format_descriptions = {
            "best": "Best Available (Recommended)",
            "mp4": "MP4 Video (Universal)",
            "webm": "WebM Video (Web)",
            "mp3": "MP3 Audio (Music)",
            "m4a": "M4A Audio (iPhone/iTunes)",
            "wav": "WAV Audio (Lossless)",
            "flac": "FLAC Audio (Lossless Compressed)"
        }
        
        self.format_combo = ttk.Combobox(options_inner, textvariable=self.format_var,
                                        values=["best", "mp4", "webm", "mp3", "m4a", "wav", "flac"],
                                        state="readonly", width=25,
                                        font=("Segoe UI", 10))
        self.format_combo.grid(row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(0, 15))
        
        # Format description label
        self.format_desc_label = tk.Label(options_inner,
                                          text=format_descriptions.get(self.format_var.get(), ""),
                                          font=("Segoe UI", 9),
                                          bg='#ffffff', fg='#7f8c8d',
                                          anchor='w')
        self.format_desc_label.grid(row=2, column=0, sticky=tk.W, padx=(0, 20), pady=(0, 10))
        
        # Video Quality selection (shown for video formats)
        self.quality_label = tk.Label(options_inner, text="Video Quality:",
                                font=("Segoe UI", 10, "bold"),
                                bg='#ffffff', fg='#34495e')
        self.quality_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 10), pady=(0, 5))
        
        # Quality descriptions with better labels
        quality_options = [
            ("best", "Best Available (HD+)"),
            ("1080p", "Full HD 1080p"),
            ("720p", "HD 720p"),
            ("480p", "SD 480p"),
            ("360p", "360p (Mobile)"),
            ("240p", "240p (Low)"),
            ("worst", "Lowest Quality")
        ]
        quality_values = [q[0] for q in quality_options]
        quality_labels = [q[1] for q in quality_options]
        
        self.quality_combo = ttk.Combobox(options_inner, textvariable=self.quality_var,
                                         values=quality_values,
                                         state="readonly", width=25,
                                         font=("Segoe UI", 10))
        self.quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(0, 15))
        
        # Quality description label
        self.quality_desc_label = tk.Label(options_inner,
                                           text=quality_labels[quality_values.index(self.quality_var.get())] if self.quality_var.get() in quality_values else "",
                                           font=("Segoe UI", 9),
                                           bg='#ffffff', fg='#7f8c8d',
                                           anchor='w')
        self.quality_desc_label.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(0, 10))
        
        # Update quality description when changed
        def on_quality_change(event=None):
            if self.quality_var.get() in quality_values:
                idx = quality_values.index(self.quality_var.get())
                self.quality_desc_label.config(text=quality_labels[idx])
        
        self.quality_combo.bind('<<ComboboxSelected>>', on_quality_change)
        
        # Audio bitrate selection (shown when audio format selected)
        self.audio_quality_label = tk.Label(options_inner, text="Audio Quality:",
                                           font=("Segoe UI", 10, "bold"),
                                           bg='#ffffff', fg='#34495e')
        self.audio_quality_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 10), pady=(0, 5))
        self.audio_quality_label.grid_remove()  # Hidden by default
        
        # Audio quality options with descriptions
        audio_quality_options = [
            ("320", "320 kbps - Best Quality (MP3 Maximum)"),
            ("256", "256 kbps - High Quality"),
            ("192", "192 kbps - Good Quality"),
            ("128", "128 kbps - Standard Quality")
        ]
        audio_values = [a[0] for a in audio_quality_options]
        audio_labels = [a[1] for a in audio_quality_options]
        
        self.audio_quality_combo = ttk.Combobox(options_inner, textvariable=self.audio_quality_var,
                                               values=audio_values,
                                               state="readonly", width=25,
                                               font=("Segoe UI", 10))
        self.audio_quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=(0, 15))
        self.audio_quality_combo.grid_remove()  # Hidden by default
        
        # Audio quality description label
        self.audio_quality_desc_label = tk.Label(options_inner,
                                                text=audio_labels[audio_values.index(self.audio_quality_var.get())] if self.audio_quality_var.get() in audio_values else "",
                                                font=("Segoe UI", 9),
                                                bg='#ffffff', fg='#7f8c8d',
                                                anchor='w',
                                                wraplength=300)
        self.audio_quality_desc_label.grid(row=2, column=1, sticky=tk.W, padx=(0, 20), pady=(0, 10))
        self.audio_quality_desc_label.grid_remove()  # Hidden by default
        
        # Update audio quality description when changed
        def on_audio_quality_change(event=None):
            if self.audio_quality_var.get() in audio_values:
                idx = audio_values.index(self.audio_quality_var.get())
                self.audio_quality_desc_label.config(text=audio_labels[idx])
        
        self.audio_quality_combo.bind('<<ComboboxSelected>>', on_audio_quality_change)
        
        # Info label for audio quality (helpful note)
        self.audio_info_label = tk.Label(options_inner, 
                                        text="💡 Note: YouTube source is typically 128-256kbps AAC. Higher bitrates preserve quality better.",
                                        font=("Segoe UI", 9),
                                        bg='#e8f4f8', fg='#2c3e50',
                                        wraplength=500,
                                        padx=10, pady=8,
                                        relief=tk.FLAT,
                                        anchor='w',
                                        justify='left')
        self.audio_info_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=(0, 20), pady=(5, 0))
        self.audio_info_label.grid_remove()  # Hidden by default
        
        # Update format description when changed
        def on_format_desc_change(event=None):
            fmt = self.format_var.get()
            desc = format_descriptions.get(fmt, "")
            self.format_desc_label.config(text=desc)
            self.on_format_change(event)
        
        # Show/hide audio quality based on format selection
        self.format_combo.bind('<<ComboboxSelected>>', on_format_desc_change)
        
        # Initialize format description on startup
        initial_fmt = self.format_var.get()
        initial_desc = format_descriptions.get(initial_fmt, "")
        self.format_desc_label.config(text=initial_desc)
        
        # Initialize quality description on startup
        if initial_fmt not in ["mp3", "m4a", "wav", "flac"]:
            initial_quality = self.quality_var.get()
            if initial_quality in quality_values:
                idx = quality_values.index(initial_quality)
                self.quality_desc_label.config(text=quality_labels[idx])
        
        # Download Button - Professional styling
        button_frame = tk.Frame(content_padding, bg='#ffffff')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.download_btn = tk.Button(button_frame, text="Download",
                                      command=self.start_download,
                                      font=("Segoe UI", 12, "bold"),
                                      bg='#3498db', fg='#ffffff',
                                      relief=tk.FLAT, padx=40, pady=15,
                                      cursor='hand2', activebackground='#2980b9',
                                      activeforeground='#ffffff')
        self.download_btn.pack()
        
        # Progress section with loading spinner
        progress_frame = tk.Frame(content_padding, bg='#ffffff')
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Loading spinner container
        spinner_frame = tk.Frame(progress_frame, bg='#ffffff')
        spinner_frame.pack(pady=10)
        
        # Create animated loading spinner (circle)
        self.spinner_canvas = tk.Canvas(spinner_frame, width=40, height=40, 
                                        bg='#ffffff', highlightthickness=0)
        # Start hidden - only show when downloading
        self.spinner_canvas.pack_forget()
        
        # Spinner variables
        self.spinner_angle = 0
        self.spinner_visible = False
        
        # Status label
        self.status_label = tk.Label(progress_frame, text="Ready",
                                     font=("Segoe UI", 10),
                                     bg='#ffffff', fg='#27ae60')
        self.status_label.pack(pady=(10, 0))
        
        # Log output section
        log_label = tk.Label(content_padding, text="Download Log",
                            font=("Segoe UI", 10, "bold"),
                            bg='#ffffff', fg='#2c3e50', anchor='w')
        log_label.pack(fill=tk.X, pady=(0, 8))
        
        log_frame = tk.Frame(content_padding, bg='#ffffff')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Styled log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12,
                                                  font=("Consolas", 9),
                                                  bg='#f8f9fa', fg='#2c3e50',
                                                  relief=tk.SOLID, borderwidth=1,
                                                  wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TProgressbar', background='#3498db', troughcolor='#ecf0f1')
    
    def animate_spinner(self):
        """Animate the loading spinner - rotating circle with fade effect"""
        if not self.spinner_visible:
            return
        
        self.spinner_canvas.delete("all")
        
        # Draw rotating circle segments
        center_x, center_y = 20, 20
        radius = 15
        
        # Draw 12 segments that rotate (smoother animation)
        num_segments = 12
        for i in range(num_segments):
            angle = (self.spinner_angle + i * (360 / num_segments)) % 360
            
            # Calculate opacity (fade effect - trailing edge)
            opacity = max(0.1, 1.0 - (i / num_segments))
            
            # Convert to color (blue theme matching the app)
            # Blue color with varying opacity
            base_color = 0x3498db  # App blue color
            r = int(((base_color >> 16) & 0xFF) * opacity)
            g = int(((base_color >> 8) & 0xFF) * opacity)
            b = int((base_color & 0xFF) * opacity)
            
            # Ensure minimum visibility
            if r < 50:
                r = 50
            if g < 50:
                g = 50
            if b < 50:
                b = 50
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            # Draw arc segment
            self.spinner_canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=angle, extent=20,
                outline=color, width=3, style=tk.ARC
            )
        
        # Increment angle for rotation (smooth rotation)
        self.spinner_angle = (self.spinner_angle + 8) % 360
        
        # Schedule next animation frame (50ms = 20fps, smooth animation)
        if self.spinner_visible:
            self.root.after(50, self.animate_spinner)
    
    def show_spinner(self):
        """Show the loading spinner"""
        self.spinner_visible = True
        self.spinner_canvas.pack()
        self.animate_spinner()
    
    def hide_spinner(self):
        """Hide the loading spinner"""
        self.spinner_visible = False
        self.spinner_canvas.delete("all")
        self.spinner_canvas.pack_forget()
    
    def on_format_change(self, event=None):
        """Show/hide audio quality options based on format selection"""
        format_type = self.format_var.get()
        is_audio_format = format_type in ["mp3", "m4a", "wav", "flac"]
        
        if is_audio_format:
            # Show audio quality options
            self.audio_quality_label.grid()
            self.audio_quality_combo.grid()
            self.audio_quality_desc_label.grid()
            self.audio_info_label.grid()
            # Hide video quality options
            self.quality_label.grid_remove()
            self.quality_combo.grid_remove()
            self.quality_desc_label.grid_remove()
            
            # Update audio quality description
            audio_values = ["320", "256", "192", "128"]
            audio_labels = [
                "320 kbps - Best Quality (MP3 Maximum)",
                "256 kbps - High Quality",
                "192 kbps - Good Quality",
                "128 kbps - Standard Quality"
            ]
            if self.audio_quality_var.get() in audio_values:
                idx = audio_values.index(self.audio_quality_var.get())
                self.audio_quality_desc_label.config(text=audio_labels[idx])
        else:
            # Hide audio quality options
            self.audio_quality_label.grid_remove()
            self.audio_quality_combo.grid_remove()
            self.audio_quality_desc_label.grid_remove()
            self.audio_info_label.grid_remove()
            # Show video quality options
            self.quality_label.grid()
            self.quality_combo.grid()
            self.quality_desc_label.grid()
            
            # Update video quality description
            quality_values = ["best", "1080p", "720p", "480p", "360p", "240p", "worst"]
            quality_labels = [
                "Best Available (HD+)",
                "Full HD 1080p",
                "HD 720p",
                "SD 480p",
                "360p (Mobile)",
                "240p (Low)",
                "Lowest Quality"
            ]
            if self.quality_var.get() in quality_values:
                idx = quality_values.index(self.quality_var.get())
                self.quality_desc_label.config(text=quality_labels[idx])
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get(),
                                        title="Select Download Folder")
        if folder:
            self.download_path.set(folder)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clean_youtube_url(self, url):
        """Extract video ID from YouTube URL and return clean video-only URL"""
        # Remove playlist parameters and extract video ID
        video_id = None
        
        # Pattern for various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                break
        
        if video_id:
            # Return clean video URL without playlist parameters
            clean_url = f"https://www.youtube.com/watch?v={video_id}"
            if clean_url != url:
                self.log(f"Cleaned URL (removed playlist parameters)")
                self.log(f"Original: {url}")
                self.log(f"Clean: {clean_url}")
            return clean_url
        else:
            # If we can't extract video ID, try to remove playlist parameters
            parsed = urlparse(url)
            if parsed.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']:
                # Remove list parameter if present
                query_params = parse_qs(parsed.query)
                if 'list' in query_params:
                    query_params.pop('list')
                    # Reconstruct URL without list parameter
                    new_query = '&'.join([f"{k}={v[0]}" for k, v in query_params.items()])
                    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"
                    self.log(f"Removed playlist parameter from URL")
                    return clean_url
        
        # Return original URL if we can't clean it
        return url
    
    def check_ytdlp(self):
        """Check if yt-dlp is available - ONLY as module"""
        try:
            import yt_dlp
            version = yt_dlp.version.__version__
            self.log(f"✓ yt-dlp {version} ready")
            return True
        except ImportError:
            self.log("✗ Error: yt-dlp module not found!")
            messagebox.showerror("Missing Dependency",
                               "yt-dlp is not available. The installer may be corrupted.\n\nPlease reinstall the application.")
            return False
    
    def download_video(self):
        """Download the video using yt-dlp module directly - NO subprocess"""
        if self.is_downloading:
            return
        
        self.is_downloading = True
        self.download_btn.config(state="disabled", bg='#95a5a6')
        self.show_spinner()  # Show animated loading spinner
        self.status_label.config(text="Downloading...", fg='#3498db')
        self.log_text.delete(1.0, tk.END)
        
        try:
            # ALWAYS use yt_dlp module directly - no subprocess ever
            import yt_dlp
            from yt_dlp import YoutubeDL
            
            url = self.url.get().strip()
            if not url:
                raise ValueError("Please enter a YouTube URL")
            
            # Clean URL to extract video ID and remove playlist parameters
            clean_url = self.clean_youtube_url(url)
            
            download_path = self.download_path.get()
            os.makedirs(download_path, exist_ok=True)
            format_type = self.format_var.get()
            quality = self.quality_var.get()
            
            self.log(f"URL: {clean_url}")
            self.log(f"Format: {format_type}")
            if format_type in ["mp3", "m4a", "wav", "flac"]:
                audio_bitrate = self.audio_quality_var.get()
                self.log(f"Audio Bitrate: {audio_bitrate}kbps")
            else:
                self.log(f"Quality: {quality}")
            self.log(f"Save to: {download_path}\n")
            
            # Build yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'noplaylist': True,  # Force single video download, ignore playlists
                'extract_flat': False,  # Extract full video info (not just metadata)
            }
            
            # Set format
            if format_type == "mp3":
                # Get best audio source from YouTube, then convert to MP3
                ydl_opts['format'] = 'bestaudio/best'
                # Use selected bitrate (320, 256, 192, or 128 kbps)
                # FFmpegExtractAudio uses quality scale 0-9, but we can also try bitrate strings
                # Map bitrates: 320=0 (best), 256=2, 192=5, 128=7 (approximate)
                audio_bitrate = self.audio_quality_var.get()
                bitrate_map = {'320': '0', '256': '2', '192': '5', '128': '7'}
                quality_value = bitrate_map.get(audio_bitrate, '0')  # Default to best (320)
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality_value,  # Quality scale 0-9 (0 = best ~320kbps)
                }]
            elif format_type == "m4a":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            elif format_type == "wav":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }]
            elif format_type == "flac":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                }]
            elif format_type == "mp4":
                # Prefer H.264 (avc1) over AV1 for better compatibility and seekability
                # Exclude AV1 codec explicitly
                if quality == "best":
                    ydl_opts['format'] = 'bestvideo[vcodec!*=av01][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[vcodec!*=av01][ext=mp4]+bestaudio[ext=m4a]/best[vcodec!*=av01][ext=mp4]'
                else:
                    height = quality.replace('p', '')
                    ydl_opts['format'] = f'bestvideo[vcodec!*=av01][height<={height}][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[vcodec!*=av01][height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[vcodec!*=av01][height<={height}][ext=mp4]'
            elif format_type == "webm":
                # Prefer VP9 over AV1 for WebM (AV1 is not well supported)
                if quality == "best":
                    ydl_opts['format'] = 'bestvideo[vcodec!*=av01][ext=webm][vcodec^=vp9]+bestaudio[ext=webm]/bestvideo[vcodec!*=av01][ext=webm]+bestaudio[ext=webm]/best[vcodec!*=av01][ext=webm]'
                else:
                    height = quality.replace('p', '')
                    ydl_opts['format'] = f'bestvideo[vcodec!*=av01][height<={height}][ext=webm][vcodec^=vp9]+bestaudio[ext=webm]/bestvideo[vcodec!*=av01][height<={height}][ext=webm]+bestaudio[ext=webm]/best[vcodec!*=av01][height<={height}][ext=webm]'
            else:  # best
                # For "best" format, exclude AV1 and prefer H.264/VP9
                if quality == "best":
                    # Prefer MP4 with H.264, fallback to other non-AV1 formats
                    ydl_opts['format'] = 'bestvideo[vcodec!*=av01][ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/bestvideo[vcodec!*=av01][ext=webm][vcodec^=vp9]+bestaudio[ext=webm]/bestvideo[vcodec!*=av01]+bestaudio/best[vcodec!*=av01]'
                elif quality == "worst":
                    ydl_opts['format'] = 'worst[vcodec!*=av01]'
                else:
                    height = quality.replace('p', '')
                    # Exclude AV1, prefer H.264 for MP4
                    ydl_opts['format'] = f'bestvideo[vcodec!*=av01][height<={height}][ext=mp4][vcodec^=avc1]+bestaudio/bestvideo[vcodec!*=av01][height<={height}]+bestaudio/best[vcodec!*=av01][height<={height}]'
            
            # Progress hook
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d and d['total_bytes']:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        speed = d.get('speed', 0)
                        speed_mb = speed / (1024 * 1024) if speed else 0
                        self.log(f"[{percent:.1f}%] {speed_mb:.2f} MB/s")
                    elif '_percent_str' in d:
                        self.log(f"Downloading: {d['_percent_str']}")
                elif d['status'] == 'finished':
                    filename = os.path.basename(d.get('filename', 'file'))
                    self.log(f"✓ Finished: {filename}")
                elif d['status'] == 'error':
                    self.log(f"✗ Error: {d.get('error', 'Unknown error')}")
            
            ydl_opts['progress_hooks'] = [progress_hook]
            
            self.log("Starting download...\n")
            
            # Download using module directly - NO subprocess
            # Use cleaned URL to ensure single video download
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([clean_url])
            
            # Success
            self.hide_spinner()
            self.status_label.config(text="✓ Download Complete!", fg='#27ae60')
            messagebox.showinfo("Success", "Download completed successfully!")
            self.download_btn.config(state="normal", bg='#3498db')
            self.is_downloading = False
            
        except ValueError as e:
            self.hide_spinner()
            self.status_label.config(text="✗ Error", fg='#e74c3c')
            messagebox.showerror("Error", str(e))
            self.download_btn.config(state="normal", bg='#3498db')
            self.is_downloading = False
        except Exception as e:
            self.hide_spinner()
            self.status_label.config(text="✗ Download Failed", fg='#e74c3c')
            self.log(f"\n✗ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.download_btn.config(state="normal", bg='#3498db')
            self.is_downloading = False
    
    def start_download(self):
        """Start download in a separate thread"""
        if not self.url.get().strip():
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
