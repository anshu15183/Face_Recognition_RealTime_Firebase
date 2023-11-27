import tkinter as tk
import cv2
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import numpy as np
import os
import subprocess

# Initialize the camera
cap = cv2.VideoCapture(1)
live_feed_on = False

# Create the main window
root = tk.Tk()
root.title("Camera App")

# Create a blank image to initialize the label
blank_image = np.zeros((300, 400, 3), dtype=np.uint8)
blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)
blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))

# Create a label for the live video feed
video_frame = ttk.Label(root, image=blank_image)
video_frame.image = blank_image
video_frame.grid(row=0, column=0, padx=20, pady=20)


# Create a function to capture a photo
def capture_photo():
    global live_feed_on
    if not live_feed_on:
        live_feed_on = True
        update()
    else:
        live_feed_on = False
        ret, frame = cap.read()
        if ret:
            id_name = id_entry.get()
            if id_name:
                photo_directory = 'Images/'
                photo_filename = os.path.join(photo_directory, f"{id_name}.png")
                cv2.imwrite(photo_filename, frame)


def open_folder():
    folder_path = 'D:\FaeRecognitionRealTime\Images'
    subprocess.Popen(f'explorer {folder_path}', shell=True)


# Create a button to capture a photo
capture_button = ttk.Button(root, text="Capture Photo", command=capture_photo)
capture_button.grid(row=1, column=0, padx=20, pady=20)
id_label = tk.Label(root, text="Enter ID:")
id_label.grid(row=2, column=0, padx=20, pady=20)

id_entry = tk.Entry(root)
id_entry.grid(row=3, column=0, padx=20, pady=20)

open_folder_button = tk.Button(root, text="Open Folder", command=open_folder)
open_folder_button.grid(row=4, column=0, padx=20, pady=20)


# Function to update the live video feed
def update():
    global live_feed_on
    if live_feed_on:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (400, 300))  # Resize the frame to match the label size
            photo = ImageTk.PhotoImage(Image.fromarray(frame))
            video_frame.img = photo
            video_frame.configure(image=photo)
        root.after(10, update)


# Start the Tkinter main loop
root.mainloop()
