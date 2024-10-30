import os
import sys
import subprocess
import argparse
import signal
from PIL import Image

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Wallpaper slideshow script for macOS')
    parser.add_argument('-d', '--directory', required=True, help='Directory containing images to use as wallpaper')
    parser.add_argument('-t', '--transition-time', type=int, default=10, help='Time in seconds to transition between images')
    parser.add_argument('-r', '--resolution', help='Resolution of the display (e.g. "1920x1080")')
    parser.add_argument('--original-size', action='store_true', help='Display images at their original size')
    return parser.parse_args()

def get_display_resolution():
    """Get the display resolution using system_profiler."""
    try:
        output = subprocess.check_output(['system_profiler', 'SPDisplaysDataType']).decode('utf-8')
        for line in output.splitlines():
            if "Resolution" in line:
                # Extract resolution using more robust parsing
                parts = line.split()
                if len(parts) >= 3:
                    width = parts[1].strip()
                    height = parts[3].strip()
                    resolution = f"{width}x{height}"
                    return resolution
        # Fallback if no resolution was found
        print("Could not detect display resolution. Please specify with '-r WIDTHxHEIGHT'.")
        sys.exit(1)
    except (subprocess.CalledProcessError, IndexError) as e:
        print(f"Error fetching display resolution: {e}")
        sys.exit(1)

def create_centered_image(image_path, width, height):
    """Create a new image with the original image centered on a canvas of the specified size."""
    try:
        with Image.open(image_path) as img:
            # Create a new image with the specified background color and size
            new_img = Image.new("RGB", (width, height), (0, 0, 0))  # Black background for visibility
            # Calculate position to center the original image
            x_offset = (width - img.width) // 2
            y_offset = (height - img.height) // 2
            # Paste the original image onto the new background
            new_img.paste(img, (x_offset, y_offset))
            # Save the new image to a temporary file
            tmp_filename = os.path.join('/tmp', f'centered_{os.path.basename(image_path)}')
            new_img.save(tmp_filename)
            return tmp_filename
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def setup_slideshow(images, transition_time):
    """Set up the slideshow using AppleScript."""
    images_str = ", ".join([f'"{img}"' for img in images])
    slideshow_script = f'''
    tell application "System Events"
        set the_images to {{{images_str}}}
        set the_transition_time to {transition_time}

        repeat with i from 1 to count of the_images
            set the_image to item i of the_images
            tell application "Finder"
                set desktop picture to POSIX file the_image
            end tell
            delay the_transition_time
        end repeat
    end tell
    '''
    return slideshow_script

def execute_slideshow(slideshow_script):
    """Execute the AppleScript for the slideshow."""
    try:
        subprocess.run(['osascript', '-e', slideshow_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing slideshow: {e}")
        sys.exit(1)

def clean_up(images):
    """Clean up temporary image files."""
    for img in images:
        try:
            os.remove(img)
        except OSError as e:
            print(f"Error removing temporary file {img}: {e}")

def signal_handler(sig, frame):
    """Handle interrupt signal for graceful shutdown."""
    print("\nSlideshow interrupted. Exiting...")
    sys.exit(0)

def main():
    # Set up signal handling for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Parse command-line arguments
    args = parse_arguments()

    # Determine the resolution to use
    resolution = args.resolution or get_display_resolution()
    try:
        width, height = map(int, resolution.split('x'))
    except ValueError:
        print("Invalid resolution format. Please use 'WIDTHxHEIGHT' format.")
        sys.exit(1)

    # Verify the image directory exists
    if not os.path.isdir(args.directory):
        print(f"Directory not found: {args.directory}")
        sys.exit(1)

    # Process images in the directory
    images = []
    for filename in os.listdir(args.directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
            image_path = os.path.join(args.directory, filename)
            if args.original_size:
                # Create a centered image on a canvas matching the screen resolution
                centered_image = create_centered_image(image_path, width, height)
                if centered_image:
                    images.append(centered_image)
            else:
                images.append(image_path)

    if not images:
        print("No valid images found in the specified directory.")
        sys.exit(1)

    # Generate the slideshow script
    slideshow_script = setup_slideshow(images, args.transition_time)

    # Execute the slideshow
    try:
        print("Starting slideshow... Press Ctrl+C to exit.")
        execute_slideshow(slideshow_script)
    finally:
        # Clean up temporary files
        clean_up(images)

if __name__ == '__main__':
    main()
