
![](https://img.shields.io/pypi/wheel/pymica-martinet101?style=for-the-badge)
![](https://img.shields.io/pypi/v/pymica-martinet101?style=for-the-badge)
![](https://img.shields.io/pypi/l/pymica-martinet101?style=for-the-badge)
# win32mica (also known as PyMica): A simple module to add the Mica effect on legacy python windows
The aim of this project is to apply the Mica effect on python applications made with Python, like Tkinter, PyQt/PySide, WxPython, Kivy, etc.<br>

## Installation:
```pwsh
python -m pip install pymica-martinet101
```

## Requirements:
 - Windows 11
 - A **frameless** window (It might work with a normal window, bit it is not guaranteed.)
 - The HWND (identifier) of that window. More info: [what is a hwnd?](https://stackoverflow.com/questions/1635645/what-is-hwnd-in-vc) 
 - The window must have semi-transparent widgets/controls in order to recreate the transparency effect.
 - Know if Windows has dark or light mode enabled. This can be checked with the [`darkdetect` module](https://pypi.org/project/darkdetect/)

## Usage:

```python

hwnd = qtwindow.winId() # On a PyQt/PySide window
hwnd = tkwindow.frame() # On a tkinter window
# You'll need to adjust this to your program

import win32mica

isDark = True  # Dark mode mica effect
isDark = False # Light mode mica effect

import darkdetect # Auto detect
isDark = darkdetect.isDark()

win32mica.ApplyMica(hwnd, darkMode=isDark)
```

## Result:

![Demo](https://github.com/martinet101/pymica/blob/main/img/demo.png?raw=true)
