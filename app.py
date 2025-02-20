import os
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
from camera_control import Camera_Control
from current_project_info import Project_Info
from image_list import Image_List
from image_viewer import Image_Viewer
from menubar import RPi_Menu


def test1(event):
    print("HEY")

class RPi_Microscope_App:

    # root: Tk
    # rpi_menu: RPi_Menu
    # image_list: Image_List

    # project_info: Project_Info


    def __init__(self):

        self.project_info = Project_Info()
        self.startup()



    def start_main_app(self):

        self.root = Tk()

        self.root.title("RPi Microscope")

        self.rpi_menu = RPi_Menu(self.root, self.project_info)
        self.image_list = Image_List(self.root, self.project_info)

        Camera_Control(self.root, self.project_info)
        Image_Viewer(self.root, self.project_info)


        self.root.geometry('+%d+%d'%(10,30))  

        self.root.bind("<<NewProject>>", test1)
        self.root.event_generate("<<OpenProject>>", when="tail")

    def startup(self):
        self.init_window = Tk()
        self.init_window.title("RPi Microscope Project Selection")
        label = Label(self.init_window, text="Please open a directory")
        label.grid(row=0, column=0)
        button1 = Button(self.init_window, text="New Project", command=lambda: self.new_project())
        button1.grid(row=1, column=0)
        button2 = Button(self.init_window, text="Open Project", command=lambda: self.open_project())
        button2.grid(row=1, column=1)

    def new_project(self):
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
        self.project_info.project_dir = dir + "/" + name
        self.init_window.destroy()
        self.start_main_app()

    def open_project(self):
        dir = filedialog.askdirectory(
            initialdir="~",
            title="Please choose project to open"
        )
        while dir == "":
            dir = filedialog.askdirectory(
            initialdir="~",
            title="Please choose project to open"
        )
        self.project_info.project_dir = dir
        self.init_window.destroy()
        self.start_main_app()