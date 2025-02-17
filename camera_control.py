from tkinter import Label, Tk, Button
from current_project_info import Project_Info
import subprocess

class Camera_Control:

    root: Tk
    project_info: Project_Info

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        text = Label(self.root, text="Camera Controls")
        text.grid(row=3, column = 1, padx=10, pady=10)
        
        preview_button = Button(self.root,text="Live Preview", command=start_preview)
        preview_button.grid(row=4, column=1)

    
def start_preview():
    status, output = subprocess.getstatusoutput('pwd')
    print(output)

        