import tkinter as tk
import cv2
from tkinter import PhotoImage
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create the main window
root = tk.Tk()
root.title("Camera App")

# Create a label for the live video feed
video_frame = ttk.Label(root)
video_frame.pack(padx=10, pady=10)

# Create a function to capture a photo
def capture_photo():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("captured_photo.png", frame)

# Create a button to capture a photo
capture_button = ttk.Button(root, text="Capture Photo", command=capture_photo)
capture_button.pack(pady=10)

# Function to update the live video feed
def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (400, 300))  # Resize the frame to match the label size
        photo = ImageTk.PhotoImage(Image.fromarray(frame))
        video_frame.img = photo
        video_frame.configure(image=photo)
    root.after(10, update)

# Start updating the live feed
update()

# Start the Tkinter main loop
root.mainloop()
