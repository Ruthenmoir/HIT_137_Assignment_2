"""We used the following video series from youtube as tutorials:
 https://www.youtube.com/playlist?list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV
 https://www.youtube.com/playlist?list=PLpMixYKO4EXeaGnqT_YWx7_mA77bz2VqM
 """

from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk


class image_manager:
    """Manages image processing operations such as opening, resizing, cropping, and saving images.

    Attributes:
        original_image (PIL.Image): The currently loaded image for processing.
        image_canvas (tkinter.Canvas): Canvas widget to display the image.
        status_label (tkinter.Label): Label to display status messages.
        gui (gui): Reference to the GUI manager for accessing sliders and root window.
        photo (ImageTk.PhotoImage): Tkinter-compatible image for display.
        is_cropping (bool): Flag indicating if cropping mode is active.
        crop_rect (int): Canvas rectangle ID for the crop selection.
        history (list): List of image states for undo/redo (max 10).
        history_index (int): Current position in the history list.
        initial_image (PIL.Image): Copy of the original image for reset.
    """
    def __init__(self, image_canvas, status_label, gui):
        self.original_image = None
        self.image_canvas = image_canvas
        self.status_label = status_label
        self.photo = None
        self.gui = gui
        self.is_cropping = False 
        self.crop_rect = None    
        self.history = []
        self.history_index = -1
        self.initial_image = None
        self.displayed_image_size = None

    def open_image(self):
        """Opens an image file and displays it on the canvas.

        Uses a file dialog to select an image, resizes it for display while preserving
        the original, and updates GUI sliders with image dimensions.
        """
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),("All files", "*.*")))
        if filepath:
            self.status_label.config(text=f"Opening image: {filepath}")
            self.original_image = Image.open(filepath)
            self.initial_image = self.original_image.copy()  # Store initial state for reset
            
            # Calculate new dimensions with width = 1000, maintaining aspect ratio
            orig_width, orig_height = self.original_image.size
            new_width = min(1000, orig_width)
            new_height = int((new_width / orig_width) * orig_height)
            
            # Resize image for display
            display_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Update sliders with original image dimensions
            self.gui.width_slider.set(orig_width)
            self.gui.height_slider.set(orig_height)
            self.gui.width_slider.config(state="normal")
            self.gui.height_slider.config(state="normal")
            
            # Display the resized image
            self.display_image(display_image)
        else:
            self.gui.width_slider.config(state="disabled")
            self.gui.height_slider.config(state="disabled")
            self.status_label.config(text="No image loaded")

    def display_image(self, image):
        """Displays the provided image on the canvas.

        Args:
            image (PIL.Image): The image to display.

        Updates the canvas size, scroll region, and status label with image details.
        Handles exceptions to prevent crashes from invalid images.
        """
        try:
            image_width, image_height = image.size
            self.photo = ImageTk.PhotoImage(image)
            self.image_canvas.delete("all")   # Clear previous content
            self.image_canvas.create_image(0, 0, image=self.photo, anchor=NW)
            # Set canvas size and scroll region to match image
            self.image_canvas.config(width=image_width, height=image_height)
            self.image_canvas.config(scrollregion=(0, 0, image_width, image_height))
            self.displayed_image_size = (image_width, image_height)
            
            # Update sliders with original image dimensions if original_image exists
            if self.original_image:
                orig_width, orig_height = self.original_image.size
                self.gui.width_slider.set(orig_width)
                self.gui.height_slider.set(orig_height)
                self.status_label.config(text=f"Image displayed ({image_width}x{image_height}), original size: ({orig_width}x{orig_height})")
            else:
                self.status_label.config(text=f"Image displayed ({image_width}x{image_height})")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def resize_image(self, new_width, new_height):
        """Resizes the original image to the specified dimensions.

        Args:
            new_width (int): Desired width in pixels.
            new_height (int): Desired height in pixels.

        Saves the current state to history, resizes the image, and updates the display.
        """
        try:
            if self.original_image:
                self.save_to_history()
                self.original_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
                display_width = min(1000, new_width)
                display_height = int((display_width / new_width) * new_height)
                display_image = self.original_image.resize((display_width, display_height), Image.LANCZOS)
                self.display_image(display_image)
                self.status_label.config(text=f"Image resized to: {new_width} x {new_height}")
            else:
                self.status_label.config(text="No image loaded")
        except Exception as e:
            self.status_label.config(text=f"Error resizing image: {e}")
            
    def prompt_resize(self):
        """Prompts the user for new dimensions and resizes the image. 
           Only used in the menu option of resizing
           """
        if self.original_image:
            new_width = simpledialog.askinteger("Resize", "Enter new width:", parent=self.image_canvas.master, minvalue=1)
            if new_width is None:
                return
            new_height = simpledialog.askinteger("Resize", "Enter new height:", parent=self.image_canvas.master, minvalue=1)
            if new_height is None:
                return
            self.resize_image(new_width, new_height)
        else:
            self.status_label.config(text="No image loaded")

    def save_file(self):
        """Saves the current image to a file.

            Opens a save dialog to specify the file path and format (PNG or JPEG).
            """
        if self.original_image:
            filepath = filedialog.asksaveasfilename(
                initialfile = 'Untitled.png', 
                defaultextension= ".png", 
                filetypes = [("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All Files", "*.*")])
       
            if filepath:
                try:
                    self.original_image.save(filepath)
                    self.status_label.config(text=f"Image saved to {filepath}")
                except Exception as e:
                    self.status_label.config(text=f"Error saving image: {e}")
            else: 
                self.status_label.config(text="Save cancelled")
        else:
            self.status_label.config(text="No image loaded")

    def save_to_history(self):
        """Saves the current image state to the history for undo/redo.

        Maintains a maximum of 10 history states, removing the oldest if exceeded.
        """
        if self.original_image:
            self.history = self.history[:self.history_index + 1] 
            self.history.append(self.original_image.copy())  
            self.history_index += 1            
            if len(self.history) > 10:    # Limit history to 10 states to manage memory
                self.history.pop(0)
                self.history_index -= 1

    def undo(self):
        """Reverts to the previous image state in the history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.original_image = self.history[self.history_index].copy()
            self.display_image(self.original_image)
            self.status_label.config(text="Undo performed")
        else:
            self.status_label.config(text="Nothing to undo")
    
    def redo(self):
        """Restores the next image state in the history."""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.original_image = self.history[self.history_index].copy()
            self.display_image(self.original_image)
            self.status_label.config(text="Redo performed")
        else:
            self.status_label.config(text="Nothing to redo")

    def start_crop(self):
        """Initiates cropping mode, allowing the user to select a crop area."""
        if self.original_image:
            self.save_to_history()
            self.is_cropping = True
            self.status_label.config(text="Click and drag to select crop area")
            self.image_canvas.config(cursor="crosshair")
            self.image_canvas.bind("<Button-1>", self.crop_mouse_press)
            self.image_canvas.bind("<B1-Motion>", self.crop_mouse_drag)
            self.image_canvas.bind("<ButtonRelease-1>", self.crop_mouse_release)
            self.image_canvas.bind("<Escape>", self.cancel_crop)
        else:
            self.status_label.config(text="No image loaded")   

    def crop_mouse_press(self, event):
        """Handles the start of a crop selection when the mouse is pressed.

        Args:
            event: Tkinter event with mouse coordinates.
        """
        if self.is_cropping:
            self.crop_start_x = event.x
            self.crop_start_y = event.y
            if self.crop_rect:
                self.image_canvas.delete(self.crop_rect) # Remove previous rectangle
             # Create a dashed red rectangle for crop selection
            self.crop_rect = self.image_canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_start_x, self.crop_start_y, outline="red", dash=(4, 4))

    def crop_mouse_drag(self, event):
        """Updates the crop rectangle as the mouse is dragged.

        Args:
            event: Tkinter event with mouse coordinates.
        """
        if self.is_cropping and self.crop_rect:
            img_width, img_height = self.displayed_image_size
            x = max(0, min(event.x, img_width))
            y = max(0, min(event.y, img_height))
            self.image_canvas.coords(self.crop_rect, self.crop_start_x, self.crop_start_y, x, y)

    def crop_mouse_release(self, event):
        """Finalizes the crop operation when the mouse is released.

        Args:
            event: Tkinter event with mouse coordinates.

        Scales crop coordinates from display to original image size and applies the crop.
        Displays a comparison window with original and cropped images.
        """
        if self.is_cropping:
            end_x, end_y = event.x, event.y
            # Ensure coordinates are within image bounds
            img_width, img_height = self.displayed_image_size
            x1, y1 = max(0, min(self.crop_start_x, end_x)), max(0, min(self.crop_start_y, end_y))
            x2, y2 = min(img_width, max(self.crop_start_x, end_x)), min(img_height, max(self.crop_start_y, end_y))
            if x2 > x1 and y2 > y1:
                # Scale coordinates back to original image size
                display_width, display_height = img_width, img_height
                orig_width, orig_height = self.original_image.size
                scale_x = orig_width / display_width
                scale_y = orig_height / display_height
                crop_box = (int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y))
                 # Apply crop to original image
                cropped_image = self.original_image.crop(crop_box)
                # Update the main canvas with the cropped image
                self.original_image = cropped_image
                self.display_image(self.original_image)
                self.status_label.config(text=f"Image cropped to {crop_box}")
                try:
                    # Use initial_image for the original or history[-2] for the pre-crop image
                    original_image = self.initial_image if self.initial_image else self.history[-2]
                    self.display_comparison(original_image, cropped_image)
                except Exception as e:
                    self.status_label.config(text=f"Error displaying comparison: {e}")
            else:
                self.status_label.config(text="Invalid crop area")
            # Clean up
            self.image_canvas.delete(self.crop_rect)
            self.crop_rect = None
            self.is_cropping = False
            self.image_canvas.config(cursor="")
            self.image_canvas.unbind("<Button-1>")
            self.image_canvas.unbind("<B1-Motion>")
            self.image_canvas.unbind("<ButtonRelease-1>")

    def display_comparison(self, original_image, cropped_image):
            """Displays a side-by-side comparison of original and cropped images.

            Args:
                original_image (PIL.Image): The original image before cropping.
                cropped_image (PIL.Image): The cropped image.
            """
            try: 
                comparison_window = Toplevel(self.gui.root)              # Create a new window for comparison
                comparison_window.title("Original vs Cropped Image")
                comparison_window.geometry("1200x600")  # Set window size
                original_frame = Frame(comparison_window)           # Create frames for layout
                original_frame.pack(side=LEFT, padx=10, pady=10)
                cropped_frame = Frame(comparison_window)
                cropped_frame.pack(side=LEFT, padx=10, pady=10)
                Label(original_frame, text="Original Image").pack()              # Labels for clarity
                Label(cropped_frame, text="Cropped Image").pack()
                original_canvas = Canvas(original_frame, bg="white", bd=1, relief="sunken")      # Create canvases
                original_canvas.pack()
                cropped_canvas = Canvas(cropped_frame, bg="white", bd=1, relief="sunken")
                cropped_canvas.pack()
                max_size = 500              # Maximum size for displayed images
                orig_photo = self.scale_image(original_image, max_size) # Scale images to fit within a max size 
                crop_photo = self.scale_image(cropped_image, max_size)
                orig_width, orig_height = orig_photo.width(), orig_photo.height()   # Update canvas sizes
                crop_width, crop_height = crop_photo.width(), crop_photo.height()
                original_canvas.config(width=orig_width, height=orig_height)
                cropped_canvas.config(width=crop_width, height=crop_height)
                original_canvas.create_image(0, 0, image=orig_photo, anchor="nw")  # Display images on canvases
                cropped_canvas.create_image(0, 0, image=crop_photo, anchor="nw") 
                original_canvas.image = orig_photo  # Keep references to PhotoImage objects to prevent garbage collection
                cropped_canvas.image = crop_photo
                Button(comparison_window, text="Close", command=comparison_window.destroy).pack(pady=10)
            except Exception as e:
                self.status_label.config(text=f"Error in comparison window: {e}")
                if 'comparison_window' in locals():
                    comparison_window.destroy()

    def cancel_crop(self, event):
        """Cancels the cropping operation when Escape is pressed.

        Args:
            event: Tkinter event (unused).
        """
        if self.is_cropping:
            self.image_canvas.delete(self.crop_rect)
            self.crop_rect = None
            self.is_cropping = False
            self.image_canvas.config(cursor="")
            self.image_canvas.unbind("<Button-1>")
            self.image_canvas.unbind("<B1-Motion>")
            self.image_canvas.unbind("<ButtonRelease-1>")
            self.status_label.config(text="Crop cancelled")

    def reset_image(self): 
        """Resets the image to its initial state."""
        if self.initial_image:
            self.original_image = self.initial_image.copy()
            self.history = [self.original_image.copy()]
            self.history_index = 0
            orig_width, orig_height = self.original_image.size
            new_width = min(1000, orig_width)
            new_height = int((new_width / orig_width) * orig_height)
            display_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.display_image(display_image)
            self.status_label.config(text="Image reset to original")
        else:
            self.status_label.config(text="No image loaded")

    def scale_image(self, image, max_size):  
        """Scales an image to fit within a maximum size while preserving aspect ratio.

        Args:
            image (PIL.Image): The image to scale.
            max_size (int): Maximum width or height in pixels.

        Returns:
            ImageTk.PhotoImage: Tkinter-compatible scaled image.
        """
     
        image_width, image_height = image.size  
        if image_width > max_size or image_height > max_size:
            # Calculate scaling factor to fit within max_size
            scale = min(max_size / image_width, max_size / image_height)
            new_width = int(image_width * scale)
            new_height = int(image_height * scale)
            image = image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def convert_to_grayscale(self):
        """Converts the current image to grayscale."""
        if self.original_image:
            try:
                self.save_to_history()
                # Convert to grayscale using PIL
                self.original_image = self.original_image.convert('L')
                # Update display (resize to fit canvas if needed)
                orig_width, orig_height = self.original_image.size
                new_width = min(1000, orig_width)
                new_height = int((new_width / orig_width) * orig_height)
                display_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
                self.display_image(display_image)
                self.status_label.config(text="Image converted to grayscale")
            except Exception as e:
                self.status_label.config(text=f"Error converting to grayscale: {e}")
        else:
            self.status_label.config(text="No image loaded")




class gui:
    """Manages the graphical user interface for the image manipulator.

    Attributes:
        root (tkinter.Tk): The main application window.
        image_canvas (tkinter.Canvas): Canvas for displaying images.
        status_label (tkinter.Label): Label for status messages.
        image_mgr (image_manager): Reference to the image manager.
        width_slider (tkinter.Scale): Slider for setting image width.
        height_slider (tkinter.Scale): Slider for setting image height.
    """

    def __init__(self, root):
        """Initializes the GUI with a menu, toolbar, canvas, and sliders."""
        self.root = root
        self.root.title("Group 2, Assignment 3")

        self.banner = Label(root, text="Group 2 Image Manipulator", font=("Helvetica", 16, "bold"), bg="#f0f0f0", pady=10)
        self.banner.pack(side=TOP, fill=X)

        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the scrollable canvas
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(side=RIGHT, pady=10, expand=True, fill=BOTH)

        # Add scrollbars
        self.h_scrollbar = Scrollbar(self.canvas_frame, orient=HORIZONTAL)
        self.h_scrollbar.pack(side=BOTTOM, fill=X)
        self.v_scrollbar = Scrollbar(self.canvas_frame, orient=VERTICAL)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)

        # Create the canvas
        self.image_canvas = Canvas(self.canvas_frame, bg="white", bd=1, relief=SUNKEN, xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.image_canvas.pack(side=LEFT, expand=True, fill=BOTH)

        # Configure scrollbars
        self.h_scrollbar.config(command=self.image_canvas.xview)
        self.v_scrollbar.config(command=self.image_canvas.yview)

        self.status_label = Label(root, text="No image loaded", fg="blue", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=BOTTOM, fill=X)
        self.image_mgr = image_manager(self.image_canvas, self.status_label, self)

        self.create_menu()
        self.create_toolbar()



    def create_menu(self):
        """Creates the menu bar with File and Edit options."""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)


        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", accelerator="Ctrl+O",  command=self.image_mgr.open_image)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.image_mgr.save_file)
        file_menu.add_command(label="Save As", command=self.image_mgr.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)

        edit_menu = Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.image_mgr.undo)  
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.image_mgr.redo)
        edit_menu.add_command(label="Reset Image", accelerator="Ctrl+Shift+R", command=self.image_mgr.reset_image)  
        edit_menu.add_command(label="Crop Image", accelerator="Ctrl+C",  command=self.image_mgr.start_crop)   
        edit_menu.add_command(label="Resize Image", accelerator="Ctrl+R", command=self.image_mgr.prompt_resize)   
        edit_menu.add_command(label="Grayscale", accelerator="Ctrl+G", command=self.image_mgr.convert_to_grayscale)

    def create_toolbar(self):
        """Creates the toolbar with buttons and resize sliders."""
        toolbar = Frame(self.main_frame, bg="#f0f0f0", bd=1, relief=GROOVE, width=220)
        toolbar.pack(side=RIGHT, fill=Y, padx=5, pady=5)

    

        #Button style
        button_style = {"bg": "#d3d3d3", "relief": FLAT, "padx": 10, "pady": 8, "width": 14, "font": ("Helvetica", 12)}


      # Button configurations: (text_color, text, command)
        button_configs = [
            ("#0066CC", "Open", self.image_mgr.open_image),  # Blue for Open
            ("#009900", "Save", self.image_mgr.save_file),    # Green for Save
            ("#FF6600", "Undo", self.image_mgr.undo),         # Orange for Undo
            ("#CC9900", "Redo", self.image_mgr.redo),         # Yellow for Redo
            ("#CC0000", "Crop", self.image_mgr.start_crop),  # Red for Crop
            ("#666666", "Grayscale", self.image_mgr.convert_to_grayscale),  # Gray for Grayscale
            ("#660099", "Help", self.show_help),             # Purple for Help
            ]

        # Create buttons with colored icons
        for text_color, text, command in button_configs:
            row_frame = Frame(toolbar, bg="#f0f0f0")  
            row_frame.pack(pady=4, anchor="center")  
            Button(row_frame, text=text, command=command, fg=text_color, **button_style).pack(side=LEFT, padx=10)

       # Separator for visual clarity
        separator = Frame(toolbar, height=2, bg="#d3d3d3")
        separator.pack(fill=X, pady=5)

       # Resize Controls label
        Label(toolbar, text="Resize Controls", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=8)

        # Height slider
        height_frame = Frame(toolbar, bg="#f0f0f0")
        height_frame.pack(pady=5)
        Label(height_frame, text="Height", bg="#f0f0f0").pack()
        self.height_slider = Scale(height_frame, from_=1, to=1000, orient=VERTICAL, length=150, command=self.height_slide, state="disabled")
        self.height_slider.pack()

        # Width slider
        width_frame = Frame(toolbar, bg="#f0f0f0")
        width_frame.pack(pady=5)
        Label(width_frame, text="Width", bg="#f0f0f0").pack()
        self.width_slider = Scale(width_frame, from_=1, to=1000, orient=HORIZONTAL, length=150, command=self.width_slide, state="disabled")
        self.width_slider.pack()

    def width_slide(self, value):
        """Handles width slider changes to resize the image.

        Args:
            value (str): Slider value (converted to int).

        Debounces rapid slider changes using a 200ms delay.
        """
        if self.image_mgr.original_image:
            try:
                if hasattr(self, '_resize_timer'):
                    self.root.after_cancel(self._resize_timer)
                def resize():
                    new_width = int(self.width_slider.get())
                    new_height = int(self.height_slider.get())
                    self.image_mgr.resize_image(new_width, new_height)
                self._resize_timer = self.root.after(200, resize)
            except Exception as e:
                self.status_label.config(text=f"Error resizing: {e}")
        else:
            self.status_label.config(text="No image loaded")     

    def height_slide(self, value):
        """Handles height slider changes to resize the image.

        Args:
            value (str): Slider value (converted to int).

        Debounces rapid slider changes using a 200ms delay.
        """
        if self.image_mgr.original_image:
            try:
                if hasattr(self, '_resize_timer'):
                    self.root.after_cancel(self._resize_timer)
                def resize():
                    new_height = int(self.height_slider.get())
                    new_width = int(self.width_slider.get())
                    self.image_mgr.resize_image(new_width, new_height)
                self._resize_timer = self.root.after(200, resize)
            except Exception as e:
                self.status_label.config(text=f"Error resizing: {e}")
        else:
            self.status_label.config(text="No image loaded")

    def show_help(self):
        """Displays a window listing all keyboard shortcuts."""
        help_window = Toplevel(self.root)
        help_window.title("Keyboard Shortcuts")
        help_window.geometry("400x400")
        help_window.resizable(False, False)

        # Title
        Label(help_window, text="Keyboard Shortcuts", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Frame for shortcuts
        shortcuts_frame = Frame(help_window)
        shortcuts_frame.pack(padx=10, pady=5, fill="both")

        # List of shortcuts
        shortcuts = [
            ("Ctrl+O", "Open Image", "Opens a new image file"),
            ("Ctrl+S", "Save", "Saves the current image"),
            ("Ctrl+Q", "Exit", "Closes the application"),
            ("Ctrl+Z", "Undo", "Reverts the last operation"),
            ("Ctrl+Y", "Redo", "Restores the last undone operation"),
            ("Ctrl+Shift+R", "Reset Image", "Resets to the original image"),
            ("Ctrl+C", "Crop Image", "Starts cropping mode"),
            ("Ctrl+R", "Resize Image", "Prompts for new dimensions"),
            ("Ctrl+G", "Grayscale", "Converts image to grayscale"),
        ]

        # Display shortcuts in a grid
        for i, (shortcut, action, description) in enumerate(shortcuts):
            Label(shortcuts_frame, text=shortcut, font=("Helvetica", 10), anchor="w").grid(row=i, column=0, padx=5, pady=2, sticky="w")
            Label(shortcuts_frame, text=action, font=("Helvetica", 10), anchor="w").grid(row=i, column=1, padx=5, pady=2, sticky="w")
            Label(shortcuts_frame, text=description, font=("Helvetica", 10), anchor="w").grid(row=i, column=2, padx=5, pady=2, sticky="w")

        # Close button
        Button(help_window, text="Close", command=help_window.destroy, font=("Helvetica", 10)).pack(pady=10)

root = Tk()
app = gui(root)


# Event handlers for keyboard shortcuts
def open_image_event(event):
    """Handles Ctrl+O to open an image."""
    app.image_mgr.open_image()

def save_image_event(event):
    """Handles Ctrl+S to save the image."""
    app.image_mgr.save_file()

def quit_event(event):
    """Handles Ctrl+Q to exit the application."""
    root.quit()

def undo_event(event):
    """Handles Ctrl+Z to undo the last operation."""
    app.image_mgr.undo()

def redo_event(event):
    """Handles Ctrl+Y to redo the last undone operation."""
    app.image_mgr.redo()

def resize_image_event(event):
    """Handles Ctrl+R to prompt for resize dimensions."""
    app.image_mgr.prompt_resize()

def crop_image_event(event):
    """Handles Ctrl+C to start cropping."""
    app.image_mgr.start_crop()

def reset_image_event(event):
    """Handles Ctrl+Shift+R to reset the image."""
    app.image_mgr.reset_image()

def grayscale_event(event):
    """Handles Ctrl+G to convert the image to grayscale."""
    app.image_mgr.convert_to_grayscale()

root.bind("<Control-o>", open_image_event)
root.bind("<Control-s>", save_image_event)
root.bind("<Control-q>", quit_event)
root.bind("<Control-z>", undo_event)
root.bind("<Control-y>", redo_event)
root.bind("<Control-r>", resize_image_event)
root.bind("<Control-c>", crop_image_event)
root.bind("<Control-Shift-R>", reset_image_event)
root.bind("<Control-g>", grayscale_event)



root.mainloop()







