#!/usr/bin/env python3
"""
GIF Worker GUI - Professional PowerPoint GIF Studio

A unified GUI application combining MP4-to-GIF conversion and GIF looping functionality.
Perfect for creating professional, continuously looping GIFs for PowerPoint presentations.

Features:
    - Convert single or multiple MP4 videos to looping GIFs
    - Make existing GIFs loop infinitely
    - Drag & drop file support
    - Quality presets and customization options
    - Beautiful, intuitive interface

Requirements:
    pip install moviepy Pillow
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.font import Font
import threading
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips
from PIL import Image
import glob


# ═══════════════════════════════════════════════════════════════════════════
#                       CORE FUNCTIONALITY (PRESERVED)
# ═══════════════════════════════════════════════════════════════════════════

def convert_mp4_to_gif(input_paths, output_path=None, fps=10, width=None, quality='medium', 
                       progress_callback=None):
    """
    Convert one or more MP4 videos to a continuously looping GIF.
    
    Args:
        input_paths (list): List of paths to input MP4 files
        output_path (str): Path for output GIF file (optional)
        fps (int): Frames per second for the GIF (default: 10)
        width (int): Width in pixels (height auto-calculated, optional)
        quality (str): Quality preset ('low', 'medium', 'high')
        progress_callback (callable): Function to call with progress updates
    
    Returns:
        str: Path to the output file
    """
    def log(msg):
        if progress_callback:
            progress_callback(msg)
    
    # Validate input files
    valid_paths = []
    for path in input_paths:
        if not os.path.exists(path):
            log(f"⚠️  Warning: File not found, skipping: {path}")
            continue
        if not path.lower().endswith('.mp4'):
            log(f"⚠️  Warning: Not an MP4 file, skipping: {path}")
            continue
        valid_paths.append(path)
    
    if not valid_paths:
        raise FileNotFoundError("No valid MP4 files found")
    
    # Generate output filename if not provided
    if output_path is None:
        if len(valid_paths) == 1:
            base_name = os.path.splitext(valid_paths[0])[0]
            output_path = f"{base_name}.gif"
        else:
            first_dir = os.path.dirname(valid_paths[0])
            output_path = os.path.join(first_dir, "combined_video.gif")
    
    # Quality presets
    quality_settings = {
        'low': {'fps': 8, 'resize_factor': 0.5},
        'medium': {'fps': 10, 'resize_factor': 0.7},
        'high': {'fps': 15, 'resize_factor': 1.0}
    }
    
    if quality in quality_settings:
        settings = quality_settings[quality]
        if fps == 10:  # Only override if using default
            fps = settings['fps']
        resize_factor = settings['resize_factor']
    else:
        resize_factor = 0.7
    
    try:
        video_clips = []
        total_duration = 0
        
        log(f"\n📹 Loading {len(valid_paths)} video file(s):")
        
        # Load all video clips
        for i, path in enumerate(valid_paths, 1):
            log(f"  {i}. {os.path.basename(path)}")
            clip = VideoFileClip(path)
            
            duration = clip.duration
            original_fps = clip.fps
            original_size = clip.size
            total_duration += duration
            
            log(f"     Duration: {duration:.1f}s, FPS: {original_fps:.1f}, Size: {original_size[0]}x{original_size[1]}")
            
            # Calculate target dimensions
            if i == 1:
                if width:
                    new_width = width
                    new_height = int((width / original_size[0]) * original_size[1])
                else:
                    new_width = int(original_size[0] * resize_factor)
                    new_height = int(original_size[1] * resize_factor)
                
                # Ensure dimensions are even
                new_width = new_width if new_width % 2 == 0 else new_width - 1
                new_height = new_height if new_height % 2 == 0 else new_height - 1
                target_size = (new_width, new_height)
                
                log(f"\n  📐 Target size: {new_width}x{new_height}")
                log(f"  🎬 Target FPS: {fps}")
                log(f"  💡 Quality preset: {quality}")
            
            # Resize to match target dimensions
            if original_size != target_size:
                clip_resized = clip.resized(target_size)
                video_clips.append(clip_resized)
            else:
                video_clips.append(clip)
        
        log(f"\n📊 Total duration: {total_duration:.1f} seconds")
        
        # Concatenate videos if multiple files
        if len(video_clips) == 1:
            final_video = video_clips[0]
            log(f"\n🔄 Converting single video to GIF...")
        else:
            log(f"\n🔗 Stitching {len(video_clips)} videos together...")
            final_video = concatenate_videoclips(video_clips, method="compose")
            log(f"🔄 Converting combined video to GIF...")
        
        # Convert to GIF with infinite loop
        final_video.write_gif(
            output_path,
            fps=fps,
            loop=0
        )
        
        # Clean up
        for clip in video_clips:
            clip.close()
        if len(video_clips) > 1:
            final_video.close()
        
        # Get output file info
        output_size = os.path.getsize(output_path)
        
        log(f"\n✅ Successfully created looping GIF!")
        log(f"  • Output: {os.path.basename(output_path)}")
        log(f"  • Videos combined: {len(valid_paths)}")
        log(f"  • Duration: {total_duration:.1f} seconds")
        log(f"  • File size: {output_size/1024/1024:.1f} MB")
        log(f"  • Ready for PowerPoint! 🎉")
        
        if output_size / 1024 / 1024 > 10:
            log(f"\n💡 Tip: File is large. Try 'low' quality or smaller width for PowerPoint.")
        
        return output_path
        
    except Exception as e:
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass
        raise Exception(f"Error converting MP4(s) to GIF: {str(e)}")


def make_gif_loop(input_path, output_path=None, progress_callback=None):
    """
    Convert a GIF to loop continuously.
    
    Args:
        input_path (str): Path to input GIF file
        output_path (str): Path for output GIF file (optional)
        progress_callback (callable): Function to call with progress updates
    
    Returns:
        str: Path to the output file
    """
    def log(msg):
        if progress_callback:
            progress_callback(msg)
    
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_looped.gif"
    
    try:
        log(f"🔄 Processing: {os.path.basename(input_path)}")
        
        with Image.open(input_path) as img:
            if img.format != 'GIF':
                log(f"⚠️  Warning: Input is {img.format}, not GIF. Converting anyway...")
            
            frames = []
            durations = []
            
            try:
                while True:
                    frame = img.copy()
                    frames.append(frame)
                    duration = img.info.get('duration', 100)
                    durations.append(duration)
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
            
            if frames:
                log("💾 Saving with infinite loop...")
                frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=0,
                    optimize=True
                )
                
                output_size = os.path.getsize(output_path)
                
                log(f"\n✅ Successfully created looping GIF!")
                log(f"  • Output: {os.path.basename(output_path)}")
                log(f"  • Frames: {len(frames)}")
                log(f"  • Avg duration: {sum(durations)/len(durations):.1f}ms per frame")
                log(f"  • File size: {output_size/1024/1024:.2f} MB")
                log(f"  • Ready for PowerPoint! 🎉")
                
                return output_path
            else:
                raise ValueError("No frames found in the input file")
                
    except Exception as e:
        raise Exception(f"Error processing GIF: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════
#                              GUI APPLICATION
# ═══════════════════════════════════════════════════════════════════════════

class GIFWorkerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 GIF Worker - PowerPoint GIF Studio")
        self.root.geometry("900x750")
        self.root.minsize(800, 600)
        
        # Set icon if available
        try:
            # You can add an icon file later
            pass
        except:
            pass
        
        # Color scheme - Professional blue theme
        self.colors = {
            'bg': '#f0f4f8',
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#cbd5e1',
            'white': '#ffffff'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Fonts
        self.font_title = Font(family="Segoe UI", size=20, weight="bold")
        self.font_subtitle = Font(family="Segoe UI", size=11)
        self.font_normal = Font(family="Segoe UI", size=10)
        self.font_small = Font(family="Segoe UI", size=9)
        
        # File lists
        self.mp4_files = []
        self.gif_file = None
        self.batch_files = []  # Store full paths for batch processing
        
        self.create_widgets()
        self.setup_drag_drop()
        
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # ═══════════════════════════════════════════════════════════════
        #                         HEADER
        # ═══════════════════════════════════════════════════════════════
        
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎬 GIF Worker",
            font=self.font_title,
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Professional PowerPoint GIF Studio",
            font=self.font_subtitle,
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        subtitle_label.pack()
        
        # ═══════════════════════════════════════════════════════════════
        #                         NOTEBOOK TABS
        # ═══════════════════════════════════════════════════════════════
        
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Style for notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=self.font_normal)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.mp4_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.gif_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.batch_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        
        self.notebook.add(self.mp4_tab, text="  🎬 MP4 to GIF  ")
        self.notebook.add(self.gif_tab, text="  🔁 Loop GIF  ")
        self.notebook.add(self.batch_tab, text="  📦 Batch Process  ")
        
        # Populate tabs
        self.create_mp4_tab()
        self.create_gif_tab()
        self.create_batch_tab()
        
        # ═══════════════════════════════════════════════════════════════
        #                         STATUS BAR
        # ═══════════════════════════════════════════════════════════════
        
        status_frame = tk.Frame(self.root, bg=self.colors['secondary'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready to create amazing GIFs for PowerPoint! 🎉",
            font=self.font_small,
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X)
        
    def create_mp4_tab(self):
        """Create the MP4 to GIF conversion tab."""
        
        # Info panel
        info_frame = tk.Frame(self.mp4_tab, bg=self.colors['white'])
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Convert single or multiple MP4 videos into a continuously looping GIF.\n"
                 "Perfect for PowerPoint presentations!",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text_light'],
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
        
        # File selection
        file_frame = tk.LabelFrame(
            self.mp4_tab,
            text="  Select MP4 Files  ",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # File list
        list_frame = tk.Frame(file_frame, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.mp4_listbox = tk.Listbox(
            list_frame,
            font=self.font_normal,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            bg=self.colors['bg'],
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.mp4_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.mp4_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(file_frame, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_button(
            btn_frame, "Add Files", self.add_mp4_files, "primary"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.create_button(
            btn_frame, "Clear All", self.clear_mp4_files, "secondary"
        ).pack(side=tk.LEFT)
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            self.mp4_tab,
            text="  Settings  ",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Quality preset
        quality_row = tk.Frame(settings_frame, bg=self.colors['white'])
        quality_row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            quality_row,
            text="Quality Preset:",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.mp4_quality_var = tk.StringVar(value="medium")
        quality_combo = ttk.Combobox(
            quality_row,
            textvariable=self.mp4_quality_var,
            values=["low", "medium", "high"],
            state="readonly",
            font=self.font_normal,
            width=20
        )
        quality_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            quality_row,
            text="💡 medium = balanced quality",
            font=self.font_small,
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=10)
        
        # FPS
        fps_row = tk.Frame(settings_frame, bg=self.colors['white'])
        fps_row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            fps_row,
            text="FPS (optional):",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.mp4_fps_var = tk.StringVar()
        fps_entry = tk.Entry(
            fps_row,
            textvariable=self.mp4_fps_var,
            font=self.font_normal,
            width=22,
            relief=tk.SOLID,
            borderwidth=1
        )
        fps_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            fps_row,
            text="💡 Leave empty to use quality preset",
            font=self.font_small,
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=10)
        
        # Width
        width_row = tk.Frame(settings_frame, bg=self.colors['white'])
        width_row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            width_row,
            text="Width (optional):",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            width=15,
            anchor=tk.W
        ).pack(side=tk.LEFT)
        
        self.mp4_width_var = tk.StringVar()
        width_entry = tk.Entry(
            width_row,
            textvariable=self.mp4_width_var,
            font=self.font_normal,
            width=22,
            relief=tk.SOLID,
            borderwidth=1
        )
        width_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            width_row,
            text="💡 Pixels (height auto-calculated)",
            font=self.font_small,
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=10)
        
        # Convert button
        convert_frame = tk.Frame(self.mp4_tab, bg=self.colors['white'])
        convert_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.create_button(
            convert_frame, "🎬 Convert to GIF", self.convert_mp4, "success", large=True
        ).pack(anchor=tk.CENTER)
        
    def create_gif_tab(self):
        """Create the GIF looping tab."""
        
        # Info panel
        info_frame = tk.Frame(self.gif_tab, bg=self.colors['white'])
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Make any GIF loop infinitely.\n"
                 "Perfect for ensuring smooth playback in PowerPoint!",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text_light'],
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
        
        # File selection
        file_frame = tk.LabelFrame(
            self.gif_tab,
            text="  Select GIF File  ",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Selected file display
        self.gif_file_label = tk.Label(
            file_frame,
            text="No file selected",
            font=self.font_normal,
            bg=self.colors['bg'],
            fg=self.colors['text_light'],
            relief=tk.FLAT,
            borderwidth=1,
            padx=15,
            pady=40,
            anchor=tk.CENTER
        )
        self.gif_file_label.pack(fill=tk.BOTH, expand=True)
        
        # Button
        btn_frame = tk.Frame(file_frame, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_button(
            btn_frame, "Select GIF File", self.select_gif_file, "primary"
        ).pack(anchor=tk.CENTER)
        
        # Convert button
        convert_frame = tk.Frame(self.gif_tab, bg=self.colors['white'])
        convert_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.create_button(
            convert_frame, "🔁 Make Loop Infinitely", self.loop_gif, "success", large=True
        ).pack(anchor=tk.CENTER)
        
    def create_batch_tab(self):
        """Create the batch processing tab."""
        
        # Info panel
        info_frame = tk.Frame(self.batch_tab, bg=self.colors['white'])
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        info_text = tk.Label(
            info_frame,
            text="💡 Process multiple files at once!\n"
                 "Great for converting entire folders of videos or GIFs.",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text_light'],
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W)
        
        # Mode selection
        mode_frame = tk.LabelFrame(
            self.batch_tab,
            text="  Processing Mode  ",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        mode_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.batch_mode_var = tk.StringVar(value="mp4")
        
        tk.Radiobutton(
            mode_frame,
            text="Convert MP4s to GIFs",
            variable=self.batch_mode_var,
            value="mp4",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            selectcolor=self.colors['bg']
        ).pack(anchor=tk.W, pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="Make GIFs loop infinitely",
            variable=self.batch_mode_var,
            value="gif",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            selectcolor=self.colors['bg']
        ).pack(anchor=tk.W, pady=5)
        
        # File list
        file_frame = tk.LabelFrame(
            self.batch_tab,
            text="  Files to Process  ",
            font=self.font_normal,
            bg=self.colors['white'],
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        list_frame = tk.Frame(file_frame, bg=self.colors['white'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.batch_listbox = tk.Listbox(
            list_frame,
            font=self.font_normal,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            bg=self.colors['bg'],
            relief=tk.FLAT,
            borderwidth=1
        )
        self.batch_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.batch_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(file_frame, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_button(
            btn_frame, "Add Files", self.add_batch_files, "primary"
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        self.create_button(
            btn_frame, "Clear All", self.clear_batch_files, "secondary"
        ).pack(side=tk.LEFT)
        
        # Process button
        process_frame = tk.Frame(self.batch_tab, bg=self.colors['white'])
        process_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.create_button(
            process_frame, "📦 Process All Files", self.process_batch, "success", large=True
        ).pack(anchor=tk.CENTER)
        
    def create_button(self, parent, text, command, style="primary", large=False):
        """Create a styled button."""
        
        colors = {
            'primary': (self.colors['primary'], self.colors['white']),
            'secondary': (self.colors['secondary'], self.colors['white']),
            'success': (self.colors['success'], self.colors['white']),
            'warning': (self.colors['warning'], self.colors['white'])
        }
        
        bg, fg = colors.get(style, colors['primary'])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=Font(family="Segoe UI", size=11 if large else 10, weight="bold" if large else "normal"),
            bg=bg,
            fg=fg,
            relief=tk.FLAT,
            borderwidth=0,
            padx=30 if large else 20,
            pady=12 if large else 8,
            cursor="hand2"
        )
        
        # Hover effects
        def on_enter(e):
            btn['bg'] = self._lighten_color(bg)
        
        def on_leave(e):
            btn['bg'] = bg
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color by 10%."""
        # Simple lightening - just for hover effect
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * 1.1)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
    def setup_drag_drop(self):
        """Set up drag and drop support (basic implementation)."""
        # Note: Full drag-drop support would require tkinterdnd2
        # This is a placeholder for future enhancement
        pass
    
    # ═══════════════════════════════════════════════════════════════════
    #                         MP4 TAB FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def add_mp4_files(self):
        """Add MP4 files to the list."""
        files = filedialog.askopenfilenames(
            title="Select MP4 Files",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.mp4_files:
                self.mp4_files.append(file)
                self.mp4_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"Added {len(files)} file(s)")
    
    def clear_mp4_files(self):
        """Clear all MP4 files from the list."""
        self.mp4_files.clear()
        self.mp4_listbox.delete(0, tk.END)
        self.update_status("Cleared file list")
    
    def convert_mp4(self):
        """Convert MP4(s) to GIF."""
        if not self.mp4_files:
            messagebox.showwarning("No Files", "Please add at least one MP4 file.")
            return
        
        # Get output path
        output_path = filedialog.asksaveasfilename(
            title="Save GIF As",
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        # Get settings
        quality = self.mp4_quality_var.get()
        fps = int(self.mp4_fps_var.get()) if self.mp4_fps_var.get() else 10
        width = int(self.mp4_width_var.get()) if self.mp4_width_var.get() else None
        
        # Show progress window
        self.show_progress_window(
            "Converting MP4 to GIF",
            lambda progress_callback: convert_mp4_to_gif(
                self.mp4_files,
                output_path,
                fps=fps,
                width=width,
                quality=quality,
                progress_callback=progress_callback
            )
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                         GIF TAB FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def select_gif_file(self):
        """Select a GIF file."""
        file = filedialog.askopenfilename(
            title="Select GIF File",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        if file:
            self.gif_file = file
            self.gif_file_label.config(
                text=f"Selected: {os.path.basename(file)}",
                fg=self.colors['success']
            )
            self.update_status(f"Selected: {os.path.basename(file)}")
    
    def loop_gif(self):
        """Make GIF loop infinitely."""
        if not self.gif_file:
            messagebox.showwarning("No File", "Please select a GIF file.")
            return
        
        # Get output path
        default_name = os.path.splitext(os.path.basename(self.gif_file))[0] + "_looped.gif"
        output_path = filedialog.asksaveasfilename(
            title="Save Looped GIF As",
            initialfile=default_name,
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
        
        # Show progress window
        self.show_progress_window(
            "Making GIF Loop",
            lambda progress_callback: make_gif_loop(
                self.gif_file,
                output_path,
                progress_callback=progress_callback
            )
        )
    
    # ═══════════════════════════════════════════════════════════════════
    #                         BATCH TAB FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def add_batch_files(self):
        """Add files for batch processing."""
        mode = self.batch_mode_var.get()
        
        if mode == "mp4":
            filetypes = [("MP4 files", "*.mp4"), ("All files", "*.*")]
        else:
            filetypes = [("GIF files", "*.gif"), ("All files", "*.*")]
        
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=filetypes
        )
        
        for file in files:
            self.batch_files.append(file)  # Store full path
            self.batch_listbox.insert(tk.END, os.path.basename(file))
        
        self.update_status(f"Added {len(files)} file(s) for batch processing")
    
    def clear_batch_files(self):
        """Clear batch file list."""
        self.batch_files.clear()  # Clear full paths
        self.batch_listbox.delete(0, tk.END)
        self.update_status("Cleared batch file list")
    
    def process_batch(self):
        """Process all files in batch."""
        if not self.batch_files:
            messagebox.showwarning("No Files", "Please add files to process.")
            return
        
        mode = self.batch_mode_var.get()
        quality = self.mp4_quality_var.get() if mode == "mp4" else None
        
        # Create progress window for batch processing
        def batch_process(progress_callback):
            success = 0
            failed = 0
            
            for i, filepath in enumerate(self.batch_files, 1):
                filename = os.path.basename(filepath)
                progress_callback(f"\n{'─'*50}")
                progress_callback(f"[{i}/{len(self.batch_files)}] {filename}")
                progress_callback(f"{'─'*50}")
                
                try:
                    if mode == "mp4":
                        # Auto-generate output name
                        base_name = os.path.splitext(filepath)[0]
                        output_path = f"{base_name}.gif"
                        
                        convert_mp4_to_gif(
                            [filepath],
                            output_path,
                            fps=10,
                            width=None,
                            quality=quality,
                            progress_callback=progress_callback
                        )
                    else:  # gif mode
                        # Auto-generate output name
                        base_name = os.path.splitext(filepath)[0]
                        output_path = f"{base_name}_looped.gif"
                        
                        make_gif_loop(
                            filepath,
                            output_path,
                            progress_callback=progress_callback
                        )
                    
                    success += 1
                except Exception as e:
                    progress_callback(f"❌ Error: {str(e)}")
                    failed += 1
            
            progress_callback(f"\n{'═'*50}")
            progress_callback(f"📊 Batch Complete!")
            progress_callback(f"   • Successful: {success}")
            progress_callback(f"   • Failed: {failed}")
            progress_callback(f"{'═'*50}")
            
            return f"Processed {success + failed} files"
        
        self.show_progress_window("Batch Processing", batch_process)
    
    # ═══════════════════════════════════════════════════════════════════
    #                         UTILITY FUNCTIONS
    # ═══════════════════════════════════════════════════════════════════
    
    def update_status(self, message):
        """Update the status bar."""
        self.status_label.config(text=message)
    
    def show_progress_window(self, title, task_function):
        """Show a progress window while processing."""
        
        # Create progress window
        progress_win = tk.Toplevel(self.root)
        progress_win.title(title)
        progress_win.geometry("600x400")
        progress_win.transient(self.root)
        progress_win.grab_set()
        
        # Progress text
        text_frame = tk.Frame(progress_win, bg=self.colors['white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        progress_text = scrolledtext.ScrolledText(
            text_frame,
            font=self.font_small,
            wrap=tk.WORD,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        progress_text.pack(fill=tk.BOTH, expand=True)
        
        # Close button (initially disabled)
        close_btn = self.create_button(
            progress_win, "Close", progress_win.destroy, "secondary"
        )
        close_btn.pack(pady=10)
        close_btn.config(state=tk.DISABLED)
        
        def log_progress(message):
            """Add message to progress window."""
            progress_text.insert(tk.END, message + "\n")
            progress_text.see(tk.END)
            progress_text.update()
        
        def run_task():
            """Run the task in a thread."""
            try:
                result = task_function(log_progress)
                log_progress("\n" + "═" * 50)
                log_progress("✅ Task completed successfully!")
                messagebox.showinfo("Success", f"Operation completed!\nOutput: {os.path.basename(result)}")
            except Exception as e:
                log_progress(f"\n❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Operation failed:\n{str(e)}")
            finally:
                close_btn.config(state=tk.NORMAL)
        
        # Start task in thread
        thread = threading.Thread(target=run_task, daemon=True)
        thread.start()


# ═══════════════════════════════════════════════════════════════════════════
#                              MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = GIFWorkerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
