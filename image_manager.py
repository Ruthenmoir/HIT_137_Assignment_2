"""We used the following video series from YouTube as tutorials:
 https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV
 https://www.youtube.com/playlist?list=PLpMixYKO4EXeaGnqT_YWx7_mA77bz2VqM
 """

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageManager:
    """
    This class manages the image manipulation operations, including opening, saving, resizing, scaling and grayscaling
    images.
    """

    def __init__(self):
        self.status = ""

    def open_image(self):
        """Opens an image file and displays it on the canvas.

        Uses a file dialog to select an image, resizes it for display while preserving
        the original, and updates GUI sliders with image dimensions.
        """
        filepath = filedialog.askopenfilename(title="Select Image",
                                              filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),
                                                         ("All files", "*.*")))
        if filepath:
            self.status = f"Opening image: {filepath}"
            image = Image.open(filepath)

            # Calculate new dimensions with width = 1000, maintaining aspect ratio
            orig_width, orig_height = image.size
            new_width = min(1000, orig_width)
            new_height = int((new_width / orig_width) * orig_height)

            # Resize image for display
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Return the resized image
            return display_image
        else:
            self.status = "No image loaded"
            return None

    def save_file(self, image):
        """Saves the current image to a file.

            Opens a save dialog to specify the file path and format (PNG or JPEG).
            """
        filepath = filedialog.asksaveasfilename(
            initialfile='Untitled.png',
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All Files", "*.*")])

        if filepath:
            try:
                image.save(filepath)
                self.status = f"Image saved to {filepath}"
            except Exception as e:
                self.status = f"Error saving image: {e}"
        else:
            self.status = "Save cancelled"

    def resize_image(self, original_image, new_width, new_height) -> Image:
        """
        Resizes the original image to the specified dimensions.
        Saves the current state to history, resizes the image, and updates the display.

        :param original_image: Image to resize.
        :param new_width: Desired width in pixels.
        :param new_height: Desired height in pixels.
        :return: Resized image.
        """

        try:
            display_width = min(1000, new_width)
            display_height = int((display_width / new_width) * new_height)
            display_image = original_image.resize((display_width, display_height), Image.Resampling.LANCZOS)
            self.status = f"Image resized to: {new_width} x {new_height}"
            return display_image
        except Exception as e:
            self.status = f"Error resizing image: {e}"
            return None

    def scale_image(self, image: Image, max_size: int) -> PhotoImage:
        """
        Scales an image to fit within a maximum size while preserving aspect ratio.

        :param image: The image to scale
        :param max_size: Maximum width or height in pixels
        :return: Tkinter-compatible scaled image
        """

        image_width, image_height = image.size
        if image_width > max_size or image_height > max_size:
            # Calculate scaling factor to fit within max_size
            scale = min(max_size / image_width, max_size / image_height)
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def convert_to_grayscale(self, original_image):
        """Converts the current image to grayscale."""
        try:
            # Convert to grayscale using PIL
            original_image = original_image.convert('L')

            # Update display (resize to fit canvas if needed)
            orig_width, orig_height = original_image.size
            new_width = min(1000, orig_width)
            new_height = int((new_width / orig_width) * orig_height)
            display_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.status = "Image converted to grayscale"
            return display_image
        except Exception as e:
            self.status = f"Error converting to grayscale: {e}"
            return None
