#!/usr/bin/env python3
"""
GIF Worker - Professional PowerPoint GIF Studio

A unified tool combining MP4-to-GIF conversion and GIF looping functionality.
Perfect for creating professional, continuously looping GIFs for PowerPoint presentations.

Features:
    - Convert single or multiple MP4 videos to looping GIFs
    - Make existing GIFs loop infinitely
    - Batch process multiple files
    - Interactive menu or command-line interface
    - Quality presets and customization options

Usage:
    Interactive Mode:
        python gif_worker.py
    
    MP4 to GIF Mode:
        python gif_worker.py --mp4 video.mp4
        python gif_worker.py --mp4 video1.mp4 video2.mp4 --output combined.gif
        python gif_worker.py --mp4 *.mp4 --quality high --fps 15
    
    GIF Looping Mode:
        python gif_worker.py --loop animation.gif
        python gif_worker.py --loop input.gif --output looped.gif
    
    Batch Mode:
        python gif_worker.py --batch *.gif --loop
        python gif_worker.py --batch *.mp4 --mp4 --quality low

Requirements:
    pip install moviepy Pillow
"""

import sys
import os
from moviepy import VideoFileClip, concatenate_videoclips
from PIL import Image
import argparse
import glob
import time


# ═══════════════════════════════════════════════════════════════════════════
#                           VISUAL ELEMENTS & UI
# ═══════════════════════════════════════════════════════════════════════════

def display_banner():
    """Display the application banner with visual styling."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           🎬 GIF WORKER - PowerPoint GIF Studio 🎬           ║
║                     Professional GIF Tools                    ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_menu():
    """Display the interactive main menu."""
    menu = """
╔══════════════════════════════════════════════════════════════╗
║                         MAIN MENU                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1️⃣  Convert MP4(s) to Looping GIF                          ║
║     💡 Tip: Combine multiple videos into one GIF            ║
║                                                              ║
║  2️⃣  Make Existing GIF Loop Infinitely                      ║
║     💡 Tip: Perfect for PowerPoint presentations            ║
║                                                              ║
║  3️⃣  Batch Process Files                                    ║
║     💡 Tip: Process multiple files at once                  ║
║                                                              ║
║  4️⃣  Help & Examples                                        ║
║     ℹ️  Learn more about features and usage                 ║
║                                                              ║
║  5️⃣  Exit                                                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(menu)


def display_help():
    """Display comprehensive help and examples."""
    help_text = """
╔══════════════════════════════════════════════════════════════╗
║                      HELP & EXAMPLES                         ║
╚══════════════════════════════════════════════════════════════╝

📋 COMMAND-LINE EXAMPLES:
   
   MP4 to GIF Conversion:
   ─────────────────────────────────────────────────────────────
   • Single file:
     python gif_worker.py --mp4 video.mp4
   
   • Multiple files (stitched together):
     python gif_worker.py --mp4 part1.mp4 part2.mp4 part3.mp4 -o combined.gif
   
   • All MP4s in folder:
     python gif_worker.py --mp4 *.mp4 --quality high
   
   • Custom settings:
     python gif_worker.py --mp4 video.mp4 --fps 15 --width 800 --quality high
   
   GIF Looping:
   ─────────────────────────────────────────────────────────────
   • Make GIF loop infinitely:
     python gif_worker.py --loop animation.gif
   
   • Specify output name:
     python gif_worker.py --loop input.gif -o output_looped.gif
   
   Batch Processing:
   ─────────────────────────────────────────────────────────────
   • Loop all GIFs in folder:
     python gif_worker.py --batch *.gif --loop
   
   • Convert all MP4s to GIFs:
     python gif_worker.py --batch *.mp4 --mp4 --quality medium

⚙️  QUALITY PRESETS:
   ─────────────────────────────────────────────────────────────
   • low    → 8 fps, 50% size  (smallest files)
   • medium → 10 fps, 70% size (balanced, default)
   • high   → 15 fps, 100% size (best quality, larger files)

💡 TIPS FOR POWERPOINT:
   ─────────────────────────────────────────────────────────────
   • Keep file sizes under 10MB for smooth playback
   • Use 'medium' quality for most presentations
   • Width of 400-600px works well for slide elements
   • All GIFs created loop infinitely (perfect for slides!)

🎯 BEST PRACTICES:
   ─────────────────────────────────────────────────────────────
   • Test your GIF in PowerPoint before the presentation
   • Use consistent dimensions when combining multiple MP4s
   • Lower quality settings for email/web sharing
   • Higher quality for local presentations

Press Enter to return to main menu...
    """
    print(help_text)
    input()


def print_section_header(title):
    """Print a formatted section header."""
    print(f"\n{'─' * 62}")
    print(f"  {title}")
    print(f"{'─' * 62}")


def print_success(message):
    """Print a success message with visual styling."""
    print(f"\n✅ {message}")


def print_error(message):
    """Print an error message with visual styling."""
    print(f"\n❌ {message}")


def print_warning(message):
    """Print a warning message with visual styling."""
    print(f"\n⚠️  {message}")


def print_info(message):
    """Print an info message with visual styling."""
    print(f"\nℹ️  {message}")


def print_tip(message):
    """Print a tip message with visual styling."""
    print(f"\n💡 Tip: {message}")


def print_progress(message):
    """Print a progress message with visual styling."""
    print(f"🔄 {message}")


# ═══════════════════════════════════════════════════════════════════════════
#                       CORE FUNCTIONALITY - MP4 TO GIF
# ═══════════════════════════════════════════════════════════════════════════

def convert_mp4_to_gif(input_paths, output_path=None, fps=10, width=None, quality='medium'):
    """
    Convert one or more MP4 videos to a continuously looping GIF.
    
    ℹ️  This function preserves all original functionality from gif_creator.py
    
    Args:
        input_paths (list): List of paths to input MP4 files
        output_path (str): Path for output GIF file (optional)
        fps (int): Frames per second for the GIF (default: 10)
        width (int): Width in pixels (height auto-calculated, optional)
        quality (str): Quality preset ('low', 'medium', 'high')
    
    Returns:
        str: Path to the output file
    
    💡 Tip: Use quality presets for quick optimization:
        - 'low' for smallest files
        - 'medium' for balanced quality (default)
        - 'high' for best quality
    """
    # Validate input files
    valid_paths = []
    for path in input_paths:
        if not os.path.exists(path):
            print_warning(f"File not found, skipping: {path}")
            continue
        if not path.lower().endswith('.mp4'):
            print_warning(f"Not an MP4 file, skipping: {path}")
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
            # Use first file's directory and create a combined name
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
        resize_factor = 0.7  # Default
    
    try:
        video_clips = []
        total_duration = 0
        
        print(f"\n📹 Loading {len(valid_paths)} video file(s):")
        
        # Load all video clips
        for i, path in enumerate(valid_paths, 1):
            print(f"  {i}. {os.path.basename(path)}")
            clip = VideoFileClip(path)
            
            duration = clip.duration
            original_fps = clip.fps
            original_size = clip.size
            total_duration += duration
            
            print(f"     ⚙️  Duration: {duration:.1f}s, FPS: {original_fps:.1f}, Size: {original_size[0]}x{original_size[1]}")
            
            # Calculate target dimensions (use first video as reference)
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
                
                print(f"\n  📐 Target size for all videos: {new_width}x{new_height}")
                print(f"  🎬 Target FPS: {fps}")
                print_tip(f"Using '{quality}' quality preset")
            
            # Resize to match target dimensions
            if original_size != target_size:
                clip_resized = clip.resized(target_size)
                video_clips.append(clip_resized)
            else:
                video_clips.append(clip)
        
        print(f"\n📊 Total duration: {total_duration:.1f} seconds")
        
        # Concatenate videos if multiple files
        if len(video_clips) == 1:
            final_video = video_clips[0]
            print_progress("Converting single video to GIF...")
        else:
            print_progress(f"Stitching {len(video_clips)} videos together...")
            final_video = concatenate_videoclips(video_clips, method="compose")
            print_progress("Converting combined video to GIF...")
        
        # Convert to GIF with infinite loop
        final_video.write_gif(
            output_path,
            fps=fps,
            loop=0  # 0 = infinite loop
        )
        
        # Clean up
        for clip in video_clips:
            clip.close()
        if len(video_clips) > 1:
            final_video.close()
        
        # Get output file info
        output_size = os.path.getsize(output_path)
        
        print_success(f"Successfully created looping GIF: {output_path}")
        print(f"  • Videos combined: {len(valid_paths)}")
        print(f"  • Total duration: {total_duration:.1f} seconds")
        print(f"  • File size: {output_size:,} bytes ({output_size/1024/1024:.1f} MB)")
        print(f"  • Ready for PowerPoint! 🎉")
        
        # Provide optimization tips
        file_size_mb = output_size / 1024 / 1024
        if file_size_mb > 10:
            print_tip(f"File is {file_size_mb:.1f}MB. For smaller files, try:")
            print(f"      • Use --quality low")
            print(f"      • Use --width 400 (or smaller)")
            print(f"      • Reduce --fps to 8")
        
        return output_path
        
    except Exception as e:
        # Clean up on error
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass
        raise Exception(f"Error converting MP4(s) to GIF: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════
#                       CORE FUNCTIONALITY - GIF LOOPING
# ═══════════════════════════════════════════════════════════════════════════

def make_gif_loop(input_path, output_path=None):
    """
    Convert a GIF to loop continuously.
    
    ℹ️  This function preserves all original functionality from gif_looper.py
    
    Args:
        input_path (str): Path to input GIF file
        output_path (str): Path for output GIF file (optional)
    
    Returns:
        str: Path to the output file
    
    💡 Tip: The output GIF will loop infinitely in PowerPoint presentations
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Generate output filename if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_looped.gif"
    
    try:
        print_progress(f"Processing: {os.path.basename(input_path)}")
        
        # Open the GIF
        with Image.open(input_path) as img:
            # Check if it's actually a GIF
            if img.format != 'GIF':
                print_warning(f"Input file is {img.format}, not GIF. Converting anyway...")
            
            # Get all frames
            frames = []
            durations = []
            
            try:
                while True:
                    # Copy the frame
                    frame = img.copy()
                    frames.append(frame)
                    
                    # Get frame duration (default to 100ms if not available)
                    duration = img.info.get('duration', 100)
                    durations.append(duration)
                    
                    # Move to next frame
                    img.seek(img.tell() + 1)
            except EOFError:
                # End of frames
                pass
            
            # Save with infinite loop
            if frames:
                print_progress("Saving with infinite loop...")
                frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=0,  # 0 = infinite loop
                    optimize=True
                )
                
                output_size = os.path.getsize(output_path)
                
                print_success(f"Successfully created looping GIF: {output_path}")
                print(f"  • Frames: {len(frames)}")
                print(f"  • Average duration: {sum(durations)/len(durations):.1f}ms per frame")
                print(f"  • File size: {output_size:,} bytes ({output_size/1024/1024:.2f} MB)")
                print(f"  • Ready for PowerPoint! 🎉")
                
                return output_path
            else:
                raise ValueError("No frames found in the input file")
                
    except Exception as e:
        raise Exception(f"Error processing GIF: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════
#                          INTERACTIVE MODE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_file_paths(prompt="Enter file path(s)", allow_multiple=True):
    """
    Get file path(s) from user input with validation.
    
    Args:
        prompt (str): Prompt message to display
        allow_multiple (bool): Allow multiple files to be entered
    
    Returns:
        list: List of validated file paths
    """
    if allow_multiple:
        print(f"\n{prompt}")
        print("💡 Tip: Enter one path per line. Press Enter twice when done.")
        print("💡 Tip: You can drag & drop files into this window (in some terminals)")
        print("💡 Tip: Use wildcards like *.mp4 to match multiple files")
    else:
        print(f"\n{prompt}")
        print("💡 Tip: You can drag & drop a file into this window (in some terminals)")
    
    paths = []
    while True:
        path = input("   Path: ").strip().strip('"').strip("'")
        
        if not path:
            if paths or not allow_multiple:
                break
            else:
                print("   ⚠️  Please enter at least one file path")
                continue
        
        # Expand wildcards
        if '*' in path or '?' in path:
            matches = glob.glob(path)
            if matches:
                paths.extend(matches)
                print(f"   ✓ Found {len(matches)} file(s) matching pattern")
            else:
                print(f"   ⚠️  No files match pattern: {path}")
        else:
            paths.append(path)
            print(f"   ✓ Added: {os.path.basename(path)}")
        
        if not allow_multiple:
            break
    
    return paths


def get_quality_preset():
    """
    Get quality preset from user.
    
    Returns:
        str: Quality preset ('low', 'medium', 'high')
    """
    print("\n⚙️  Select quality preset:")
    print("   1. Low    (8 fps, 50% size - smallest files)")
    print("   2. Medium (10 fps, 70% size - balanced) [DEFAULT]")
    print("   3. High   (15 fps, 100% size - best quality)")
    
    choice = input("\n   Choice (1-3) or press Enter for default: ").strip()
    
    quality_map = {
        '1': 'low',
        '2': 'medium',
        '3': 'high',
        '': 'medium'
    }
    
    return quality_map.get(choice, 'medium')


def get_custom_settings():
    """
    Get custom FPS and width settings from user.
    
    Returns:
        tuple: (fps, width) or (None, None) for defaults
    """
    print("\n⚙️  Custom settings (optional - press Enter to use defaults):")
    
    fps_input = input("   FPS (frames per second): ").strip()
    fps = int(fps_input) if fps_input else None
    
    width_input = input("   Width in pixels: ").strip()
    width = int(width_input) if width_input else None
    
    if fps or width:
        print(f"   ✓ Custom settings applied")
    else:
        print(f"   ℹ️  Using quality preset defaults")
    
    return fps, width


def interactive_mp4_to_gif():
    """Interactive mode for converting MP4(s) to GIF."""
    print_section_header("🎬 Convert MP4(s) to Looping GIF")
    
    # Get input files
    input_paths = get_file_paths("Enter MP4 file path(s)", allow_multiple=True)
    
    if not input_paths:
        print_warning("No files provided. Returning to menu.")
        return
    
    # Get output path
    print("\n📁 Output file (optional - press Enter for automatic naming):")
    output_path = input("   Output path: ").strip().strip('"').strip("'")
    if not output_path:
        output_path = None
        print("   ℹ️  Will use automatic naming")
    
    # Get quality preset
    quality = get_quality_preset()
    
    # Get custom settings
    fps, width = get_custom_settings()
    
    # Confirm and process
    print("\n" + "═" * 62)
    print("📋 Summary:")
    print(f"   • Input files: {len(input_paths)}")
    for i, path in enumerate(input_paths, 1):
        print(f"     {i}. {os.path.basename(path)}")
    print(f"   • Quality: {quality}")
    if fps:
        print(f"   • FPS: {fps}")
    if width:
        print(f"   • Width: {width}px")
    print("═" * 62)
    
    confirm = input("\nProceed? (Y/n): ").strip().lower()
    if confirm and confirm not in ['y', 'yes']:
        print("   ℹ️  Cancelled")
        return
    
    try:
        # Process with custom FPS if provided, otherwise use quality preset default
        actual_fps = fps if fps else 10  # Let convert function use quality preset
        output = convert_mp4_to_gif(
            input_paths, 
            output_path, 
            fps=actual_fps,
            width=width,
            quality=quality
        )
        print(f"\n🎉 Success! Output file: {os.path.abspath(output)}")
    except Exception as e:
        print_error(f"Failed: {str(e)}")
    
    input("\nPress Enter to continue...")


def interactive_gif_loop():
    """Interactive mode for making GIF loop infinitely."""
    print_section_header("🔁 Make GIF Loop Infinitely")
    
    # Get input file
    input_paths = get_file_paths("Enter GIF file path", allow_multiple=False)
    
    if not input_paths:
        print_warning("No file provided. Returning to menu.")
        return
    
    input_path = input_paths[0]
    
    # Get output path
    print("\n📁 Output file (optional - press Enter for automatic naming):")
    print("   💡 Tip: Automatic naming adds '_looped' suffix")
    output_path = input("   Output path: ").strip().strip('"').strip("'")
    if not output_path:
        output_path = None
        print("   ℹ️  Will use automatic naming")
    
    # Confirm and process
    print("\n" + "═" * 62)
    print("📋 Summary:")
    print(f"   • Input: {os.path.basename(input_path)}")
    if output_path:
        print(f"   • Output: {os.path.basename(output_path)}")
    print("═" * 62)
    
    confirm = input("\nProceed? (Y/n): ").strip().lower()
    if confirm and confirm not in ['y', 'yes']:
        print("   ℹ️  Cancelled")
        return
    
    try:
        output = make_gif_loop(input_path, output_path)
        print(f"\n🎉 Success! Output file: {os.path.abspath(output)}")
    except Exception as e:
        print_error(f"Failed: {str(e)}")
    
    input("\nPress Enter to continue...")


def interactive_batch_process():
    """Interactive mode for batch processing multiple files."""
    print_section_header("📦 Batch Process Files")
    
    print("\nℹ️  Batch processing allows you to process multiple files at once")
    print("💡 Tip: Great for converting entire folders of videos or GIFs")
    
    # Choose operation type
    print("\n⚙️  Select operation:")
    print("   1. Convert MP4s to looping GIFs")
    print("   2. Make GIFs loop infinitely")
    
    op_choice = input("\n   Choice (1-2): ").strip()
    
    if op_choice not in ['1', '2']:
        print_warning("Invalid choice. Returning to menu.")
        return
    
    is_mp4_mode = (op_choice == '1')
    
    # Get input files
    if is_mp4_mode:
        input_paths = get_file_paths("Enter MP4 file path(s) or pattern (e.g., *.mp4)", allow_multiple=True)
    else:
        input_paths = get_file_paths("Enter GIF file path(s) or pattern (e.g., *.gif)", allow_multiple=True)
    
    if not input_paths:
        print_warning("No files provided. Returning to menu.")
        return
    
    # Get settings for MP4 mode
    quality = None
    fps = None
    width = None
    if is_mp4_mode:
        quality = get_quality_preset()
        fps, width = get_custom_settings()
    
    # Confirm
    print("\n" + "═" * 62)
    print("📋 Batch Summary:")
    print(f"   • Operation: {'MP4 to GIF' if is_mp4_mode else 'Make GIF loop'}")
    print(f"   • Files to process: {len(input_paths)}")
    if is_mp4_mode and quality:
        print(f"   • Quality: {quality}")
    if fps:
        print(f"   • FPS: {fps}")
    if width:
        print(f"   • Width: {width}px")
    print("═" * 62)
    
    confirm = input("\nProcess all files? (Y/n): ").strip().lower()
    if confirm and confirm not in ['y', 'yes']:
        print("   ℹ️  Cancelled")
        return
    
    # Process files
    success_count = 0
    fail_count = 0
    
    print(f"\n{'─' * 62}")
    print(f"Processing {len(input_paths)} file(s)...")
    print(f"{'─' * 62}")
    
    for i, input_path in enumerate(input_paths, 1):
        print(f"\n[{i}/{len(input_paths)}] Processing: {os.path.basename(input_path)}")
        
        try:
            if is_mp4_mode:
                actual_fps = fps if fps else 10
                convert_mp4_to_gif(
                    [input_path], 
                    None,  # Auto-generate output name
                    fps=actual_fps,
                    width=width,
                    quality=quality
                )
            else:
                make_gif_loop(input_path, None)  # Auto-generate output name
            
            success_count += 1
        except Exception as e:
            print_error(f"Failed to process {os.path.basename(input_path)}: {str(e)}")
            fail_count += 1
    
    # Summary
    print(f"\n{'═' * 62}")
    print("📊 Batch Processing Complete!")
    print(f"   • Successful: {success_count}")
    print(f"   • Failed: {fail_count}")
    print(f"{'═' * 62}")
    
    input("\nPress Enter to continue...")


def interactive_mode():
    """Run the application in interactive mode with menu."""
    while True:
        # Clear screen (works on most terminals)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        display_banner()
        display_menu()
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            interactive_mp4_to_gif()
        elif choice == '2':
            interactive_gif_loop()
        elif choice == '3':
            interactive_batch_process()
        elif choice == '4':
            display_help()
        elif choice == '5':
            print("\n👋 Thank you for using GIF Worker!")
            print("   Visit again for all your PowerPoint GIF needs!\n")
            sys.exit(0)
        else:
            print_warning("Invalid choice. Please select 1-5.")
            time.sleep(1)


# ═══════════════════════════════════════════════════════════════════════════
#                          COMMAND-LINE MODE
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main function to handle command line arguments or start interactive mode."""
    parser = argparse.ArgumentParser(
        description="GIF Worker - Professional PowerPoint GIF Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
═══════════════════════════════════════════════════════════════════════════
                              EXAMPLES
═══════════════════════════════════════════════════════════════════════════

MP4 to GIF Mode:
────────────────────────────────────────────────────────────────────────────
  Single file:
    python gif_worker.py --mp4 video.mp4
  
  Multiple files (stitched together):
    python gif_worker.py --mp4 part1.mp4 part2.mp4 part3.mp4 -o combined.gif
  
  All MP4s in folder with high quality:
    python gif_worker.py --mp4 *.mp4 --quality high --fps 15
  
  Custom dimensions:
    python gif_worker.py --mp4 video.mp4 --width 800

GIF Looping Mode:
────────────────────────────────────────────────────────────────────────────
  Make GIF loop infinitely:
    python gif_worker.py --loop animation.gif
  
  Specify output name:
    python gif_worker.py --loop input.gif -o output_looped.gif

Batch Processing:
────────────────────────────────────────────────────────────────────────────
  Loop all GIFs in folder:
    python gif_worker.py --batch *.gif --loop
  
  Convert all MP4s:
    python gif_worker.py --batch *.mp4 --mp4 --quality low

Interactive Mode:
────────────────────────────────────────────────────────────────────────────
  Launch interactive menu (no arguments):
    python gif_worker.py

Quality Presets:
────────────────────────────────────────────────────────────────────────────
  low    → 8 fps, 50% size  (smallest files)
  medium → 10 fps, 70% size (balanced, default)
  high   → 15 fps, 100% size (best quality)

═══════════════════════════════════════════════════════════════════════════
        """
    )
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--mp4', nargs='+', metavar='FILE', 
                           help='Convert MP4(s) to looping GIF. Can specify multiple files.')
    mode_group.add_argument('--loop', metavar='FILE',
                           help='Make existing GIF loop infinitely.')
    mode_group.add_argument('--batch', nargs='+', metavar='FILE',
                           help='Batch process multiple files.')
    
    # Common arguments
    parser.add_argument('--output', '-o', metavar='FILE',
                       help='Output file path (optional, auto-generated if not specified)')
    
    # MP4 conversion arguments
    parser.add_argument('--fps', type=int, default=10, metavar='N',
                       help='Frames per second for GIF (default: 10, or based on quality preset)')
    parser.add_argument('--width', type=int, metavar='PIXELS',
                       help='Width in pixels (height auto-calculated)')
    parser.add_argument('--quality', choices=['low', 'medium', 'high'], default='medium',
                       help='Quality preset: low, medium (default), or high')
    
    parser.add_argument('--version', action='version', version='GIF Worker 1.0')
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    # Command-line mode
    display_banner()
    
    try:
        if args.mp4:
            # MP4 to GIF mode
            print_section_header("🎬 MP4 to GIF Mode")
            
            # Expand glob patterns
            expanded_inputs = []
            for pattern in args.mp4:
                if '*' in pattern or '?' in pattern:
                    matches = glob.glob(pattern)
                    if matches:
                        expanded_inputs.extend(sorted(matches))
                        print_info(f"Pattern '{pattern}' matched {len(matches)} file(s)")
                    else:
                        print_warning(f"No files match pattern '{pattern}'")
                else:
                    expanded_inputs.append(pattern)
            
            if not expanded_inputs:
                print_error("No input files found")
                sys.exit(1)
            
            # Show file list if multiple
            if len(expanded_inputs) > 1:
                print(f"\n📋 Processing {len(expanded_inputs)} files:")
                for i, file in enumerate(expanded_inputs, 1):
                    print(f"   {i}. {os.path.basename(file)}")
            
            # Convert
            output = convert_mp4_to_gif(
                expanded_inputs,
                args.output,
                fps=args.fps,
                width=args.width,
                quality=args.quality
            )
            
            print(f"\n🎉 Complete! Output: {os.path.abspath(output)}")
            
        elif args.loop:
            # GIF looping mode
            print_section_header("🔁 GIF Looping Mode")
            
            output = make_gif_loop(args.loop, args.output)
            
            print(f"\n🎉 Complete! Output: {os.path.abspath(output)}")
            
        elif args.batch:
            # Batch processing mode
            print_section_header("📦 Batch Processing Mode")
            
            # Expand glob patterns
            expanded_inputs = []
            for pattern in args.batch:
                if '*' in pattern or '?' in pattern:
                    matches = glob.glob(pattern)
                    if matches:
                        expanded_inputs.extend(sorted(matches))
                    else:
                        print_warning(f"No files match pattern '{pattern}'")
                else:
                    expanded_inputs.append(pattern)
            
            if not expanded_inputs:
                print_error("No input files found")
                sys.exit(1)
            
            print_info(f"Processing {len(expanded_inputs)} file(s) in batch mode")
            print_tip("Each file will be processed individually with auto-generated output names")
            
            # Determine mode based on file extensions
            mp4_files = [f for f in expanded_inputs if f.lower().endswith('.mp4')]
            gif_files = [f for f in expanded_inputs if f.lower().endswith('.gif')]
            
            if mp4_files and gif_files:
                print_warning("Mixed file types detected. Processing all as individual files.")
            
            success_count = 0
            fail_count = 0
            
            for i, input_path in enumerate(expanded_inputs, 1):
                print(f"\n[{i}/{len(expanded_inputs)}] {os.path.basename(input_path)}")
                
                try:
                    if input_path.lower().endswith('.mp4'):
                        convert_mp4_to_gif(
                            [input_path],
                            None,  # Auto-generate output
                            fps=args.fps,
                            width=args.width,
                            quality=args.quality
                        )
                    elif input_path.lower().endswith('.gif'):
                        make_gif_loop(input_path, None)
                    else:
                        print_warning(f"Unsupported file type, skipping")
                        continue
                    
                    success_count += 1
                except Exception as e:
                    print_error(f"Failed: {str(e)}")
                    fail_count += 1
            
            print(f"\n{'═' * 62}")
            print(f"📊 Batch Complete: {success_count} succeeded, {fail_count} failed")
            print(f"{'═' * 62}")
        
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(str(e))
        print_info("Make sure you have the required packages installed:")
        print("   pip install moviepy Pillow")
        sys.exit(1)


if __name__ == "__main__":
    main()
