import tkinter as tk
from tkinter import messagebox, ttk
from pipVid import VideoProcessingPipeline
import os

# Function to be triggered when the button is clicked
def on_button_click():
    video_url = url_entry.get()
    resolution = resolution_combobox.get()
    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL.")
        return
    try:
        pipeline = VideoProcessingPipeline(video_url, resolution)
        pipeline.run_pipeline()
        messagebox.showinfo("Success", "Video processing started successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        
def check_and_create_db_file():
    if not os.path.exists('db.txt'):
        with open('db.txt', 'w') as f:
            f.write('1\n1')
            
            
check_and_create_db_file()
# Create the main window
root = tk.Tk()
root.title("QVMG Quraan Video Mass Generator")

# Create a frame for the entry widgets
entry_frame = tk.Frame(root, padx=10, pady=10)
entry_frame.pack(padx=10, pady=10)

# Label and entry for the URL input
label1 = tk.Label(entry_frame, text="URL:")
label1.grid(row=0, column=0, sticky=tk.W, pady=5)
url_entry = tk.Entry(entry_frame, width=30)
url_entry.grid(row=0, column=1, pady=5)

# Label and combobox for the resolution selection
label2 = tk.Label(entry_frame, text="Resolution:")
label2.grid(row=1, column=0, sticky=tk.W, pady=5)
resolutions = ["144p", "360p", "480p", "720p", "1080p"]
resolution_combobox = ttk.Combobox(entry_frame, values=resolutions, width=27, state='readonly')
resolution_combobox.grid(row=1, column=1, pady=5)
resolution_combobox.current(3)  # Set default selection to 720p

# Create a frame for the button
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.pack(padx=10, pady=10)

# Create the button
button = tk.Button(button_frame, text="Submit", command=on_button_click, width=15)
button.pack()

# Start the Tkinter event loop
root.mainloop()
