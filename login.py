import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog  # For password dialog
from PIL import Image, ImageTk  # For displaying the image
import cvzone

# Define a valid username and password (you can replace these with your own)
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

def run_main():
    subprocess.Popen(["python", "main.py"])

def authenticate_and_run_add_to_database():
    # Prompt for a username and password
    username = simpledialog.askstring("Authentication", "Enter Username:")
    password = simpledialog.askstring("Authentication", "Enter Password:", show="*")

    # Check if the entered username and password are valid
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        subprocess.Popen(["python", "AddDataToDatabase.py"])
    else:
        status_label.config(text="Authentication failed!")

root = tk.Tk()
root.title("Facial Recognition Attendance System")

# Create a custom font for the heading
custom_font = ('Helvetica', 24, 'bold')

# Create a frame for the image with a border
image_frame = ttk.Frame(root, relief="groove", borderwidth=2)
image_frame.pack()

# Load and display an image inside the frame
image = Image.open("logo.png")  # Replace "your_image.png" with your image file path
image = image.resize((200, 200), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(image_frame, image=photo)
image_label.image = photo
image_label.pack()

# Create a label for the heading
heading_label = tk.Label(root, text="Facial Recognition Attendance System", font=custom_font)
heading_label.pack()

# Create buttons to run main.py and add_to_database.py
main_button = ttk.Button(root, text="Run Main", command=run_main)
main_button.pack()

add_to_db_button = ttk.Button(root, text="Run Add to Database", command=authenticate_and_run_add_to_database)
add_to_db_button.pack()

# Create a status label
status_label = tk.Label(root, text="Status: Ready")
status_label.pack()

root.mainloop()
