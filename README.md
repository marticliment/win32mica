
![](https://img.shields.io/pypi/wheel/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/v/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/l/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/dm/win32mica?style=for-the-badge)
# Win32mica (aka PyMica): A simple module to add the Mica effect on legacy python windows
The aim of this project is to apply the Mica effect on python applications made with Python, like Tkinter, PyQt/PySide, WxPython, Kivy, etc.<br>

View this project also on [PyPi](https://pypi.org/project/win32mica/)

## Installation:
```pwsh
python -m pip install win32mica
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

from win32mica import MICAMODE, ApplyMica

mode = MICAMODE.DARK  # Dark mode mica effect
mode = MICAMODE.LIGHT # Light mode mica effect

import darkdetect # Auto mode detect
mode = darkdetect.isDark()

win32mica.ApplyMica(hwnd, mode)
```

## Result:

![Demo](https://github.com/martinet101/pymica/blob/main/img/demo.png?raw=true)<br>
_This is a PySide2 window with custom transparent widgets. The screenshot has been taken on dark mode._
