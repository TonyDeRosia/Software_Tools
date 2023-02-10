#!/usr/bin/env python
# coding: utf-8

# In[4]:


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
from pytube import YouTube

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Downloader")
        self.geometry("400x200")

        self.url_label = tk.Label(self, text="Enter the YouTube video URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        self.path_label = tk.Label(self, text="Enter the path to save the video:")
        self.path_label.pack()

        self.path_entry = tk.Entry(self)
        self.path_entry.pack()

        self.browse_button = tk.Button(self, text="Browse", command=self.browse)
        self.browse_button.pack()

        self.download_button = tk.Button(self, text="Download", command=self.download)
        self.download_button.pack()

        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack()

    def browse(self):
        save_path = filedialog.askdirectory()
        self.path_entry.insert(0, save_path)

    def download(self):
        url = self.url_entry.get()
        save_path = self.path_entry.get()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube video URL.")
            return

        if not save_path:
            messagebox.showerror("Error", "Please enter a path to save the video.")
            return

        self.progress.start()

        try:
            yt = YouTube(url)
            stream = yt.streams.first()
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            stream.download(save_path)
            self.progress.stop()
            messagebox.showinfo("Success", "Video has been successfully downloaded.")
        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred while downloading the video: {e}")


app = Application()
app.mainloop()


# In[ ]:




