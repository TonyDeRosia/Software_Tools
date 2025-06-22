# Software Tools

This repository contains several standalone Python scripts that provide small desktop utilities built with PyQt5 or Tkinter.

## Installation

Install Python 3 and use `pip` to install the dependencies:

```bash
pip install PyQt5 moviepy pytube
```

These packages are required for the graphical applications and video features provided by the scripts below.

## Scripts

### Easy_Video_Format_Converter

Converts a selected video file to a different format using a simple PyQt5 interface.

**Usage:**
```bash
python Easy_Video_Format_Converter
```
**Requires:** `PyQt5`, `moviepy`

### File Organizer Choose Which Data Types To Organize.py

Organizes files in a chosen folder into sub‑folders based on file extensions using a Tkinter GUI.

**Usage:**
```bash
python "File Organizer Choose Which Data Types To Organize.py"
```
**Requires:** standard library only (`tkinter` comes with Python)

### Folder Un-Organizer.py

Moves files from nested sub‑folders back into the selected folder and removes the empty directories. Built with PyQt5.

**Usage:**
```bash
python "Folder Un-Organizer.py"
```
**Requires:** `PyQt5`

### Legal Disclaimer Information Generator.py

Displays prewritten Terms of Service, Privacy Policy, and Disclaimer text in a PyQt5 window.

**Usage:**
```bash
python "Legal Disclaimer Information Generator.py"
```
**Requires:** `PyQt5`

### Sales and Marketing version 1.py

A small PyQt5 application to track affiliate link statistics and generate CSV reports.

**Usage:**
```bash
python "Sales and Marketing version 1.py"
```
**Requires:** `PyQt5`

### Youtube Audio Download Program.py

Downloads the audio stream of a YouTube video to a specified directory using PyQt5 for the interface.

**Usage:**
```bash
python "Youtube Audio Download Program.py"
```
**Requires:** `PyQt5`, `pytube`

### Youtube Single Video Download Program.py

Downloads a single YouTube video using a Tkinter interface.

**Usage:**
```bash
python "Youtube Single Video Download Program.py"
```
**Requires:** `pytube` (uses Tkinter which is included with Python)

