from tkinter import *
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk


def menu_tester():
    print("Menu Test works")

#Image processing Section

class image_manager:
    def __init__(self, image_canvas, status_label):
        self.original_image = None
        self.image_canvas = image_canvas
        self.status_label = status_label
        self.photo = None        

    def open_image(self):
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),("All files", "*.*")))
        if filepath:
            self.status_label.config(text=f"Opening image: {filepath}")
            self.original_image = Image.open(filepath)
            self.display_image(self.original_image)

    def display_image(self, image):
        try:
            image_width, image_height = image.size 
            max_size = 1500
            if image_width > max_size or image_height > max_size:
                scale = min(max_size / image_width, max_size / image_height)
                image_width = int(image_width * scale)
                image_height = int(image_height * scale)
                image = image.resize((image_width, image_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            print("PhotoImage created successfully")
            self.image_canvas.delete("all")
            self.image_canvas.create_image(0,0,image=self.photo, anchor=NW)
            print("Image drawn on canvas")
            self.image_canvas.config(width=image_width, height=image_height)          
            self.status_label.config(text=f"Image displayed({image_width}x{image_height}")
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

#GUI Manager Section

class gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 2, Assignment 3")



        self.banner = Label(root, text="Group 2's Image Manipulator", bg="grey")
        self.banner.pack(side=TOP, fill=X)

        self.image_canvas = Canvas(root, width=400, height=400, bg="white")
        self.image_canvas.pack(pady=10)
        print("Canvas initialised")

        self.status_label = Label(root, text="No image loaded", fg="blue", bd=1, relief=SUNKEN, anchor=W)
        self.status_label.pack(side=BOTTOM, fill=X)       
        self.image_mgr = image_manager(self.image_canvas, self.status_label)
     
        self.create_menu()
        self.create_toolbar()



    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)


        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.image_mgr.open_image)
        file_menu.add_command(label="Save", command=menu_tester)
        file_menu.add_command(label="Save As", command=menu_tester)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = Menu(menubar, tearoff=0)   
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=menu_tester)  
        edit_menu.add_command(label="Reset Image", command=menu_tester)  
        edit_menu.add_command(label="Crop Image", command=menu_tester)   
        edit_menu.add_command(label="Resize Image", command=self.image_mgr.prompt_resize)   

    def create_toolbar(self):
        toolbar = Frame(self.root)
        toolbar.pack(side=BOTTOM, fill=X)

        button_frame = Frame(toolbar)
        button_frame.pack(anchor=CENTER)

        opentbutton = Button(button_frame, text="Open", command=self.image_mgr.open_image)
        opentbutton.pack(side=LEFT, padx=2, pady=2)
        savebutton= Button(button_frame, text="Save", command=menu_tester)
        savebutton.pack(side=LEFT, padx=2, pady=2)
        undobutton= Button(button_frame, text="Undo", command=menu_tester)
        undobutton.pack(side=LEFT, padx=2, pady=2)
        redobutton= Button(button_frame, text="Redo", command=menu_tester)
        redobutton.pack(side=LEFT, padx=2, pady=2)
        cropbutton= Button(button_frame, text="Crop", command=menu_tester)
        cropbutton.pack(side=LEFT, padx=2, pady=2)
        resizebutton= Button(button_frame, text="Resize", command=self.image_mgr.prompt_resize)
        resizebutton.pack(side=LEFT, padx=2, pady=2)




root = Tk()

app = gui(root)




root.mainloop()





#Mouse Interaction Section


#History Manager Section for Undo and Redo
