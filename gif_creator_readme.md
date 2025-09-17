# GIF Tools

Two Python scripts for creating continuously looping GIFs perfect for PowerPoint presentations:

1. **gif_looper.py** - Convert existing GIFs to loop infinitely
2. **gif_creator.py** - Convert single or multiple MP4 videos to looping GIFs

## Features

### gif_looper.py
- ✅ Converts any GIF to loop infinitely
- ✅ Preserves original frame timing and quality
- ✅ Optimizes file size
- ✅ Simple command-line interface

### gif_creator.py (Enhanced Multi-File Support)
- ✅ Converts single MP4 videos to looping GIFs
- ✅ Stitches multiple MP4s together into one continuous GIF
- ✅ Supports glob patterns (*.mp4) to process all files in a folder
- ✅ Quality presets (low, medium, high)
- ✅ Customizable frame rate and dimensions
- ✅ Automatic file size optimization
- ✅ Smart dimension handling and video resizing

## Installation

### Option 1: Use the Included Virtual Environment (Recommended)
The folder includes a pre-configured virtual environment with all dependencies:

1. **Navigate to the GIF creator folder:**
   ```bash
   cd "path\to\GIF creator"
   ```

2. **Activate the virtual environment:**
   ```bash
   # Windows
   gif_env\Scripts\activate
   
   # You should see (gif_env) in your prompt
   ```

3. **Run the scripts:**
   ```bash
   python gif_creator.py video.mp4
   python gif_looper.py animation.gif
   ```

### Option 2: Manual Installation
If you prefer to install dependencies yourself:

1. Make sure you have Python 3.6+ installed
2. Install the required packages:
   ```
   pip install Pillow moviepy
   ```
   
   Or install from requirements file:
   ```
   pip install -r gif_creator_requirements.txt
   ```

**Note:** MoviePy 2.x has different API than 1.x. This code is compatible with MoviePy 2.0+.

## Usage

### gif_looper.py - Convert existing GIFs

**Basic usage:**
```bash
python gif_looper.py input.gif
```
Creates `input_looped.gif`

**Specify output filename:**
```bash
python gif_looper.py input.gif output.gif
```

### gif_creator.py - Convert MP4 to GIF

**Single file:**
```bash
python gif_creator.py video.mp4
```
Creates `video.gif`

**Multiple files (stitched together):**
```bash
python gif_creator.py video1.mp4 video2.mp4 video3.mp4
```
Creates `combined_video.gif`

**Specify output name:**
```bash
python gif_creator.py part1.mp4 part2.mp4 --output presentation.gif
```

**All MP4s in current directory:**
```bash
python gif_creator.py *.mp4 --output slideshow.gif
```

**With quality settings:**
```bash
python gif_creator.py video.mp4 --quality high --fps 15
```

**Custom dimensions:**
```bash
python gif_creator.py video1.mp4 video2.mp4 --width 800
```

## Quality Presets

- **low** - 8 fps, 50% size (smallest files, ~1-3 MB)
- **medium** - 10 fps, 70% size (balanced, default, ~3-8 MB)
- **high** - 15 fps, 100% size (best quality, ~8-20+ MB)

## Examples

```bash
# Convert single MP4 to GIF
python gif_creator.py presentation_video.mp4

# Combine multiple MP4s into one GIF
python gif_creator.py intro.mp4 demo.mp4 outro.mp4

# High quality conversion with multiple files
python gif_creator.py part1.mp4 part2.mp4 part3.mp4 --output demo_hq.gif --quality high

# All MP4s in folder to small GIF
python gif_creator.py *.mp4 --output slideshow.gif --quality low --width 400

# Convert existing GIF to loop
python gif_looper.py animation.gif looping_animation.gif

# Process files with spaces in names
python gif_creator.py "C:\Videos\Part 1.mp4" "C:\Videos\Part 2.mp4" --output "C:\Presentation\animation.gif"
```

## PowerPoint Integration

1. Run the appropriate script on your video/GIF file(s)
2. Insert the output GIF into PowerPoint (Insert → Pictures → This Device)
3. The GIF will now loop continuously during your presentation

## Common Use Cases

### **Multi-Part Presentations**
Create seamless presentation flows by combining intro, content, and outro videos:
```bash
python gif_creator.py intro.mp4 main_content.mp4 conclusion.mp4 --output full_presentation.gif
```

### **Batch Processing**
Convert all MP4s in a folder to a single slideshow:
```bash
python gif_creator.py *.mp4 --output conference_slideshow.gif --quality medium
```

### **File Size Optimization**
For email sharing or web use:
```bash
python gif_creator.py large_video.mp4 --quality low --width 400
```

## What the scripts do

### gif_looper.py
- Opens the input GIF file
- Extracts all frames and timing information
- Saves with loop count set to 0 (infinite loops)
- Optimizes file size

### gif_creator.py
- Loads one or more MP4 videos using MoviePy
- Stitches multiple videos together in sequence (if multiple files provided)
- Resizes all videos to match the first video's dimensions
- Converts to GIF format with optimized settings
- Sets loop count to 0 (infinite loops)
- Provides file size optimization tips

## Troubleshooting

**"Module not found" error:**
```bash
pip install Pillow moviepy
```

**MoviePy installation issues on Windows:**
```bash
pip install --upgrade pip
pip install moviepy[optional]
```

**API compatibility issues:**
- This code requires MoviePy 2.0+ (included in virtual environment)
- If using MoviePy 1.x, some methods may differ
- The included virtual environment has the correct versions

**Virtual environment activation:**
```bash
# Make sure you're in the GIF creator folder
gif_env\Scripts\activate

# You should see (gif_env) in your prompt before running scripts
```

**Large file sizes:**
- Try `--quality low` option
- Use `--width 400` or smaller
- Reduce `--fps` to 8 or lower
- Consider splitting very long videos into shorter segments

**Multiple file processing issues:**
- Ensure all MP4 files are in the same directory when using `*.mp4`
- Check that file paths don't contain special characters
- Use quotes around file paths with spaces

**"File not found" error:**
- Check the file path is correct
- Use quotes around paths with spaces
- Make sure the file exists and is readable
- For glob patterns (`*.mp4`), ensure you're in the correct directory

**The output GIF doesn't loop in PowerPoint:**
- Try saving your PowerPoint as .pptx format
- Ensure you're using a recent version of PowerPoint
- Check that the GIF plays correctly in a web browser first
- Some very large GIFs may not display properly - try reducing file size

**Videos don't stitch together properly:**
- Check that all input videos have similar frame rates
- Ensure videos are not corrupted
- Try converting videos to the same format/codec before processing
- Use `--width` parameter to force consistent dimensions