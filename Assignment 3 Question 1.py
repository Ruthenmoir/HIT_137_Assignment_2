from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


def menu_tester():
    print("Menu Test works")

#Image processing Section

class image_manager:
    def __init__(self, image_label, status_label):
        self.original_image = None
        self.image_label = image_label
        self.status_label = status_label        

    def open_image(self):
        filepath = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"),("All files", "*.*")))
        if filepath:
            self.display_image(filepath)

    def display_image(self, filepath):
        try:
            image = Image.open(filepath)
            image = image.resize((400, 400), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo  
            self.status_label.config(text=f"Image loaded: {filepath}")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")



#GUI Manager Section

class gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Group 2, Assignment 3")



        self.banner = Label(root, text="Group 2's Image Manipulator", bg="grey")
        self.banner.pack(side=TOP, fill=X)

        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        self.status_label = Label(root, text="No image loaded", fg="blue")
        self.status_label.pack(side=BOTTOM, fill=X)       
        self.image_mgr = image_manager(self.image_label, self.status_label)
     
        self.create_menu()

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
        edit_menu.add_command(label="Resize Image", command=menu_tester)   










root = Tk()

app = gui(root)




root.mainloop()





#Mouse Interaction Section


#History Manager Section for Undo and Redo
