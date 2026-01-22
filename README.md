## MP4 Time-Lapse Generator (Python)

This script converts a folder of sequential images into an `.mp4` time-lapse video using OpenCV. It supports natural filename sorting, multiple image formats, optional resizing, and configurable frame rates.

---

## Features

- ✅ Natural sorting (`img2.png` → `img10.png`)
- ✅ Supports common image formats (`jpg`, `png`, `tif`, `bmp`, `webp`)
- ✅ Optional frame resizing (e.g. `1920x1080`)
- ✅ Adjustable frames-per-second (FPS)
- ✅ Skips unreadable or corrupt images safely
- ✅ Outputs a standard `.mp4` video

---

## Requirements

- Python 3.9+
- OpenCV

Install dependencies:

```bash
pip install opencv-python
