from tkinter import *
from tkinter import simpledialog

from PIL import ImageTk
from PIL import Image

from history_manager import HistoryManager
from image_manager import ImageManager


class Gui:
    """This class manages the graphical user interface for the image manipulator.

    Attributes:
        root (tkinter.Tk): The main application window.
        image_canvas (tkinter.Canvas): Canvas for displaying images.
        status_label (tkinter.Label): Label for status messages.
        image_mgr (image_manager): Reference to the image manager.
        history_mgr (image_manager): Reference to the history manager.
        width_slider (tkinter.Scale): Slider for setting image width.
        height_slider (tkinter.Scale): Slider for setting image height.
    """

    def __init__(self, root):
        """Initializes the GUI with a menu, toolbar, canvas, and sliders."""
        self.root = root
        self.root.title("Group 2, Assignment 3")

        self.banner = Label(root, text="Group 2 Image Manipulator", font=("Helvetica", 16, "bold"), bg="#f0f0f0",
                            pady=10)
        self.banner.pack(side="top", fill="x")

        self.main_frame = Frame(self.root)
        self.main_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.photo = None

        # Create a frame for the scrollable canvas
        self.canvas_frame = Frame(self.main_frame)
        self.canvas_frame.pack(side="right", pady=10, expand=True, fill="both")

        # Add scrollbars
        self.h_scrollbar = Scrollbar(self.canvas_frame, orient="horizontal")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar = Scrollbar(self.canvas_frame, orient="vertical")
        self.v_scrollbar.pack(side="right", fill="y")

        # Create the canvas
        self.image_canvas = Canvas(self.canvas_frame, bg="white", bd=1, relief="sunken",
                                   xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        self.image_canvas.pack(side="left", expand=True, fill="both")
        self.displayed_image_size = None

        # Configure scrollbars
        self.h_scrollbar.config(command=self.image_canvas.xview)
        self.v_scrollbar.config(command=self.image_canvas.yview)

        self.status_label = Label(root, text="No image loaded", fg="blue", bd=1, relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

        # Initialise the image manager and the history manager
        self.image_mgr = ImageManager()
        self.history_mgr = HistoryManager()

        self.create_menu()
        self.create_toolbar()

        # Cropping
        self.is_cropping = False
        self.crop_rect = None
        self.crop_start_x = None
        self.crop_start_y = None

    def create_menu(self):
        """Creates the menu bar with File and Edit options."""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", accelerator="Ctrl+O", command=self.image_mgr.open_image)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.root.quit)

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
        edit_menu.add_command(label="Reset Image", accelerator="Ctrl+Shift+R", command=self.reset)
        edit_menu.add_command(label="Crop Image", accelerator="Ctrl+C", command=self.start_crop)
        edit_menu.add_command(label="Resize Image", accelerator="Ctrl+R", command=self.prompt_resize)
        edit_menu.add_command(label="Grayscale", accelerator="Ctrl+G", command=self.grayscale)

    def create_toolbar(self):
        """Creates the toolbar with buttons and resize sliders."""
        toolbar = Frame(self.main_frame, bg="#f0f0f0", bd=1, relief="groove", width=220)
        toolbar.pack(side="right", fill="y", padx=5, pady=5)

        # Button style
        button_style = {"bg": "#d3d3d3", "relief": FLAT, "padx": 10, "pady": 8, "width": 14, "font": ("Helvetica", 12)}

        # Button configurations: (text_color, text, command)
        button_configs = [
            ("#0066CC", "Open", self.open),            # Blue for Open
            ("#009900", "Save", self.save_image),      # Green for Save
            ("#FF6600", "Undo", self.undo),            # Orange for Undo
            ("#CC9900", "Redo", self.redo),            # Yellow for Redo
            ("#CC0000", "Crop", self.start_crop),      # Red for Crop
            ("#666666", "Grayscale", self.grayscale),  # Gray for Grayscale
            ("#660099", "Help", self.show_help),       # Purple for Help
        ]

        # Create buttons with colored icons
        for text_color, text, command in button_configs:
            row_frame = Frame(toolbar, bg="#f0f0f0")
            row_frame.pack(pady=4, anchor="center")
            Button(row_frame, text=text, command=command, fg=text_color, **button_style).pack(side="left", padx=10)

        # Separator for visual clarity
        separator = Frame(toolbar, height=2, bg="#d3d3d3")
        separator.pack(fill="x", pady=5)

        # Resize Controls label
        Label(toolbar, text="Resize Controls", bg="#f0f0f0", font=("Helvetica", 12, "bold")).pack(pady=8)

        # Height slider
        height_frame = Frame(toolbar, bg="#f0f0f0")
        height_frame.pack(pady=5)
        Label(height_frame, text="Height", bg="#f0f0f0").pack()
        self.height_slider = Scale(height_frame, from_=1, to=1000, orient="vertical", length=150,
                                   command=self.slide, state="disabled")
        self.height_slider.pack()

        # Width slider
        width_frame = Frame(toolbar, bg="#f0f0f0")
        width_frame.pack(pady=5)
        Label(width_frame, text="Width", bg="#f0f0f0").pack()
        self.width_slider = Scale(width_frame, from_=1, to=1000, orient="horizontal", length=150,
                                  command=self.slide, state="disabled")
        self.width_slider.pack()

    def display_image(self, image: Image, update_history: bool = True):
        """
        Displays the provided image on the canvas.
        Updates the canvas size, scroll region, and status label with image details.
        Handles exceptions to prevent crashes from invalid images.

        :param image: The image to display.
        :param update_history: Whether to add the new image to the history log.
        """
        try:
            image_width, image_height = image.size
            self.photo = ImageTk.PhotoImage(image)
            self.image_canvas.delete("all")  # Clear previous content
            self.image_canvas.create_image(0, 0, image=self.photo, anchor=NW)

            # Set canvas size and scroll region to match image
            self.image_canvas.config(width=image_width, height=image_height)
            self.image_canvas.config(scrollregion=(0, 0, image_width, image_height))
            self.displayed_image_size = (image_width, image_height)

            if update_history is True:
                self.history_mgr.save_to_history(image)
                self.status_label.config(text=self.history_mgr.status)

            self.width_slider.set(image_width)
            self.height_slider.set(image_height)
            self.width_slider.config(state="normal")
            self.height_slider.config(state="normal")

            # Update sliders with original image dimensions if original_image exists
            if self.history_mgr.original_image is self.history_mgr.current_image:
                orig_width, orig_height = self.history_mgr.original_image.size
                self.width_slider.set(orig_width)
                self.height_slider.set(orig_height)
                self.status_label.config(
                    text=f"Image displayed ({image_width}x{image_height}), original size: ({orig_width}x{orig_height})")
            else:
                self.status_label.config(text=f"Image displayed ({image_width}x{image_height})")
        except Exception as e:
            self.width_slider.config(state="disabled")
            self.height_slider.config(state="disabled")
            self.status_label.config(text=f"Error: {e}")

    def prompt_resize(self):
        """
        Prompts the user for new dimensions and resizes the image.
        Only used in the menu option of resizing.
        """
        new_width = simpledialog.askinteger("Resize", "Enter new width:", parent=self.image_canvas.master,
                                            minvalue=1)
        if new_width is None:
            return
        new_height = simpledialog.askinteger("Resize", "Enter new height:", parent=self.image_canvas.master,
                                             minvalue=1)
        if new_height is None:
            return

        self.display_image(self.image_mgr.resize_image(self.history_mgr.current_image, new_width, new_height))

    def slide(self, value):
        """
        Handles slider changes to resize the image.
        De-bounces rapid slider changes using a 200ms delay.
        """

        if self.history_mgr.current_image:
            try:
                if hasattr(self, '_resize_timer'):
                    self.root.after_cancel(self._resize_timer)

                def resize():
                    new_height = int(self.height_slider.get())
                    new_width = int(self.width_slider.get())
                    return self.image_mgr.resize_image(self.history_mgr.current_image, new_width, new_height)

                self._resize_timer = self.root.after(200, self.display_image, resize())

            except Exception as e:
                self.status_label.config(text=f"Error resizing: {e}")
        else:
            self.status_label.config(text="No image loaded")

    def open(self):
        self.display_image(self.image_mgr.open_image())
        self.status_label.config(text=self.image_mgr.status)

    def save_image(self):
        self.display_image(self.image_mgr.save_file(self.history_mgr.current_image))
        self.status_label.config(text=self.image_mgr.status)

    def grayscale(self):
        self.display_image(self.image_mgr.convert_to_grayscale(self.history_mgr.current_image))
        self.status_label.config(text=self.image_mgr.status)

    def undo(self):
        self.history_mgr.undo()
        self.display_image(self.history_mgr.current_image, False)

    def redo(self):
        self.history_mgr.redo()
        self.display_image(self.history_mgr.current_image, False)

    def reset(self):
        self.history_mgr.reset()
        self.display_image(self.history_mgr.current_image, False)

    def start_crop(self):
        """
        Initiates cropping mode, allowing the user to select a crop area.
        """
        self.is_cropping = True
        self.status_label.config(text="Click and drag to select crop area")
        self.image_canvas.config(cursor="crosshair")
        self.image_canvas.bind("<Button-1>", self.crop_mouse_press)
        self.image_canvas.bind("<B1-Motion>", self.crop_mouse_drag)
        self.image_canvas.bind("<ButtonRelease-1>", self.crop_mouse_release)
        self.image_canvas.bind("<Escape>", self.cancel_crop)

    def crop_mouse_press(self, event):
        """
        Handles the start of a crop selection when the mouse is pressed.

        :param event: Tkinter event with mouse coordinates.
        :return:
        """
        if self.is_cropping:
            self.crop_start_x = event.x
            self.crop_start_y = event.y
            # Remove previous rectangle if it exists
            if self.crop_rect:
                self.image_canvas.delete(self.crop_rect)

            # Create a dashed red rectangle for crop selection
            self.crop_rect = self.image_canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_start_x,
                                                                self.crop_start_y, outline="red", dash=(4, 4))

    def crop_mouse_drag(self, event):
        """
        Updates the crop rectangle as the mouse is dragged.

        :param event: Tkinter event with mouse coordinates.
        """
        if self.is_cropping and self.crop_rect:
            img_width, img_height = self.history_mgr.current_image.size
            x = max(0, min(event.x, img_width))
            y = max(0, min(event.y, img_height))
            self.image_canvas.coords(self.crop_rect, self.crop_start_x, self.crop_start_y, x, y)

    def crop_mouse_release(self, event):
        """
        Finalizes the crop operation when the mouse is released.
        Scales crop coordinates from display to original image size and applies the crop.
        Displays a comparison window with original and cropped images.

        :param event: Tkinter event with mouse coordinates.
        """
        if self.is_cropping:
            end_x, end_y = event.x, event.y
            # Ensure coordinates are within image bounds
            img_width, img_height = self.history_mgr.current_image.size
            x1, y1 = max(0, min(self.crop_start_x, end_x)), max(0, min(self.crop_start_y, end_y))
            x2, y2 = min(img_width, max(self.crop_start_x, end_x)), min(img_height, max(self.crop_start_y, end_y))
            if x2 > x1 and y2 > y1:
                # Apply crop to original image
                crop = int(x1), int(y1), int(x2), int(y2)
                cropped_image = self.history_mgr.current_image.crop(crop)

                # Update the main canvas with the cropped image
                self.display_image(cropped_image)
                self.status_label.config(text=f"Image cropped to {crop}")
                try:
                    self.display_comparison(self.history_mgr.history[-2], cropped_image)
                except Exception as e:
                    self.status_label.config(text=f"Error displaying comparison: {e}")
            else:
                self.status_label.config(text="Invalid crop area")

            # Clean up
            self.clean_up_crop_canvas()

    def display_comparison(self, original_image: Image, cropped_image: Image):
        """
        Displays a side-by-side comparison of original and cropped images.

        :param original_image: The original image before cropping
        :param cropped_image: The cropped image
        """
        try:
            # Create a new window for comparison
            comparison_window = Toplevel(self.root)
            comparison_window.title("Original vs Cropped Image")
            comparison_window.geometry("1200x600")

            # Create frames for layout
            original_frame = Frame(comparison_window)
            original_frame.pack(side="left", padx=10, pady=10)
            cropped_frame = Frame(comparison_window)
            cropped_frame.pack(side="left", padx=10, pady=10)

            # Add labels for clarity
            Label(original_frame, text="Original Image").pack()
            Label(cropped_frame, text="Cropped Image").pack()

            # Create canvases
            original_canvas = Canvas(original_frame, bg="white", bd=1, relief="sunken")
            original_canvas.pack()
            cropped_canvas = Canvas(cropped_frame, bg="white", bd=1, relief="sunken")
            cropped_canvas.pack()

            # Scale images to fit within a max size
            max_size = 500  # Maximum size for displayed images
            orig_photo = self.image_mgr.scale_image(original_image, max_size)
            crop_photo = self.image_mgr.scale_image(cropped_image, max_size)

            # Update canvas sizes
            orig_width, orig_height = orig_photo.width(), orig_photo.height()
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
        """
        Cancels the cropping operation when Escape is pressed.

        :param event: Tkinter event (unused).
        """
        if self.is_cropping:
            self.clean_up_crop_canvas()
            self.status_label.config(text="Crop cancelled")

    def clean_up_crop_canvas(self):
        self.image_canvas.delete(self.crop_rect)
        self.crop_rect = None
        self.is_cropping = False
        self.image_canvas.config(cursor="")
        self.image_canvas.unbind("<Button-1>")
        self.image_canvas.unbind("<B1-Motion>")
        self.image_canvas.unbind("<ButtonRelease-1>")

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
            Label(shortcuts_frame, text=shortcut, font=("Helvetica", 10), anchor="w").grid(row=i, column=0, padx=5,
                                                                                           pady=2, sticky="w")
            Label(shortcuts_frame, text=action, font=("Helvetica", 10), anchor="w").grid(row=i, column=1, padx=5,
                                                                                         pady=2, sticky="w")
            Label(shortcuts_frame, text=description, font=("Helvetica", 10), anchor="w").grid(row=i, column=2, padx=5,
                                                                                              pady=2, sticky="w")

        # Close button
        Button(help_window, text="Close", command=help_window.destroy, font=("Helvetica", 10)).pack(pady=10)


root = Tk()
app = Gui(root)


# Event handlers for keyboard shortcuts
def open_image_event(event):
    """Handles Ctrl+O to open an image."""
    app.open()

def save_image_event(event):
    """Handles Ctrl+S to save the image."""
    app.save_image()

def undo_event(event):
    """Handles Ctrl+Z to undo the last operation."""
    app.undo()

def redo_event(event):
    """Handles Ctrl+Y to redo the last undone operation."""
    app.redo()

def resize_image_event(event):
    """Handles Ctrl+R to prompt for resize dimensions."""
    app.prompt_resize()

def crop_image_event(event):
    """Handles Ctrl+C to start cropping."""
    app.start_crop()

def reset_image_event(event):
    """Handles Ctrl+Shift+R to reset the image."""
    app.reset()

def grayscale_event(event):
    """Handles Ctrl+G to convert the image to grayscale."""
    app.grayscale()

def quit_event(event):
    """Handles Ctrl+Q to exit the application."""
    root.quit()


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
