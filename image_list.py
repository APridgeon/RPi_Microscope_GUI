from tkinter import ACTIVE, Button, Label, Listbox, Tk, Entry, Toplevel
import os
from current_project_info import Project_Info


class Image_List:

    root: Tk
    project_info: Project_Info

    file_list: Listbox

    folder_window: Toplevel

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        text = Label(self.root, text="Project Image List")
        text.grid(row=0, column = 1, padx=10, pady=10)

        self.file_list = Listbox(self.root, height=10, selectmode="extended")
        self.file_list.grid(row=1, column=1, padx= (10, 0), pady=10)

        self.populate_image_list()

        self.file_list.bind('<Button-1>', lambda error: self.select_item())
        self.file_list.bind('<Button-2>', lambda error: self.right_click_window())

        self.root.bind("<<OpenProject>>", lambda error: self.populate_image_list())
        self.root.bind("<<Update-FileList>>", lambda error: self.populate_image_list())



    def select_item(self):
        if(self.file_list.curselection()):
            selected_item = self.file_list.get(self.file_list.curselection()[0])
            if(selected_item == self.project_info.selected_image): return     
            path = self.project_info.project_dir + "/" + selected_item  
            if(os.path.isdir(path)):
                self.select_collection(selected_item, path)
                return
            self.project_info.selected_image = selected_item

            self.root.event_generate('<<Change-Photo>>', when="tail")

    def select_collection(self, collection: str, path: str):
        try: self.folder_window.destroy()
        except: pass
        self.folder_window = Toplevel(self.root)
        self.folder_window.title("Collection files")
        self.folder_window.geometry('+%d+%d'%(100,30))  
        folder_file_list = Listbox(self.folder_window, height=6, selectmode="extended")
        folder_file_list.grid(row=0, column=0, padx=10, pady=10)
        self.populate_collection_list(folder_file_list, collection)
        folder_file_list.bind('<Double-Button-1>', lambda error: self.select_collection_item(collection, folder_file_list))
        folder_file_list.bind('<Button-2>', lambda error: self.right_click_collection_window(collection, folder_file_list))

    def select_collection_item(self, collection: str, file_list: Listbox):
        if(file_list.curselection()):
            selected_image = file_list.get(file_list.curselection()[0])
            print(file_list.get(file_list.curselection()[0]))
            if(selected_image == self.project_info.selected_image): return
            selected_image_path = collection + "/" + selected_image
            self.project_info.selected_image = selected_image_path
            self.root.event_generate('<<Change-Photo>>', when="tail")
    
    def right_click_collection_window(self, collection: str, file_list: Listbox):
        file_indeces = file_list.curselection()
        if(len(file_indeces) == 0): return

        text_entry = Toplevel(self.root)
        text_entry.title("Rename")
        rename_label = Label(text_entry, text="Rename files: ")
        rename_label.grid(row=0, column=0)
        rename_input = Entry(text_entry, width=10)
        rename_input.grid(row=0, column=1)
        cancel_button = Button(text_entry, text="Cancel", command=lambda: text_entry.destroy())
        cancel_button.grid(row=1, column=0, )
        ok_button = Button(text_entry, text="Ok", command=lambda: self.rename_collection_files(file_indeces, collection, file_list, text_entry, rename_input.get()))
        ok_button.grid(row=1, column=1)

    def rename_collection_files(self, file_indeces: list[int], collection: str, file_list: Listbox, text_entry: Toplevel, new_name: str):
        if(new_name == ""): return
        path = self.project_info.project_dir + "/" + collection
        for i, index in enumerate(file_indeces):
            print(file_list.get(i), i)
            os.rename(path + "/" + file_list.get(index), path + "/" + new_name + "_" + str(i).zfill(4) + ".jpg")
        text_entry.destroy()
        self.populate_collection_list(file_list, collection)

    def populate_collection_list(self, file_list: Listbox, collection: str):
        file_list.delete(0, file_list.size())
        collection_path = self.project_info.project_dir + "/" + collection
        files = os.listdir(collection_path)
        files.sort()
        # files.sort(key=lambda item: os.path.getmtime(self.project_info.project_dir + "/" + collection + "/" + item))
        for i, file in enumerate(files):
            file_list.insert(i, file)

    def populate_image_list(self):
        self.file_list.delete(0, self.file_list.size())
        files = os.listdir(self.project_info.project_dir)
        # files.sort(key=lambda item: os.path.getmtime(self.project_info.project_dir + "/" + item))
        files.sort()
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
        for i, index in enumerate(file_indeces):
            j = i
            ending = ".jpg"
            if(os.path.isdir(path + "/" + self.file_list.get(index))): ending = ""
            file_path = path + "/" + new_name + "_" + str(j).zfill(4) + ending
            print(file_path)
            while(os.path.isfile(file_path)):
                j = j + 1
                file_path = path + "/" + new_name + "_" + str(j).zfill(4) + ending
            os.rename(path + "/" + self.file_list.get(index), path + "/" + new_name + "_" + str(j).zfill(4) + ending)
        text_entry.destroy()
        self.populate_image_list()

