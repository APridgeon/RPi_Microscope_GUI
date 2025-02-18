
from tkinter import Label, PhotoImage, Tk, Toplevel
from PIL import Image, ImageTk
from current_project_info import Project_Info


class Image_Viewer:

    root: Tk
    project_info: Project_Info

    photo_window: Toplevel

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info


        self.root.bind("<<Change-Photo>>", lambda error: self.display_photo())

    def display_photo(self):
        try: self.photo_window.destroy()
        except: pass
        self.photo_window = Toplevel(self.root)
        self.photo_window.title(self.project_info.selected_image)
        self.project_info.photo_window = self.photo_window

        img = Image.open(self.project_info.project_dir + "/" + self.project_info.selected_image).convert("RGB")
        my_img = ImageTk.PhotoImage(img)
        lab = Label(self.photo_window, image=my_img)
        lab.image = my_img
        lab.pack()