#!/usr/bin/env python
# coding: utf-8

# In[5]:


import tkinter as tk
from tkinter import filedialog
import os

def organize_folder():
    selected_folder = folder_path.get()
    if not selected_folder:
        result_label.config(text="Please select a folder first.")
        return

    # Check if the selected folder exists
    if not os.path.exists(selected_folder):
        result_label.config(text="The selected folder does not exist.")
        return

    # Check if the selected folder is a directory
    if not os.path.isdir(selected_folder):
        result_label.config(text="The selected path is not a folder.")
        return

    # Get a list of all files in the selected folder
    try:
        files = os.listdir(selected_folder)
    except PermissionError:
        result_label.config(text="Permission denied for the selected folder.")
        return

    # Dictionary to store subfolders for each file type
    subfolders = {}

    # Iterate through each file in the selected folder
    for file in files:
        # Skip hidden files
        if file.startswith("."):
            continue

        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        # If the file extension is not in the dictionary, add it
        if file_extension not in subfolders:
            subfolders[file_extension] = []

        # Add the file to the corresponding subfolder
        subfolders[file_extension].append(file)

    # Create subfolders for each file type
    for file_extension, file_list in subfolders.items():
        subfolder_path = os.path.join(selected_folder, file_extension[1:] + "_files")
        try:
            os.makedirs(subfolder_path, exist_ok=True)
        except PermissionError:
            result_label.config(text="Permission denied to create subfolder in the selected folder.")
            return

        # Move the files to the corresponding subfolder
        for file in file_list:
            file_path = os.path.join(selected_folder, file)
            destination = os.path.join(subfolder_path, file)
            try:
                os.rename(file_path, destination)
            except PermissionError:
                result_label.config(text="Permission denied to move files in the selected folder.")
                return

    result_label.config(text="Folder organized successfully!", font=("TkDefaultFont", 14, "bold"))

# GUI setup
root = tk.Tk()
root.title("Folder Organizer")
root.geometry("400x200")
root.resizable(False, False)

folder_path = tk.StringVar()

browse_frame = tk.Frame(root)
browse_frame.pack(pady=20)

browse_label = tk.Label(browse_frame, text="Select a folder:", font=("TkDefaultFont", 12, "bold"))
browse_label.pack(side="left")

browse_button= tk.Button(browse_frame, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory()))
browse_button.pack(side="left")

result_frame = tk.Frame(root)
result_frame.pack(pady=20)

result_label = tk.Label(result_frame, text="", font=("TkDefaultFont", 12))
result_label.pack()

organize_button = tk.Button(root, text="Organize Folder", command=organize_folder)
organize_button.pack(pady=20)

root.mainloop()


# In[ ]:




