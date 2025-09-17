#!/usr/bin/env python3
"""
GIF Creator - Convert MP4 videos to continuously looping GIFs for PowerPoint

This script takes one or more MP4 files and converts them to a continuously looping GIF
suitable for PowerPoint presentations. Multiple MP4s will be stitched together in sequence.
Includes options for quality control and frame rate adjustment.

Usage:
    python gif_creator.py input.mp4 [output.gif]                    # Single file
    python gif_creator.py input1.mp4 input2.mp4 input3.mp4         # Multiple files
    python gif_creator.py *.mp4 --output combined.gif              # All MP4s in folder

If no output filename is provided, it will create a new file with ".gif" extension.

Requirements:
    pip install moviepy Pillow
"""

import sys
import os
from moviepy import VideoFileClip, concatenate_videoclips
from PIL import Image
import argparse
import tempfile
import glob


def convert_mp4_to_gif(input_paths, output_path=None, fps=10, width=None, quality='medium'):
    """
    Convert one or more MP4 videos to a continuously looping GIF.
    
    Args:
        input_paths (list): List of paths to input MP4 files
        output_path (str): Path for output GIF file (optional)
        fps (int): Frames per second for the GIF (default: 10)
        width (int): Width in pixels (height auto-calculated, optional)
        quality (str): Quality preset ('low', 'medium', 'high')
    
    Returns:
        str: Path to the output file
    """
    # Validate input files
    valid_paths = []
    for path in input_paths:
        if not os.path.exists(path):
            print(f"⚠️  Warning: File not found, skipping: {path}")
            continue
        if not path.lower().endswith('.mp4'):
            print(f"⚠️  Warning: Not an MP4 file, skipping: {path}")
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
        
        print(f"📹 Loading {len(valid_paths)} video file(s):")
        
        # Load all video clips
        for i, path in enumerate(valid_paths, 1):
            print(f"  {i}. {os.path.basename(path)}")
            clip = VideoFileClip(path)
            
            duration = clip.duration
            original_fps = clip.fps
            original_size = clip.size
            total_duration += duration
            
            print(f"     - Duration: {duration:.1f}s, FPS: {original_fps:.1f}, Size: {original_size[0]}x{original_size[1]}")
            
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
                
                print(f"  📐 Target size for all videos: {new_width}x{new_height}")
                print(f"  🎬 Target FPS: {fps}")
            
            # Resize to match target dimensions
            if original_size != target_size:
                clip_resized = clip.resized(target_size)
                video_clips.append(clip_resized)
            else:
                video_clips.append(clip)
        
        print(f"📊 Total duration: {total_duration:.1f} seconds")
        
        # Concatenate videos if multiple files
        if len(video_clips) == 1:
            final_video = video_clips[0]
            print(f"🔄 Converting single video to GIF...")
        else:
            print(f"🔗 Stitching {len(video_clips)} videos together...")
            final_video = concatenate_videoclips(video_clips, method="compose")
            print(f"🔄 Converting combined video to GIF...")
        
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
        
        print(f"✓ Successfully created looping GIF: {output_path}")
        print(f"  - Videos combined: {len(valid_paths)}")
        print(f"  - Total duration: {total_duration:.1f} seconds")
        print(f"  - File size: {output_size:,} bytes ({output_size/1024/1024:.1f} MB)")
        print(f"  - Ready for PowerPoint!")
        
        return output_path
        
    except Exception as e:
        # Clean up on error
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass
        raise Exception(f"Error converting MP4(s) to GIF: {str(e)}")


def main():
    """Main function to handle command line arguments and process MP4(s)."""
    parser = argparse.ArgumentParser(
        description="Convert MP4 videos to continuously looping GIFs for PowerPoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Single file
    python gif_creator.py video.mp4
    python gif_creator.py input.mp4 output.gif
    
    # Multiple files (stitched together)
    python gif_creator.py video1.mp4 video2.mp4 video3.mp4
    python gif_creator.py part1.mp4 part2.mp4 --output combined.gif
    
    # All MP4s in current directory
    python gif_creator.py *.mp4 --output presentation.gif
    
    # With quality settings
    python gif_creator.py video1.mp4 video2.mp4 --fps 15 --quality high
    python gif_creator.py "C:/Videos/Part 1.mp4" "C:/Videos/Part 2.mp4" --width 800

Quality presets:
    low    - 8 fps, 50% size (smallest files)
    medium - 10 fps, 70% size (balanced, default)
    high   - 15 fps, 100% size (best quality, larger files)
        """
    )
    
    parser.add_argument('inputs', nargs='+', help='Input MP4 file path(s). Can specify multiple files to stitch together.')
    parser.add_argument('--output', '-o', help='Output GIF file path (optional)')
    parser.add_argument('--fps', type=int, default=10, help='Frames per second (default: 10)')
    parser.add_argument('--width', type=int, help='Width in pixels (height auto-calculated)')
    parser.add_argument('--quality', choices=['low', 'medium', 'high'], default='medium',
                      help='Quality preset (default: medium)')
    parser.add_argument('--version', action='version', version='GIF Creator 2.0')
    
    # Handle case where script is run without arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    try:
        # Expand glob patterns (like *.mp4)
        expanded_inputs = []
        for pattern in args.inputs:
            if '*' in pattern or '?' in pattern:
                matches = glob.glob(pattern)
                if matches:
                    expanded_inputs.extend(sorted(matches))
                else:
                    print(f"⚠️  Warning: No files match pattern '{pattern}'")
            else:
                expanded_inputs.append(pattern)
        
        if not expanded_inputs:
            print("❌ No input files specified or found")
            sys.exit(1)
        
        # Validate that at least one file looks like an MP4
        mp4_files = [f for f in expanded_inputs if f.lower().endswith('.mp4')]
        if not mp4_files:
            print("⚠️  Warning: No MP4 files found in inputs. Trying anyway...")
        
        # Show what files will be processed
        if len(expanded_inputs) > 1:
            print(f"🎬 Processing {len(expanded_inputs)} files in sequence:")
            for i, file in enumerate(expanded_inputs, 1):
                print(f"   {i}. {os.path.basename(file)}")
            print()
        
        # Process the MP4(s)
        output_file = convert_mp4_to_gif(
            expanded_inputs, 
            args.output, 
            fps=args.fps,
            width=args.width,
            quality=args.quality
        )
        
        print(f"\n🎉 Done! Your looping GIF is ready for PowerPoint:")
        print(f"   {os.path.abspath(output_file)}")
        
        # Provide optimization tips
        file_size_mb = os.path.getsize(output_file) / 1024 / 1024
        if file_size_mb > 10:
            print(f"\n💡 Tip: File is {file_size_mb:.1f}MB. For smaller files, try:")
            if len(expanded_inputs) > 1:
                print(f"   python gif_creator.py {' '.join([f'\"{f}\"' for f in expanded_inputs])} --quality low")
                print(f"   python gif_creator.py {' '.join([f'\"{f}\"' for f in expanded_inputs])} --width 400")
            else:
                print(f"   python gif_creator.py \"{expanded_inputs[0]}\" --quality low")
                print(f"   python gif_creator.py \"{expanded_inputs[0]}\" --width 400")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Make sure you have the required packages installed:")
        print(f"   pip install moviepy Pillow")
        sys.exit(1)


if __name__ == "__main__":
    main()