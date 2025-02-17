from tkinter import Label, Listbox, Tk
import os
from current_project_info import Project_Info


class Image_List:

    root: Tk
    project_info: Project_Info

    file_list: Listbox

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        text = Label(self.root, text="Project Image List")
        text.grid(row=0, column = 1, padx=10, pady=10)

        self.file_list = Listbox(self.root, height=10, selectmode="extended")
        self.file_list.grid(row=1, column=1, padx= (10, 0), pady=10)

        self.root.bind("<<OpenProject>>", lambda error: self.populate_image_list())

    def populate_image_list(self):
        files = os.listdir(self.project_info.project_dir)
        for i, file in enumerate(files):
            self.file_list.insert(i, file)

