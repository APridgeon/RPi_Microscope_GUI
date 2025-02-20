from tkinter import HORIZONTAL, BooleanVar, Checkbutton, Entry, Label, Scale, Tk, Button
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

    exposure_checkbox: Checkbutton
    exposure_boolean: BooleanVar
    exposure_slider: Scale

    width_input: Entry
    height_input: Entry


    def __init__(self, root: Tk, project_info: Project_Info):
        self.root = root
        self.project_info = project_info

        text = Label(self.root, text="Camera Controls")
        text.grid(row=3, column = 1, padx=10, pady=10)
        
        self.preview_button = Button(self.root,text="Live Preview", command=self.start_preview)
        self.preview_button.grid(row=4, column=1)

        self.single_image_button = Button(self.root, text="Capture Image", command=lambda:capture_image(self))
        self.single_image_button.grid(row=5, column=1)

        self.setup_cam_options()
        self.setup_timelapse()

    def setup_cam_options(self):
        self.exposure_boolean = BooleanVar()
        self.exposure_checkbox = Checkbutton(self.root, text="Manual exposure", variable=self.exposure_boolean)
        self.exposure_checkbox.grid(row=20, column=1, pady=50)
        self.exposure_slider = Scale(self.root, from_=0, to=32987, tickinterval=0, length=100, orient=HORIZONTAL)
        self.exposure_slider.grid(row=20, column = 2, padx=10)

        width_label = Label(self.root, text="Width")
        width_label.grid(row=21, column=1)
        height_label = Label(self.root, text="Height")
        height_label.grid(row=21, column=2)
        self.width_input = Entry(self.root, width = 4)
        self.width_input.insert(0, "800")
        self.width_input.grid(row=22, column =1)
        self.height_input = Entry(self.root, width= 4)
        self.height_input.insert(0, "600")
        self.height_input.grid(row=22, column =2)

    def setup_timelapse(self):
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
    

    def retrieve_camera_control_values(self):
        exposure = ""
        if(self.exposure_boolean.get()):
            exposure_value = self.exposure_slider.get()
            exposure = " --shutter " + str(exposure_value)

        width = " --width " + str(self.width_input.get())
        height = " --height " + str(self.height_input.get())
        
        return [exposure, width, height]

    def start_preview(self):
        exposure, width, height = self.retrieve_camera_control_values()
        status, output = subprocess.getstatusoutput('libcamera-hello --timeout 0 --info-text Preview' + width + height)

def capture_image(self: Camera_Control):
    exposure, width, height = self.retrieve_camera_control_values()
    n_of_files = len(os.listdir(self.project_info.project_dir))
    file_name = "untitled" + "_" + str(n_of_files + 1).zfill(4) + '.jpg'
    output = subprocess.getoutput('libcamera-jpeg --timeout 10 ' + width + height + ' --output ' + self.project_info.project_dir + '/' + file_name + exposure)
    print(output)
    self.root.event_generate("<<Update-FileList>>")

def capture_timelapse(self: Camera_Control):
    exposure, width, height = self.retrieve_camera_control_values()
    n_of_files = len(os.listdir(self.project_info.project_dir))
    folder = 'Collection' + "_" + str(n_of_files+1).zfill(4)
    timelapse_dir = self.project_info.project_dir + '/' + folder
    os.mkdir(timelapse_dir)
    file_name = 'untitled%04d.jpg'
    output = subprocess.getoutput('libcamera-still --timeout ' + self.duration_entry.get() + ' --timelapse '+ self.interval_entry.get() + width + height + ' --output ' + timelapse_dir + '/' + file_name + exposure)
    print(output)
    self.root.event_generate("<<Update-FileList>>")


    