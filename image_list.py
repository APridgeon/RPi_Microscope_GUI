from tkinter import Button, Label, Listbox, Tk, Entry, Toplevel
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

        self.file_list.bind('<Button-1>', lambda error: self.select_image())
        self.file_list.bind('<Button-2>', lambda error: self.right_click_window())

        self.root.bind("<<OpenProject>>", lambda error: self.populate_image_list())


    def select_image(self):
        if(self.file_list.curselection()):
            self.project_info.selected_image = self.file_list.get(self.file_list.curselection()[0])
            self.root.event_generate('<<Change-Photo>>', when="tail")

    def populate_image_list(self):
        self.file_list.delete(0, self.file_list.size())
        files = os.listdir(self.project_info.project_dir)
        for i, file in enumerate(files):
            self.file_list.insert(i, file)

    def right_click_window(self):
        file_indeces = self.file_list.curselection()
        if(len(file_indeces) == 0): return

        text_entry = Toplevel(self.root)
        text_entry.title("Rename")
        rename_label = Label(text_entry, text="Rename files: ")
        rename_label.grid(row=0, column=0)
        rename_input = Entry(text_entry, width=10)
        rename_input.grid(row=0, column=1)
        cancel_button = Button(text_entry, text="Cancel", command=lambda: text_entry.destroy())
        cancel_button.grid(row=1, column=0, )
        ok_button = Button(text_entry, text="Ok", command=lambda: self.rename_files(file_indeces, text_entry, rename_input.get()))
        ok_button.grid(row=1, column=1)

    def rename_files(self, file_indeces: list[int], text_entry: Toplevel, new_name: str):
        if(new_name == ""): return
        path = self.project_info.project_dir
        for i in file_indeces:
            print(self.file_list.get(i), i)
            os.rename(path + "/" + self.file_list.get(i), path + "/" + new_name + "_" + str(i))
        text_entry.destroy()
        self.populate_image_list()

