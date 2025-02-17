from tkinter import Menu, Tk, filedialog, simpledialog, messagebox
import os
import subprocess
from current_project_info import Project_Info


def donothing():
   error, out = subprocess.getstatusoutput("pwd")
   print("hello", out)




class RPi_Menu:

    root: Tk
    file_menu: Menu
    project_info: Project_Info

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.create_menubar(root)
        self.project_info = project_info

    def create_menubar(self, root: Tk):
        menubar = Menu(root)

        #delete python menubar item
        python_menu = Menu(menubar, name='apple')
        menubar.add_cascade(menu=python_menu)
        root['menu'] = menubar
        python_menu.destroy()

        RPi_menu = Menu(menubar, tearoff=0)
        RPi_menu.add_command(label="about", command=donothing)
        menubar.add_cascade(label="RPi Microscope", menu=RPi_menu)

        self.file_menu = Menu(menubar, tearoff=0)
        self.file_menu.add_command(label="New Project", command=lambda: self.create_new_project())
        self.file_menu.add_command(label="Open Project", command=lambda: self.open_project())
        self.file_menu.add_command(label="Save Project", command=donothing)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=self.file_menu)

        root.config(menu=menubar)



    def create_new_project(self):
        name = simpledialog.askstring("Project Name", "Please enter a project name and then choose a location to save")
        dir = filedialog.askdirectory(
            initialdir="~",
            title="Please choose location to save"
        )
        if(os.path.exists(dir + "/" + name)):
            messagebox.showwarning(message="File already exists!")
        else:
            self.project_info.project_dir = dir + "/" + name
            os.mkdir(dir + "/" + name)
            self.root.event_generate("<<NewProject>>", when="tail")

    def open_project(self):
        dir = filedialog.askdirectory(
            initialdir="~",
            title="Please choose project to open"
        )
        self.project_info.project_dir = dir
        self.root.event_generate("<<OpenProject>>", when="tail")

