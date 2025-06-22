#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QProgressBar

class FolderUnOrganizer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.result_label = QtWidgets.QLabel()

        browse_frame = QtWidgets.QFrame(self)

        browse_label = QtWidgets.QLabel("Select a folder:", self)
        browse_button = QtWidgets.QPushButton("Browse", self)
        browse_button.clicked.connect(self.browse)
        self.selected_folder_entry = QtWidgets.QLineEdit(self)
        self.selected_folder_entry.setText(self.folder_path)
        self.selected_folder_entry.setReadOnly(True)

        un_organize_button = QtWidgets.QPushButton("Un-Organize Folder", self)
        un_organize_button.clicked.connect(self.un_organize_folder)

        self.progress_bar = QProgressBar(self)

        main_layout = QtWidgets.QVBoxLayout()
        browse_layout = QtWidgets.QHBoxLayout()
        browse_layout.addWidget(browse_label)
        browse_layout.addWidget(self.selected_folder_entry)
        browse_layout.addWidget(browse_button)
        main_layout.addLayout(browse_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(un_organize_button)

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setGeometry(600, 200, 600, 200)
        self.setWindowTitle("Folder Un-Organizer")
        # Attempt to set a window icon from a file in the same directory as this
        # script. The icon is optional so the application continues even if the
        # file is not present.
        icon_path = os.path.join(os.path.dirname(__file__), "Funnel Pursuit.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
        self.show()

    def browse(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select a folder:", "", options)
        self.selected_folder_entry.setText(self.folder_path)

    def un_organize_folder(self):
        selected_folder = self.folder_path
        if not selected_folder:
            self.result_label.setText("Please select a folder first.")
            return

        if not os.path.exists(selected_folder):
            self.result_label.setText("The selected folder does not exist.")
            return

        if not os.path.isdir(selected_folder):
            self.result_label.setText("The selected path is not a folder.")
            return

        subfolder_files = []
        for subdir, dirs, files in os.walk(selected_folder):
            for file in files:
                subfolder_files.append(os.path.join(subdir, file))

        for file_path in subfolder_files:
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(selected_folder, file_name)

            if file_path == new_file_path:
                continue

            if os.path.exists(new_file_path):
                i = 1
                new_file_path = os.path.join(selected_folder, "{} ({})".format(file_name, i))
                while os.path.exists(new_file_path):
                    i += 1
                    new_file_path = os.path.join(selected_folder, "{} ({})".format(file_name, i))

            try:
                os.rename(file_path, new_file_path)
            except OSError as e:
                self.result_label.setText("Error occurred while organizing the folder: {}".format(e))
                return
                
        for root, dirs, files in os.walk(selected_folder, topdown=False):
            for name in dirs:
                dir_path = os.path.join(root, name)
                if not os.listdir(dir_path):
                    try:
                        os.rmdir(dir_path)
                    except OSError as e:
                        self.result_label.setText("Error occurred while removing the empty folder: {}".format(e))
                        return
                        
        self.result_label.setText("Folder has been un-organized.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    folder_un_organizer = FolderUnOrganizer()
    sys.exit(app.exec_())


# In[ ]:




