from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk


def menu_tester():
    print("Menu Test works")

#Image processing Section

class image_manager:
    def __init__(self, image_canvas, status_label, gui):
        self.original_image = None
        self.image_canvas = image_canvas
        self.status_label = status_label
        self.photo = None
        self.gui = gui

    def open_image(self):
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),("All files", "*.*")))
        if filepath:
            self.status_label.config(text=f"Opening image: {filepath}")
            self.original_image = Image.open(filepath)
            self.display_image(self.original_image)

    def display_image(self, image):
        try:
            image_width, image_height = image.size 
            max_size = 1000
            if image_width > max_size or image_height > max_size:
                scale = min(max_size / image_width, max_size / image_height)
                image_width = int(image_width * scale)
                image_height = int(image_height * scale)
                image = image.resize((image_width, image_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.status_label.config(text="PhotoImage created successfully")
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0,0,image=self.photo, anchor=NW)
            self.status_label.config(text="Image drawn on canvas")
            self.image_canvas.config(width=image_width, height=image_height)          
            self.gui.width_slider.set(image_width)
            self.gui.height_slider.set(image_height)
            self.status_label.config(text=f"Image displayed({image_width}x{image_height})")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def resize_image(self, new_width, new_height):
        try:
            if self.original_image:
                self.original_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)
                self.display_image(self.original_image)
                self.status_label.config(text=f"Image resized to: {new_width} x {new_height}")
            else:
                self.status_label.config(text="No image loaded")
        except Exception as e:
            self.status_label.config(text=f"Error resizing image: {e}")
            
    def prompt_resize(self):
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
       
 


#History Manager Section for Undo and Redo



#GUI Manager Section

class gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 2, Assignment 3")

        self.banner = Label(root, text="Group 2 Image Manipulator", font=("Helvetica", 16, "bold"), bg="#f0f0f0", pady=10)
        self.banner.pack(side=TOP, fill=X)

        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        self.image_canvas = Canvas(self.main_frame, width=400, height=400, bg="white", bd=1, relief=SUNKEN)
        self.image_canvas.pack(side=RIGHT, pady=10, expand=True, fill=BOTH)
        print("Canvas initialised")

        self.status_label = Label(root, text="No image loaded", fg="blue", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=BOTTOM, fill=X)       
        self.image_mgr = image_manager(self.image_canvas, self.status_label, self)

   


        self.create_menu()
        self.create_toolbar()



    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)


        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.image_mgr.open_image)
        file_menu.add_command(label="Save", command=self.image_mgr.save_file)
        file_menu.add_command(label="Save As", command=self.image_mgr.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=menu_tester)  
        edit_menu.add_command(label="Reset Image", command=menu_tester)  
        edit_menu.add_command(label="Crop Image", command=menu_tester)   
        edit_menu.add_command(label="Resize Image", command=self.image_mgr.prompt_resize)   

    def create_toolbar(self):
        toolbar = Frame(self.main_frame, bg="#f0f0f0", bd=1, relief=GROOVE)
        toolbar.pack(side=LEFT, fill=Y, padx=5, pady=5)
        button_style = {"bg": "#d3d3d3", "fg": "#333333", "relief": FLAT, "padx": 5, "pady": 5, "width": 10, "font": ("Helvetica", 10)}
        opentbutton = Button(toolbar, text="Open", command=self.image_mgr.open_image, **button_style)
        opentbutton.pack(pady=2)
        savebutton= Button(toolbar, text="Save", command= self.image_mgr.save_file, **button_style)
        savebutton.pack(pady=2)
        undobutton= Button(toolbar, text="Undo", command=menu_tester, **button_style)
        undobutton.pack(pady=2)
        redobutton= Button(toolbar, text="Redo", command=menu_tester, **button_style)
        redobutton.pack(pady=2)
        cropbutton= Button(toolbar, text="Crop", command=menu_tester, **button_style)
        cropbutton.pack(pady=2)
        resizebutton= Button(toolbar, text="Resize", command=self.image_mgr.prompt_resize, **button_style) 
        resizebutton.pack(pady=2)

        slider_frame = Frame(self.main_frame, bg="#f0f0f0", bd=1, relief=GROOVE)
        slider_frame.pack(side=LEFT, fill=X, padx=5, pady=(10, 5))
   
        height_frame = Frame(slider_frame, bg="#f0f0f0")
        height_frame.pack(side=TOP, pady=5)
        Label(height_frame, text="Height", bg="#f0f0f0").pack()
        self.height_slider = Scale(toolbar, from_=1, to=1000, orient=VERTICAL, length=150, command=self.height_slide)
        self.height_slider.pack()

        width_frame = Frame(slider_frame, bg="#f0f0f0")
        width_frame.pack(side=TOP, pady=5)
        Label(width_frame, text="Width", bg="#f0f0f0").pack()
        self.width_slider = Scale(toolbar, from_=1, to=1000, orient=HORIZONTAL, length=150, command=self.width_slide)
        self.width_slider.pack()

    def width_slide(self, value):
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






root = Tk()

app = gui(root)




root.mainloop()





#Mouse Interaction Section


