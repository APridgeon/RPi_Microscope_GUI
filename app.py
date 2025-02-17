from tkinter import *
from camera_control import Camera_Control
from current_project_info import Project_Info
from image_list import Image_List
from menubar import RPi_Menu


def test1(event):
    print("HEY")

class RPi_Microscope_App:

    root: Tk
    rpi_menu: RPi_Menu
    image_list: Image_List

    project_info: Project_Info


    def __init__(self):
        self.root = Tk()
        self.project_info = Project_Info()

        self.root.title("RPi Microscope")
        self.root.geometry("200x400")

        self.rpi_menu = RPi_Menu(self.root, self.project_info)
        self.image_list = Image_List(self.root, self.project_info)
        Camera_Control(self.root, self.project_info)

        self.root.bind("<<NewProject>>", test1)




