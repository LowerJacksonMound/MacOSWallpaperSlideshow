---
layout: page
title: "MacOSWallpaperSlideshow"
description: “Simple Python script which allows user to select wallpaper images, frequency of wallpaper image change, and resolution of wallpaper image.

permalink: /MacOSWallpaperSlideshow/
---

# MacOSWallpaperSlideshow

This project is a script designed to change your MacOS wallpaper at a specified frequency. Below are instructions on how to set it up and run it on your device.

## Features

- Feature 1: Choose wallpaper change frequency.
- Feature 2: Select wallpaper image size.
- Feature 3: Select images for wallpaper.

## Requirements

- Python>=3.10
- Pillow>=8.0

## Installation

### Step 1: Clone the Repository: git clone <https://github.com/LowerJacksonMound/>

### Step 2: cd MacOSWallpaperSlideshow

### Step 3: pip3 install -r requirements.txt

Usage:
python3 slideshow.py -d /path/to/image/directory -t 15 -r 1920x1080

-d or --directory: Path to the directory containing the images.
-t or --transition-time: Time in seconds between image transitions (default is 10 seconds).
-r or --resolution: Display resolution (optional). If not specified, the script will attempt to get the current screen resolution.
