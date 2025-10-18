# 🎬 GIF Worker - PowerPoint GIF Studio# GIF Tools



**Professional tools for creating continuously looping GIFs perfect for PowerPoint presentations**Two Python scripts for creating continuously looping GIFs perfect for PowerPoint presentations:



Transform your videos and GIFs into presentation-ready, infinitely-looping animations with an intuitive GUI or powerful command-line interface.1. **gif_looper.py** - Convert existing GIFs to loop infinitely

2. **gif_creator.py** - Convert single or multiple MP4 videos to looping GIFs

---

## Features

## ✨ Features

### gif_looper.py

### 🎨 **Beautiful GUI Application**- ✅ Converts any GIF to loop infinitely

- **Tabbed interface** for easy navigation- ✅ Preserves original frame timing and quality

- **Drag & drop** file support- ✅ Optimizes file size

- **Real-time progress** tracking- ✅ Simple command-line interface

- **Batch processing** capabilities

- **Quality presets** with helpful tooltips### gif_creator.py (Enhanced Multi-File Support)

- **Professional design** with modern UI- ✅ Converts single MP4 videos to looping GIFs

- ✅ Stitches multiple MP4s together into one continuous GIF

### 🚀 **Powerful Functionality**- ✅ Supports glob patterns (*.mp4) to process all files in a folder

- ✅ Convert single or multiple MP4 videos to looping GIFs- ✅ Quality presets (low, medium, high)

- ✅ Stitch multiple videos together seamlessly- ✅ Customizable frame rate and dimensions

- ✅ Make existing GIFs loop infinitely- ✅ Automatic file size optimization

- ✅ Batch process entire folders- ✅ Smart dimension handling and video resizing

- ✅ Quality presets (low, medium, high)

- ✅ Customizable frame rate and dimensions## Installation

- ✅ Automatic file size optimization

- ✅ Smart dimension handling### Option 1: Use the Included Virtual Environment (Recommended)

The folder includes a pre-configured virtual environment with all dependencies:

### 💻 **Flexible Interface Options**

- **GUI Mode**: Beautiful graphical interface (recommended)1. **Navigate to the GIF creator folder:**

- **Interactive CLI**: Menu-driven command-line interface   ```bash

- **Command-line**: Full automation support for scripts   cd "path\to\GIF creator"

   ```

---

2. **Activate the virtual environment:**

## 📦 Installation   ```bash

   # Windows

### Option 1: Use the Included Virtual Environment (Recommended)   gif_env\Scripts\activate

   

The project includes a pre-configured virtual environment with all dependencies:   # You should see (gif_env) in your prompt

   ```

```powershell

# Navigate to the project folder3. **Run the scripts:**

cd "path\to\GIF creator"   ```bash

   python gif_creator.py video.mp4

# Activate the virtual environment (Windows)   python gif_looper.py animation.gif

gif_env\Scripts\activate   ```



# You should see (gif_env) in your prompt### Option 2: Manual Installation

```If you prefer to install dependencies yourself:



### Option 2: Manual Installation1. Make sure you have Python 3.6+ installed

2. Install the required packages:

If you prefer to install dependencies yourself:   ```

   pip install Pillow moviepy

```bash   ```

# Make sure you have Python 3.7+ installed   

pip install moviepy Pillow   Or install from requirements file:

   ```

# Or install from requirements file   pip install -r gif_creator_requirements.txt

pip install -r gif_creator_requirements.txt   ```

```

**Note:** MoviePy 2.x has different API than 1.x. This code is compatible with MoviePy 2.0+.

**Note:** MoviePy 2.x has a different API than 1.x. This code is compatible with MoviePy 2.0+.

## Usage

---

### gif_looper.py - Convert existing GIFs

## 🎯 Quick Start

**Basic usage:**

### GUI Mode (Recommended for Most Users)```bash

python gif_looper.py input.gif

Simply run:```

```powershellCreates `input_looped.gif`

python gif_worker_gui.py

```**Specify output filename:**

```bash

Then:python gif_looper.py input.gif output.gif

1. Choose your tab: **MP4 to GIF**, **Loop GIF**, or **Batch Process**```

2. Select your files

3. Adjust settings (quality, FPS, width)### gif_creator.py - Convert MP4 to GIF

4. Click the convert button!

**Single file:**

**Perfect for:**```bash

- Users who prefer visual interfacespython gif_creator.py video.mp4

- Quick one-off conversions```

- Experimenting with different settingsCreates `video.gif`



---**Multiple files (stitched together):**

```bash

### Interactive Menu Modepython gif_creator.py video1.mp4 video2.mp4 video3.mp4

```

Run without arguments for an interactive menu:Creates `combined_video.gif`

```powershell

python gif_worker.py**Specify output name:**

``````bash

python gif_creator.py part1.mp4 part2.mp4 --output presentation.gif

Navigate through the menu to:```

- Convert MP4s to GIFs

- Make GIFs loop infinitely**All MP4s in current directory:**

- Batch process multiple files```bash

- View help and examplespython gif_creator.py *.mp4 --output slideshow.gif

```

**Perfect for:**

- Users comfortable with terminals**With quality settings:**

- Quick access to all features```bash

- Step-by-step guided workflowpython gif_creator.py video.mp4 --quality high --fps 15

```

---

**Custom dimensions:**

### Command-Line Mode```bash

python gif_creator.py video1.mp4 video2.mp4 --width 800

Full automation support for scripts and power users:```



#### MP4 to GIF Conversion## Quality Presets



```bash- **low** - 8 fps, 50% size (smallest files, ~1-3 MB)

# Single file- **medium** - 10 fps, 70% size (balanced, default, ~3-8 MB)

python gif_worker.py --mp4 video.mp4- **high** - 15 fps, 100% size (best quality, ~8-20+ MB)



# Multiple files (stitched together)## Examples

python gif_worker.py --mp4 part1.mp4 part2.mp4 part3.mp4 -o combined.gif

```bash

# All MP4s in folder# Convert single MP4 to GIF

python gif_worker.py --mp4 *.mp4 --quality highpython gif_creator.py presentation_video.mp4



# Custom settings# Combine multiple MP4s into one GIF

python gif_worker.py --mp4 video.mp4 --fps 15 --width 800 --quality highpython gif_creator.py intro.mp4 demo.mp4 outro.mp4

```

# High quality conversion with multiple files

#### GIF Loopingpython gif_creator.py part1.mp4 part2.mp4 part3.mp4 --output demo_hq.gif --quality high



```bash# All MP4s in folder to small GIF

# Make GIF loop infinitelypython gif_creator.py *.mp4 --output slideshow.gif --quality low --width 400

python gif_worker.py --loop animation.gif

# Convert existing GIF to loop

# Specify output namepython gif_looper.py animation.gif looping_animation.gif

python gif_worker.py --loop input.gif -o output_looped.gif

```# Process files with spaces in names

python gif_creator.py "C:\Videos\Part 1.mp4" "C:\Videos\Part 2.mp4" --output "C:\Presentation\animation.gif"

#### Batch Processing```



```bash## PowerPoint Integration

# Loop all GIFs in folder

python gif_worker.py --batch *.gif --loop1. Run the appropriate script on your video/GIF file(s)

2. Insert the output GIF into PowerPoint (Insert → Pictures → This Device)

# Convert all MP4s3. The GIF will now loop continuously during your presentation

python gif_worker.py --batch *.mp4 --mp4 --quality medium

```## Common Use Cases



**Perfect for:**### **Multi-Part Presentations**

- Automation and scriptingCreate seamless presentation flows by combining intro, content, and outro videos:

- Processing many files```bash

- Integration with other toolspython gif_creator.py intro.mp4 main_content.mp4 conclusion.mp4 --output full_presentation.gif

- Repeatable workflows```



---### **Batch Processing**

Convert all MP4s in a folder to a single slideshow:

## ⚙️ Quality Presets```bash

python gif_creator.py *.mp4 --output conference_slideshow.gif --quality medium

Choose the preset that matches your needs:```



| Preset | FPS | Size | File Size | Best For |### **File Size Optimization**

|--------|-----|------|-----------|----------|For email sharing or web use:

| **Low** | 8 | 50% | ~1-3 MB | Email sharing, web use, file size critical |```bash

| **Medium** | 10 | 70% | ~3-8 MB | **Most presentations** (default, balanced) |python gif_creator.py large_video.mp4 --quality low --width 400

| **High** | 15 | 100% | ~8-20+ MB | High-quality local presentations, demos |```



💡 **Tip**: For most PowerPoint presentations, **medium** quality provides the best balance of quality and file size.## What the scripts do



---### gif_looper.py

- Opens the input GIF file

## 📖 Common Examples- Extracts all frames and timing information

- Saves with loop count set to 0 (infinite loops)

### Create a Presentation GIF from Video- Optimizes file size

```bash

python gif_worker.py --mp4 presentation.mp4 --quality medium### gif_creator.py

```- Loads one or more MP4 videos using MoviePy

- Stitches multiple videos together in sequence (if multiple files provided)

### Combine Multiple Video Segments- Resizes all videos to match the first video's dimensions

```bash- Converts to GIF format with optimized settings

python gif_worker.py --mp4 intro.mp4 demo.mp4 outro.mp4 -o full_demo.gif- Sets loop count to 0 (infinite loops)

```- Provides file size optimization tips



### Make an Existing GIF Loop in PowerPoint## Troubleshooting

```bash

python gif_worker.py --loop animation.gif**"Module not found" error:**

``````bash

pip install Pillow moviepy

### Batch Convert All Videos in a Folder```

```bash

python gif_worker.py --batch *.mp4 --mp4 --quality low --width 600**MoviePy installation issues on Windows:**

``````bash

pip install --upgrade pip

### Create a Small GIF for Emailpip install moviepy[optional]

```bash```

python gif_worker.py --mp4 video.mp4 --quality low --width 400

```**API compatibility issues:**

- This code requires MoviePy 2.0+ (included in virtual environment)

### High Quality GIF for Important Presentation- If using MoviePy 1.x, some methods may differ

```bash- The included virtual environment has the correct versions

python gif_worker.py --mp4 keynote.mp4 --quality high --fps 15

```**Virtual environment activation:**

```bash

---# Make sure you're in the GIF creator folder

gif_env\Scripts\activate

## 🎓 PowerPoint Integration

# You should see (gif_env) in your prompt before running scripts

1. **Create your GIF** using any of the methods above```

2. **Insert into PowerPoint**: Insert → Pictures → This Device

3. **Select your GIF** and place it on your slide**Large file sizes:**

4. **Present!** The GIF will loop continuously during your presentation- Try `--quality low` option

- Use `--width 400` or smaller

### PowerPoint Tips:- Reduce `--fps` to 8 or lower

- Keep file sizes under 10MB for smooth playback- Consider splitting very long videos into shorter segments

- Test your GIF in slideshow mode before presenting

- Use medium quality for most presentations**Multiple file processing issues:**

- Width of 400-600px works well for slide elements- Ensure all MP4 files are in the same directory when using `*.mp4`

- All GIFs created loop infinitely automatically!- Check that file paths don't contain special characters

- Use quotes around file paths with spaces

---

**"File not found" error:**

## 🔧 Advanced Options- Check the file path is correct

- Use quotes around paths with spaces

### Custom FPS (Frames Per Second)- Make sure the file exists and is readable

```bash- For glob patterns (`*.mp4`), ensure you're in the correct directory

python gif_worker.py --mp4 video.mp4 --fps 12

```**The output GIF doesn't loop in PowerPoint:**

Higher FPS = smoother animation, larger file size- Try saving your PowerPoint as .pptx format

- Ensure you're using a recent version of PowerPoint

### Custom Width- Check that the GIF plays correctly in a web browser first

```bash- Some very large GIFs may not display properly - try reducing file size

python gif_worker.py --mp4 video.mp4 --width 500

```**Videos don't stitch together properly:**

Height is automatically calculated to maintain aspect ratio- Check that all input videos have similar frame rates

- Ensure videos are not corrupted

### Combine Settings- Try converting videos to the same format/codec before processing

```bash- Use `--width` parameter to force consistent dimensions
python gif_worker.py --mp4 *.mp4 --output slideshow.gif --quality medium --fps 12 --width 600
```

---

## 📊 Use Cases

### 🎤 **Conference Presentations**
Combine intro, main content, and Q&A slides into one looping GIF:
```bash
python gif_worker.py --mp4 intro.mp4 content.mp4 outro.mp4 --output conference.gif
```

### 📧 **Email Campaigns**
Create small, optimized GIFs for email:
```bash
python gif_worker.py --mp4 product_demo.mp4 --quality low --width 400
```

### 🌐 **Web Graphics**
Batch process social media content:
```bash
python gif_worker.py --batch *.mp4 --mp4 --quality medium --width 600
```

### 🎬 **Demo Videos**
High-quality product demonstrations:
```bash
python gif_worker.py --mp4 feature1.mp4 feature2.mp4 feature3.mp4 --quality high
```

---

## 🛠️ Troubleshooting

### "Module not found" error
```bash
pip install Pillow moviepy
```

### MoviePy installation issues (Windows)
```bash
pip install --upgrade pip
pip install moviepy[optional]
```

### Virtual environment not activating
```powershell
# Make sure you're in the project folder
cd "path\to\GIF creator"

# Then activate
gif_env\Scripts\activate

# You should see (gif_env) in your terminal prompt
```

### File size too large
- Use `--quality low` option
- Reduce width: `--width 400` or smaller
- Lower FPS: `--fps 8` or less
- Split long videos into shorter segments

### GIF doesn't loop in PowerPoint
- Save PowerPoint as .pptx format
- Ensure you're using a recent PowerPoint version
- Test the GIF in a web browser first
- Try reducing file size if very large

### Videos don't stitch together properly
- Ensure all videos have similar frame rates
- Check that videos aren't corrupted
- Use `--width` parameter to force consistent dimensions
- Convert videos to the same format first

### GUI doesn't launch
- Make sure tkinter is installed (usually included with Python)
- Try the command-line version instead
- Check that Python 3.7+ is installed

---

## 📋 Command Reference

### GIF Worker GUI
```bash
python gif_worker_gui.py
```
Launches the graphical interface

### GIF Worker CLI

**Interactive Mode:**
```bash
python gif_worker.py
```
No arguments launches the interactive menu

**MP4 to GIF:**
```bash
python gif_worker.py --mp4 FILE [FILE ...] [OPTIONS]
```

**Loop GIF:**
```bash
python gif_worker.py --loop FILE [OPTIONS]
```

**Batch Process:**
```bash
python gif_worker.py --batch FILE [FILE ...] [OPTIONS]
```

**Options:**
- `--output, -o FILE` - Specify output filename
- `--fps N` - Frames per second (default: based on quality)
- `--width PIXELS` - Width in pixels (height auto-calculated)
- `--quality {low,medium,high}` - Quality preset (default: medium)
- `--version` - Show version information
- `--help` - Show help message

---

## 💡 Tips & Best Practices

### For Best Quality:
- Use `--quality high` for important presentations
- Keep original video resolution when possible
- Use 15 FPS for smooth animations

### For Smaller Files:
- Use `--quality low` for email/web
- Reduce `--width` to 400-600 pixels
- Lower FPS to 8 frames per second
- Keep videos short (under 30 seconds)

### For PowerPoint:
- **Recommended**: Medium quality, 10 FPS, 600px width
- Keep files under 10MB for smooth playback
- Test in slideshow mode before presenting
- Use consistent dimensions for multiple GIFs on same slide

### For Email/Web:
- **Recommended**: Low quality, 8 FPS, 400px width
- Aim for files under 3MB
- Test loading time in email clients
- Consider shorter loops for faster loading

---

## 📝 Technical Details

### What the Tools Do

**MP4 to GIF Conversion:**
1. Loads MP4 video(s) using MoviePy
2. Stitches multiple videos together (if applicable)
3. Resizes to target dimensions
4. Converts to GIF format with optimized settings
5. Sets loop count to 0 (infinite loops)
6. Provides optimization suggestions

**GIF Looping:**
1. Opens the input GIF file
2. Extracts all frames and timing information
3. Saves with loop count set to 0 (infinite loops)
4. Optimizes file size

**Batch Processing:**
- Processes each file individually
- Auto-generates output names
- Provides success/failure statistics
- Continues processing even if one file fails

---

## 🤝 Support

Having issues? Here are some solutions:

1. **Check the virtual environment is activated** - Look for `(gif_env)` in your prompt
2. **Verify dependencies** - Run `pip list` to see installed packages
3. **Try the GUI** - Sometimes easier than command-line
4. **Check file paths** - Use quotes around paths with spaces
5. **Test with a small file first** - Ensure everything works before batch processing

---

## 📄 License

This project is provided as-is for creating GIFs for presentations and personal use.

---

## 🎉 Credits

Created to simplify the process of creating professional, looping GIFs for PowerPoint presentations.

**Technologies Used:**
- Python 3.7+
- MoviePy (video processing)
- Pillow (image processing)
- tkinter (GUI)

---

**Ready to create amazing presentation GIFs? Launch the GUI and get started!**

```powershell
python gif_worker_gui.py
```
