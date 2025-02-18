from tkinter import Entry, Label, Tk, Button
from current_project_info import Project_Info
import subprocess
import os

class Camera_Control:

    root: Tk
    project_info: Project_Info

    preview_button: Button
    single_image_button: Button

    duration_entry: Entry
    interval_entry: Entry

    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        text = Label(self.root, text="Camera Controls")
        text.grid(row=3, column = 1, padx=10, pady=10)
        
        self.preview_button = Button(self.root,text="Live Preview", command=start_preview)
        self.preview_button.grid(row=4, column=1)

        self.single_image_button = Button(self.root, text="Capture Image", command=lambda:capture_image(self))
        self.single_image_button.grid(row=5, column=1)

        timelapse_duration = Label(self.root, text="Timelapse duration (ms): ")
        timelapse_duration.grid(row=6, column=1)
        self.duration_entry = Entry(self.root, width=6)
        self.duration_entry.insert(0, "10000")
        self.duration_entry.grid(row=6, column=2)

        timelapse_interval = Label(self.root, text="Timelapse interval (ms): ")
        timelapse_interval.grid(row=7, column=1)
        self.interval_entry = Entry(self.root, width=6)
        self.interval_entry.insert(0, "500")
        self.interval_entry.grid(row=7, column=2)

        timelapse_button = Button(self.root, text="Capture timelapse", command=lambda:capture_timelapse(self))
        timelapse_button.grid(row=8, column=1)


    
def start_preview():
    status, output = subprocess.getstatusoutput('libcamera-hello --timeout 0 --info-text Preview')

def capture_image(self: Camera_Control):
    n_of_files = len(os.listdir(self.project_info.project_dir))
    file_name = "untitled" + str(n_of_files + 1) + '.jpg'
    subprocess.getoutput('libcamera-jpeg --timeout 10 --width 800 --height 600 --output ' + self.project_info.project_dir + '/' + file_name)

def capture_timelapse(self: Camera_Control):
    n_of_files = len(os.listdir(self.project_info.project_dir))
    folder = 'Collection' + str(n_of_files+1)
    timelapse_dir = self.project_info.project_dir + '/' + folder
    os.mkdir(timelapse_dir)
    file_name = 'untitled%04d.jpg'
    subprocess.getoutput('libcamera-still --timeout ' + self.duration_entry.get() + ' --timelapse '+ self.interval_entry.get() + ' --width 800 --height 600 --output ' + timelapse_dir + '/' + file_name)


    