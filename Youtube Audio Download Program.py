#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import os
from pytube import YouTube


class Application(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.resize(400, 200)

        # Optional application icon loaded from the same directory as this file
        icon_path = os.path.join(os.path.dirname(__file__), "Funnel Pursuit.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        self.central_widget = QtWidgets.QWidget(self)

        self.url_label = QtWidgets.QLabel("Enter the YouTube video URL:", self.central_widget)
        self.url_entry = QtWidgets.QLineEdit(self.central_widget)

        self.path_label = QtWidgets.QLabel("Enter the path to save the video:", self.central_widget)
        self.path_entry = QtWidgets.QLineEdit(self.central_widget)
        self.browse_button = QtWidgets.QPushButton("Browse", self.central_widget, clicked=self.browse)

        self.download_button = QtWidgets.QPushButton("Download", self.central_widget, clicked=self.download)

        self.progress = QtWidgets.QProgressBar(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.path_label)
        self.layout.addWidget(self.path_entry)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.progress)
        self.setCentralWidget(self.central_widget)

    def browse(self):
        save_path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.path_entry.setText(save_path)

    def download(self):
        url = self.url_entry.text()
        save_path = self.path_entry.text()

        if not url:
            QMessageBox.critical(self, "Error", "Please enter a YouTube video URL.")
            return

        if not save_path:
            QMessageBox.critical(self, "Error", "Please enter a path to save the video.")
            return

        self.progress.show()

        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            stream.download(save_path)
            QMessageBox.information(self, "Success", "The audio has been downloaded")
            
            self.progress.hide()
            QMessageBox.information(self, "Success", "The audio has been successfully downloaded.")
        except Exception as e:
            self.progress.hide()
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    sys.exit(app.exec_())


# In[1]:


import os
import sys
from typing import Optional

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pytube import YouTube


class VideoDownloader:
    def __init__(self, url: str, save_path: str):
        self.url = url
        self.save_path = save_path

    def download(self):
        if not self.url:
            raise ValueError("Please enter a YouTube video URL.")
        if not self.save_path:
            raise ValueError("Please enter a path to save the video.")
        yt = YouTube(self.url)
        stream = yt.streams.filter(only_audio=True).first()
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
        stream.download(self.save_path)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Downloader")
        self.resize(400, 200)

        icon_path = os.path.join(os.path.dirname(__file__), "Funnel Pursuit.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        self.central_widget = QtWidgets.QWidget(self)

        self.url_label = QtWidgets.QLabel("Enter the YouTube video URL:", self.central_widget)
        self.url_entry = QtWidgets.QLineEdit(self.central_widget)

        self.path_label = QtWidgets.QLabel("Enter the path to save the video:", self.central_widget)
        self.path_entry = QtWidgets.QLineEdit(self.central_widget)
        self.browse_button = QtWidgets.QPushButton("Browse", self.central_widget)

        self.browse_button.clicked.connect(self.select_folder)
        self.download_button = QtWidgets.QPushButton("Download", self.central_widget)
        self.download_button.clicked.connect(self.download_video)

        self.url_layout = QtWidgets.QHBoxLayout()
        self.url_layout.addWidget(self.url_label)
        self.url_layout.addWidget(self.url_entry)

        self.path_layout = QtWidgets.QHBoxLayout()
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_entry)
        self.path_layout.addWidget(self.browse_button)

        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.main_layout.addLayout(self.url_layout)
        self.main_layout.addLayout(self.path_layout)
        self.main_layout.addWidget(self.download_button)

        self.setCentralWidget(self.central_widget)

    def select_folder(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder", "", options=options)
        if folder:
            self.path_entry.setText(folder)

    def download_video(self):
        url = self.url_entry.text()
        path = self.path_entry.text()
        video_downloader = VideoDownloader(url, path)
        try:
            video_downloader.download()
            QMessageBox.information(self, "Success", "Video has been downloaded successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


# In[ ]:




