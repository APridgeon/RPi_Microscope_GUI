
from tkinter import Label, PhotoImage, Tk, Toplevel
from PIL import Image, ImageTk
from current_project_info import Project_Info


class Image_Viewer:

    root: Tk
    project_info: Project_Info

    photo_window: Toplevel
    image_label: Label

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        self.create_display_window()


        self.root.bind("<<Change-Photo>>", lambda error: self.display_photo())

    def create_display_window(self):
        self.photo_window = Toplevel(self.root)
        self.project_info.photo_window = self.photo_window
        self.image_label = Label(self.photo_window)


    def display_photo(self):
        print("change fired!", self.project_info.selected_image)

        img = Image.open(self.project_info.project_dir + "/" + self.project_info.selected_image).convert("RGB")
        my_img = ImageTk.PhotoImage(img)

        try:
            self.photo_window.title(self.project_info.selected_image)
        except:
            self.photo_window = Toplevel(self.root)
            self.project_info.photo_window = self.photo_window            
            self.photo_window.title(self.project_info.selected_image)

        self.image_label.destroy()
        self.image_label = Label(self.photo_window, image=my_img)
        self.image_label.image = my_img
        self.image_label.pack()
        self.photo_window.focus_force()

