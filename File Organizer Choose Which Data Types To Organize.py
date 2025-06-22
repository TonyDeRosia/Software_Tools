#!/usr/bin/env python
# coding: utf-8

# In[14]:


import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import OptionMenu
import os

root = tk.Tk()
root.title("Organize Folder")

folder_path = tk.StringVar()

def choose_folder():
    selected_folder = askdirectory()
    folder_path.set(selected_folder)

def organize_folder():
    selected_folder = folder_path.get()
    selected_data_type = data_type.get()

    def unique_destination(path):
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = path
        while os.path.exists(new_path):
            new_path = f"{base}_{counter}{ext}"
            counter += 1
        return new_path

    if not selected_folder:
        result_label.config(text="Please select a folder first.")
        return

    if not os.path.exists(selected_folder):
        result_label.config(text="The selected folder does not exist.")
        return

    if not os.path.isdir(selected_folder):
        result_label.config(text="The selected path is not a folder.")
        return

    try:
        files = os.listdir(selected_folder)
    except PermissionError:
        result_label.config(text="Permission denied for the selected folder.")
        return

    subfolders = {}

    for file in files:
        if file.startswith("."):
            continue

        file_extension = os.path.splitext(file)[1]

        if selected_data_type not in ("All", "*", "", None) and selected_data_type != file_extension:
            continue

        if file_extension not in subfolders:
            subfolders[file_extension] = []

        subfolders[file_extension].append(file)

    for file_extension, file_list in subfolders.items():
        subfolder_path = os.path.join(selected_folder, file_extension[1:] + "_files")
        try:
            os.makedirs(subfolder_path, exist_ok=True)
        except PermissionError:
            result_label.config(text="Permission denied to create subfolder in the selected folder.")
            return

        for file in file_list:
            file_path = os.path.join(selected_folder, file)
            destination = os.path.join(subfolder_path, file)
            destination = unique_destination(destination)
            try:
                os.rename(file_path, destination)
            except Exception:
                result_label.config(text="An error occurred while moving the files.")
                return

    result_label.config(text="Folder organized successfully.")

label1 = tk.Label(root, text="Folder Path:")
label1.pack(pady=20)

entry1 = tk.Entry(root, textvariable=folder_path)
entry1.pack()

choose_button = tk.Button(root, text="Choose Folder", command=choose_folder)
choose_button.pack()

label2 = tk.Label(root, text="Data Type:")
label2.pack(pady=20)

data_type = tk.StringVar()
data_type.set("All")

options = ["All", "*", ".txt", ".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".mp3", ".mp4", ".avi", ".mkv", ".zip", ".rar", ".7z", ".bmp"]

dropdown = OptionMenu(root, data_type, *options)
dropdown.pack()

organize_button = tk.Button(root, text="Organize Folder", command=organize_folder)
organize_button.pack(pady=20)

result_label = tk.Label(root, text="")
result_label.pack(pady=20)

root.geometry("400x400")
root.mainloop()


# In[ ]:




