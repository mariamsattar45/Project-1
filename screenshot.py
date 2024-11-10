#REQUIREMENTS

#First create virtual environment
#python -m venv venv

#Activate the environment
#venv/Scripts/activate

#Install Tkinter
#pip install tk

#to install screeenshot library
#pip install pyscreenshot

#To check how many libraries are currently running use command
#pip freeze

#install dependency 5132 when copy to clipboard which works only on windows
#pip install pywin32

#pip install pillow pywin32


import tkinter as tk
from PIL import ImageGrab, Image, ImageTk
import time
from io import BytesIO
from datetime import datetime
import win32clipboard
import win32con 

# Root window
root = tk.Tk()
root.title("Screenshot Clipper")

#background color 
root.config(bg="lightblue")

# Canvas 
canvas_width, canvas_height = 500, 250  # Canvas size
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="lightblue")
canvas.grid(row=0, column=0, padx=20, pady=20)

# image 
image_path = "screenimage.png"  
img = Image.open(image_path)  

# aspect ratio
img_width, img_height = img.size
aspect_ratio = img_width / img_height


if img_width > img_height:
    # Landscape image: scale by width
    new_width = canvas_width
    new_height = int(new_width / aspect_ratio)
    if new_height > canvas_height:
        new_height = canvas_height
        new_width = int(new_height * aspect_ratio)
else:
    # Portrait or square image: scale by height
    new_height = canvas_height
    new_width = int(new_height * aspect_ratio)
    if new_width > canvas_width:
        new_width = canvas_width
        new_height = int(new_width / aspect_ratio)

# Resize the image
img = img.resize((new_width, new_height))

# Convert to PhotoImage for Tkinter
img_tk = ImageTk.PhotoImage(img)


canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=img_tk)

# Checkbuttons for options
copy_clip = tk.IntVar()
show_clip = tk.IntVar()

copy_clip_check = tk.Checkbutton(root, text="Copy screenshot to clipboard", variable=copy_clip, bg="lightblue")
show_clip_check = tk.Checkbutton(root, text="Show screenshot", variable=show_clip, bg="lightblue")

copy_clip_check.grid(row=1, column=0, pady=5) 
show_clip_check.grid(row=2, column=0, pady=5)

label = tk.Label(root, text="", bg="lightblue")
label.grid(row=3, column=0, pady=10)

# dimensions of the screenshot
user_left = tk.Entry(root, text="")
user_left.grid(row=4, column=0, padx=5, pady=5)

user_top = tk.Entry(root, text="")
user_top.grid(row=5, column=0, padx=5, pady=5)

user_right = tk.Entry(root, text="")
user_right.grid(row=6, column=0, padx=5, pady=5)

user_bottom = tk.Entry(root, text="")
user_bottom.grid(row=7, column=0, padx=5, pady=5)

# Function to send image to clipboard
def copy_to_clipboard(filepath):
    """Copy the screenshot image to clipboard."""
    try:
        image = Image.open(filepath)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")  
        data = output.getvalue()[14:] 
        output.close()
        send_to_clipboard(win32con.CF_DIB, data)
        print(f"Image copied to clipboard: {filepath}")
    except Exception as e:
        print(f"Error copying to clipboard: {e}")

def send_to_clipboard(clip_type, data):
    """Send image data to clipboard."""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

# Function to take a screenshot
def clip_screen(dimensions):
    """Take a screenshot based on given dimensions or full screen."""
    image_name = str(datetime.now()).replace(" ", "_").replace(":", "") + ".png"
    
    root.withdraw()  # Hide the window while capturing
    time.sleep(0.4)  
    
    try:
        if dimensions:  # If dimensions are provided, capture a specific region
            image = ImageGrab.grab(bbox=tuple(map(int, dimensions)))
        else:  # If no dimensions, capture the entire screen
            image = ImageGrab.grab()
        
        image.save(image_name)  # Save the screenshot
        print(f"Screenshot saved as {image_name}")
        
        # optional actions
        if copy_clip.get():  # If "Copy screenshot to clipboard" is checked
            copy_to_clipboard(image_name)
        if show_clip.get():  # If "Show screenshot" is checked
            image.show()
        
        return f"Clipping done, Image name is {image_name}"
    
    except Exception as e:
        print(e)  # Print any errors 
        return f"Error: {e}"
    
    root.deiconify()  # Show the Tkinter window again after capturing the screenshot

# Function to capture full-screen
def get_fullscreen():
    """Capture the full screen."""
    label.configure(text=clip_screen(None))

# Function to capture a screen region based on user input
def get_dimension():
    """Capture the screen region based on user inputs."""
    left = user_left.get().strip()
    top = user_top.get().strip()
    right = user_right.get().strip()
    bottom = user_bottom.get().strip()

    try:
        dimensions = (int(left), int(top), int(right), int(bottom))
        label.configure(text=clip_screen(dimensions))
    except ValueError:
        label.configure(text="Invalid input. Please enter valid integers for dimensions.")

# Button to capture a screenshot with specific dimensions
dim_clip_button = tk.Button(text="Clip with dimensions", command=get_dimension, bg="#3776ab", fg="white", padx=10)
dim_clip_button.grid(row=8, column=0, pady=10)  # Button for dimensions

# Button to capture a full-screen screenshot
fs_clip_button = tk.Button(text="Clip full screen", command=get_fullscreen, bg="#3776ab", fg="white", padx=10)
fs_clip_button.grid(row=9, column=0, pady=10) 

root.mainloop()
