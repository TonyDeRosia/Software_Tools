#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import sys
import os

class AffiliateLink:
    def __init__(self, name, clicks, conversions, earnings, date):
        try:
            self.clicks = float(clicks)
            self.conversions = float(conversions)
            self.earnings = float(earnings)
        except ValueError:
            raise ValueError("Clicks, conversions, and earnings must be numbers.")

        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self.name = name

        if not isinstance(date, str):
            raise TypeError("Date must be a string.")
        self.date = date
        self.checked = False

    def conversion_rate(self):
        if self.clicks == 0:
            return 0
        return self.conversions / self.clicks

    def earnings_per_click(self):
        if self.clicks == 0:
            return 0
        return self.earnings / self.clicks

class AffiliateReportApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_menu()
        self.setWindowTitle("Affiliate Link Report")
        self.resize(1300, 400)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.links = []
        self.file_path = None
        self.currency = "$"
        self.name_label = QtWidgets.QLabel("Name")
        self.clicks_label = QtWidgets.QLabel("Clicks")
        self.conversions_label = QtWidgets.QLabel("Conversions")
        self.earnings_label = QtWidgets.QLabel("Earnings")
        self.date_label = QtWidgets.QLabel("Date")
        self.name_entry = QtWidgets.QLineEdit()
        self.clicks_entry = QtWidgets.QLineEdit()
        self.conversions_entry = QtWidgets.QLineEdit()
        self.earnings_entry = QtWidgets.QLineEdit()
        self.date_entry = QtWidgets.QLineEdit()
        self.add_button = QtWidgets.QPushButton("Add")
        #self.save_button = QtWidgets.QPushButton("Save")
        #self.load_button = QtWidgets.QPushButton("Load")
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.delete_button = QtWidgets.QPushButton("Delete")
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setHeaderLabels(["Name", "Clicks", "Conversions", "Earnings", "Date", "Conversion Rate", "Earnings per Click"])
        grid = QtWidgets.QGridLayout(self.central_widget)
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.clicks_label, 0, 2)
        grid.addWidget(self.conversions_label, 0, 4)
        grid.addWidget(self.earnings_label, 0, 6)
        grid.addWidget(self.date_label, 0, 8)
        grid.addWidget(self.name_entry, 1, 1)
        grid.addWidget(self.clicks_entry, 1, 3)
        grid.addWidget(self.conversions_entry, 1, 5)
        grid.addWidget(self.earnings_entry, 1, 7)
        grid.addWidget(self.date_entry, 1, 9)
        grid.addWidget(self.add_button, 1, 10)
        #grid.addWidget(self.save_button, 2, 10)
        #grid.addWidget(self.load_button, 3, 10)
        grid.addWidget(self.clear_button, 2, 10)

        grid.addWidget(self.delete_button, 3, 10)
        self.delete_button.clicked.connect(self.delete_link)
        
        grid.addWidget(self.tree, 4, 0, 1, 11)
        self.add_button.clicked.connect(self.add_link)
        #self.save_button.clicked.connect(self.save_report)
        #self.load_button.clicked.connect(self.load_report)
        self.clear_button.clicked.connect(self.clear_entries)

    def delete_link(self):
        selected = self.tree.selectedItems()
        if not selected:
            return

        items_to_delete = []
        for item in selected:
            link_index = self.tree.indexOfTopLevelItem(item)
            items_to_delete.append(link_index)

        for index in reversed(sorted(items_to_delete)):
            self.tree.takeTopLevelItem(index)
            del self.links[index]

    def update_tree(self):
        self.tree.clear()
        for link in self.links:
            item = QtWidgets.QTreeWidgetItem([link.name, str(link.clicks), str(link.conversions), str(link.earnings), link.date, "{:.2%}".format(link.conversion_rate()), "{}{:.2f}".format(self.currency, link.earnings_per_click())])
            self.tree.addTopLevelItem(item)

    def add_link(self):
        name = self.name_entry.text().strip()
        clicks = self.clicks_entry.text().strip()
        conversions = self.conversions_entry.text().strip()
        earnings = self.earnings_entry.text().strip()
        date = self.date_entry.text().strip()
        if not name or not clicks or not conversions or not earnings or not date:
            return

        # validate the data types
        try:
            clicks = int(clicks)
            conversions = int(conversions)
            earnings = float(earnings)
        except ValueError:
            # show an error message if the data types are not valid
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setText("Clicks, Conversions, and Earnings must be numbers.")
            error_message.exec_()
            return

        # validate the date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            # show an error message if the date format is not valid
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setText("Date must be in the format YYYY-MM-DD.")
            error_message.exec_()
            return

        link = AffiliateLink(name, clicks, conversions, earnings, date)
        self.links.append(link)
        self.update_tree()
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.clear()
        self.clicks_entry.clear()
        self.conversions_entry.clear()
        self.earnings_entry.clear()
        self.date_entry.clear()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        save_action = QtWidgets.QAction("Save", self)
        save_action.triggered.connect(self.save_report)
        file_menu.addAction(save_action)
        load_action = QtWidgets.QAction("Load", self)
        load_action.triggered.connect(self.load_report)
        file_menu.addAction(load_action)

    def save_report(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Report", "", "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Name,Clicks,Conversions,Earnings,Date\n")
            for link in self.links:
                file.write("{},{}, {},{},{}\n".format(link.name, link.clicks, link.conversions, link.earnings, link.date))
                
    def load_report(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Report", "", "Comma Separated Values (.csv);;All Files ()", options=options)
        if not file_path:
            return
        self.links.clear()
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                next(file) # skip header
                for line in file:
                    name, clicks, conversions, earnings, date = line.strip().split(",")
                    self.links.append(AffiliateLink(name, clicks, conversions, earnings, date))
                    self.update_tree()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occured while opening the file: {e}")
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AffiliateReportApp()
    window.show()
    sys.exit(app.exec_())


# In[ ]:


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import sys
import os

class AffiliateLink:
    def __init__(self, name, clicks, conversions, earnings, date):
        try:
            self.clicks = float(clicks)
            self.conversions = float(conversions)
            self.earnings = float(earnings)
        except ValueError:
            raise ValueError("Clicks, conversions, and earnings must be numbers.")

        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        self.name = name

        if not isinstance(date, str):
            raise TypeError("Date must be a string.")
        self.date = date
        self.checked = False

    def conversion_rate(self):
        if self.clicks == 0:
            return 0
        return self.conversions / self.clicks

    def earnings_per_click(self):
        if self.clicks == 0:
            return 0
        return self.earnings / self.clicks

class AffiliateReportApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_menu()
        self.setWindowTitle("Affiliate Link Report")
        
        self.logo_pixmap = QtGui.QPixmap("C:/Users/antho/Documents/Python/logo.png/Funnel Pursuit.png")
        self.setWindowIcon(QtGui.QIcon(self.logo_pixmap))
        self.resize(1300, 400)
        self.central_widget = QtWidgets.QWidget(self)
        
        self.resize(1300, 400)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.links = []
        self.file_path = None
        self.currency = "$"
        self.name_label = QtWidgets.QLabel("Name")
        self.clicks_label = QtWidgets.QLabel("Clicks")
        self.conversions_label = QtWidgets.QLabel("Conversions")
        self.earnings_label = QtWidgets.QLabel("Earnings")
        self.date_label = QtWidgets.QLabel("Date")
        self.name_entry = QtWidgets.QLineEdit()
        self.clicks_entry = QtWidgets.QLineEdit()
        self.conversions_entry = QtWidgets.QLineEdit()
        self.earnings_entry = QtWidgets.QLineEdit()
        self.date_entry = QtWidgets.QLineEdit()
        self.add_button = QtWidgets.QPushButton("Add")
        #self.save_button = QtWidgets.QPushButton("Save")
        #self.load_button = QtWidgets.QPushButton("Load")
        self.clear_button = QtWidgets.QPushButton("Clear")
        self.delete_button = QtWidgets.QPushButton("Delete")
        
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setHeaderLabels(["Name", "Clicks", "Conversions", "Earnings", "Date", "Conversion Rate", "Earnings per Click"])
        grid = QtWidgets.QGridLayout(self.central_widget)
        grid.addWidget(self.name_label, 0, 0)
        grid.addWidget(self.clicks_label, 0, 2)
        grid.addWidget(self.conversions_label, 0, 4)
        grid.addWidget(self.earnings_label, 0, 6)
        grid.addWidget(self.date_label, 0, 8)
        grid.addWidget(self.name_entry, 1, 1)
        grid.addWidget(self.clicks_entry, 1, 3)
        grid.addWidget(self.conversions_entry, 1, 5)
        grid.addWidget(self.earnings_entry, 1, 7)
        grid.addWidget(self.date_entry, 1, 9)
        grid.addWidget(self.add_button, 1, 10)
        #grid.addWidget(self.save_button, 2, 10)
        #grid.addWidget(self.load_button, 3, 10)
        grid.addWidget(self.clear_button, 2, 10)
        
        grid.addWidget(self.delete_button, 3, 10)
        self.delete_button.clicked.connect(self.delete_link)
        
        grid.addWidget(self.tree, 4, 0, 1, 11)
        self.add_button.clicked.connect(self.add_link)
        #self.save_button.clicked.connect(self.save_report)
        #self.load_button.clicked.connect(self.load_report)
        self.clear_button.clicked.connect(self.clear_entries)

    def delete_link(self):
        selected = self.tree.selectedItems()
        if not selected:
            return

        items_to_delete = []
        for item in selected:
            link_index = self.tree.indexOfTopLevelItem(item)
            items_to_delete.append(link_index)

        for index in reversed(sorted(items_to_delete)):
            self.tree.takeTopLevelItem(index)
            del self.links[index]

    def update_tree(self):
        self.tree.clear()
        for link in self.links:
            item = QtWidgets.QTreeWidgetItem([link.name, str(link.clicks), str(link.conversions), str(link.earnings), link.date, "{:.2%}".format(link.conversion_rate()), "{}{:.2f}".format(self.currency, link.earnings_per_click())])
            self.tree.addTopLevelItem(item)

    def add_link(self):
        name = self.name_entry.text().strip()
        clicks = self.clicks_entry.text().strip()
        conversions = self.conversions_entry.text().strip()
        earnings = self.earnings_entry.text().strip()
        date = self.date_entry.text().strip()
        if not name or not clicks or not conversions or not earnings or not date:
            return

        # validate the data types
        try:
            clicks = int(clicks)
            conversions = int(conversions)
            earnings = float(earnings)
        except ValueError:
            # show an error message if the data types are not valid
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setText("Clicks, Conversions, and Earnings must be numbers.")
            error_message.exec_()
            return

        # validate the date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            # show an error message if the date format is not valid
            error_message = QMessageBox()
            error_message.setWindowTitle("Error")
            error_message.setText("Date must be in the format YYYY-MM-DD.")
            error_message.exec_()
            return

        link = AffiliateLink(name, clicks, conversions, earnings, date)
        self.links.append(link)
        self.update_tree()
        self.clear_entries()

    def clear_entries(self):
        self.name_entry.clear()
        self.clicks_entry.clear()
        self.conversions_entry.clear()
        self.earnings_entry.clear()
        self.date_entry.clear()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        save_action = QtWidgets.QAction("Save", self)
        save_action.triggered.connect(self.save_report)
        file_menu.addAction(save_action)
        load_action = QtWidgets.QAction("Load", self)
        load_action.triggered.connect(self.load_report)
        file_menu.addAction(load_action)

    def save_report(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Report", "", "Comma Separated Values (*.csv);;All Files (*)", options=options)
        if not file_path:
            return
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Name,Clicks,Conversions,Earnings,Date\n")
            for link in self.links:
                file.write("{},{}, {},{},{}\n".format(link.name, link.clicks, link.conversions, link.earnings, link.date))
                
    def load_report(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Report", "", "Comma Separated Values (.csv);;All Files ()", options=options)
        if not file_path:
            return
        self.links.clear()
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                next(file) # skip header
                for line in file:
                    name, clicks, conversions, earnings, date = line.strip().split(",")
                    self.links.append(AffiliateLink(name, clicks, conversions, earnings, date))
                    self.update_tree()
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"An error occured while opening the file: {e}")
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AffiliateReportApp()
    window.show()
    sys.exit(app.exec_())


# In[ ]:




