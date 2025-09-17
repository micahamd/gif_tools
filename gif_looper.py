#!/usr/bin/env python3
"""
GIF Looper - Convert any GIF to a continuously looping GIF for PowerPoint

This script takes a GIF file and ensures it loops continuously by setting
the loop count to 0 (infinite loops). Perfect for PowerPoint presentations.

Usage:
    python gif_looper.py input.gif [output.gif]

If no output filename is provided, it will create a new file with "_looped" suffix.

Requirements:
    pip install Pillow
"""

import sys
import os
from PIL import Image
import argparse


def make_gif_loop(input_path, output_path=None):
    """
    Convert a GIF to loop continuously.
    
    Args:
        input_path (str): Path to input GIF file
        output_path (str): Path for output GIF file (optional)
    
    Returns:
        str: Path to the output file
    """
    # Validate input file
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Generate output filename if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_looped.gif"
    
    try:
        # Open the GIF
        with Image.open(input_path) as img:
            # Check if it's actually a GIF
            if img.format != 'GIF':
                print(f"Warning: Input file is {img.format}, not GIF. Converting anyway...")
            
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
                frames[0].save(
                    output_path,
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=0,  # 0 = infinite loop
                    optimize=True
                )
                
                print(f"✓ Successfully created looping GIF: {output_path}")
                print(f"  - Frames: {len(frames)}")
                print(f"  - Average duration: {sum(durations)/len(durations):.1f}ms per frame")
                print(f"  - File size: {os.path.getsize(output_path)} bytes")
                
                return output_path
            else:
                raise ValueError("No frames found in the input file")
                
    except Exception as e:
        raise Exception(f"Error processing GIF: {str(e)}")


def main():
    """Main function to handle command line arguments and process GIF."""
    parser = argparse.ArgumentParser(
        description="Convert any GIF to loop continuously for PowerPoint presentations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python gif_looper.py animation.gif
    python gif_looper.py input.gif output_looped.gif
    python gif_looper.py "C:/path/with spaces/animation.gif"
        """
    )
    
    parser.add_argument('input', help='Input GIF file path')
    parser.add_argument('output', nargs='?', help='Output GIF file path (optional)')
    parser.add_argument('--version', action='version', version='GIF Looper 1.0')
    
    # Handle case where script is run without arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    try:
        # Process the GIF
        output_file = make_gif_loop(args.input, args.output)
        
        print(f"\n🎉 Done! Your looping GIF is ready for PowerPoint:")
        print(f"   {os.path.abspath(output_file)}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()