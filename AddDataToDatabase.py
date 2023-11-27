import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from firebase_admin import credentials, initialize_app, db
from datetime import datetime, timedelta
import subprocess
import os

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_app = initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-65b25-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')


# function to save data to Firebase
def save_student_data():
    student_id = entry_id.get()
    student_name = entry_name.get()
    student_major = entry_branch.get()
    student_starting_year = int(entry_starting_year.get())
    student_total_attendance = 0
    student_standing = entry_standing.get()
    student_year = int(entry_year.get())
    yesterday = datetime.now() - timedelta(days=1)
    student_last_attendance_time = yesterday.strftime("%Y-%m-%d") + datetime.now().strftime(" %H:%M:%S")

    data = {
        "name": student_name,
        "major": student_major,
        "starting_year": student_starting_year,
        "total_attendance": student_total_attendance,
        "standing": student_standing,
        "year": student_year,
        "last_attendance_time": student_last_attendance_time
    }

    ref.child(student_id).set(data)
    status_label.config(text="Data saved successfully!")

    cmd = "python EncodeGenerator.py"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("Encode Generator run successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def clear_entries():
    entry_id.delete(0, "end")
    entry_name.delete(0, "end")
    entry_branch.delete(0, "end")
    entry_starting_year.delete(0, "end")
    entry_standing.delete(0, "end")
    entry_year.delete(0, "end")

# Create a Tkinter window
window = tk.Tk()
window.title("Student Data Entry")
# window.geometry("500x500+200+200")

# Initialize the camera
cap = cv2.VideoCapture(1)
live_feed_on = False

# Create a blank image to initialize the label
blank_image = np.full((216, 216, 3), (192, 192, 192), dtype=np.uint8)
blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)
blank_image = ImageTk.PhotoImage(Image.fromarray(blank_image))

# Create a label for the live video feed
video_frame = ttk.Label(window, image=blank_image)
video_frame.image = blank_image
video_frame.grid(row=0, column=0, padx=20, pady=20, rowspan=5)


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
            id_name = entry_id.get()
            if id_name:
                cropped_frame = frame[42:258, 250:466]
                photo_directory = 'Images/'
                photo_filename = os.path.join(photo_directory, f"{id_name}.png")
                cv2.imwrite(photo_filename, cropped_frame)


def open_folder():
    folder_path = 'D:\FaeRecognitionRealTime\Images'
    subprocess.Popen(f'explorer {folder_path}', shell=True)


# Create a button to capture a photo
capture_button = tk.Button(window, text="Capture Photo", command=capture_photo)
capture_button.grid(row=5, column=0, padx=20, pady=20)

open_folder_button = tk.Button(window, text="Open Folder", command=open_folder)
open_folder_button.grid(row=6, column=0, padx=20, pady=20)


def update():
    global live_feed_on
    if live_feed_on:
        ret, frame = cap.read()
        if ret:
            frame = frame[42:258, 250:466]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.resize(frame, (400, 300))  # Resize the frame to match the label size
            photo = ImageTk.PhotoImage(Image.fromarray(frame))
            video_frame.img = photo
            video_frame.configure(image=photo)
        window.after(10, update)


# Create and arrange input fields using the grid layout
label_id = tk.Label(window, text="Student ID:")
label_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

entry_id = tk.Entry(window)
entry_id.grid(row=0, column=2, padx=5, pady=5, sticky="w")

label_name = tk.Label(window, text="Name:")
label_name.grid(row=1, column=1, sticky="w", padx=5, pady=5)

entry_name = tk.Entry(window)
entry_name.grid(row=1, column=2, padx=5, pady=5, sticky="w")

label_branch = tk.Label(window, text="Branch:")
label_branch.grid(row=2, column=1, sticky="w", padx=5, pady=5)

entry_branch = tk.Entry(window)
entry_branch.grid(row=2, column=2, padx=5, pady=5, sticky="w")

label_year = tk.Label(window, text="Grade/Year:")
label_year.grid(row=3, column=1, sticky="w", padx=5, pady=5)

entry_year = tk.Entry(window)
entry_year.grid(row=3, column=2, padx=20, pady=20, sticky="w")

label_starting_year = tk.Label(window, text="Starting Year:")
label_starting_year.grid(row=4, column=1, sticky="w", padx=5, pady=5)

entry_starting_year = tk.Entry(window)
entry_starting_year.grid(row=4, column=2, padx=5, pady=5, sticky="w")

label_standing = tk.Label(window, text="Standing:")
label_standing.grid(row=5, column=1, sticky="w", padx=5, pady=5)

entry_standing = tk.Entry(window)
entry_standing.grid(row=5, column=2, padx=5, pady=5, sticky="w")

# Save Button
save_button = tk.Button(window, text="Save Data", command=save_student_data)
save_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Clear button
clear_button = tk.Button(window, text="Clear Entries", command=clear_entries)
clear_button.grid(row=6, column=2, padx=5, pady=5, sticky="w")

# Create a label to display the status
status_label = tk.Label(window, text="")
status_label.grid(row=8, column=0, padx=20, pady=20, sticky="w")

# Start the Tkinter main loop
window.mainloop()
