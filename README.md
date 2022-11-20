
![](https://img.shields.io/pypi/wheel/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/v/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/l/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/dm/win32mica?style=for-the-badge)
# Win32mica: A simple module to add the Mica effect on Python UI Windows
The aim of this project is to apply the Mica effect on python applications made with Python, like Tkinter, PyQt/PySide, WxPython, Kivy, etc.<br> This will work on any windows version, including the new released dev builds where the mica API is public.

View this project on [PyPi](https://pypi.org/project/win32mica/)
View this project on [GitHub](https://github.com/martinet101/win32mica)

## Installation:
```pwsh
python -m pip install win32mica
```

## Requirements:
 - Windows 11
 - A window set to not have a transparent background and to have extended composition enabled* (It might work with other settings, but nothing is guaranteed.)
 - The HWND (identifier) of that window. More info: [what is a hwnd?](https://stackoverflow.com/questions/1635645/what-is-hwnd-in-vc) 
 - OPTIONAL: The window must have semi-transparent widgets/controls in order to recreate the transparency effect on the controls.
 - OPTIONAL: Know if Windows has dark or light mode enabled. This can be checked with the [`darkdetect` module](https://pypi.org/project/darkdetect/)

## Usage:

```python
#####################################################################
#                                                                   #
# Those examples are oversimplified, please see the examples folder #
# for detailed usage with each UI library.                          #
#                                                                   #
#####################################################################

hwnd = qtwindow.winId().__int__() # On a PyQt/PySide window
hwnd = tkwindow.frame() # On a tkinter window
# You'll need to adjust this to your program

from win32mica import MICAMODE, ApplyMica

mode = MICAMODE.DARK  # Dark mode mica effect
mode = MICAMODE.LIGHT # Light mode mica effect
# Choose one of them following your app color scheme

import darkdetect # You can pass the darkdetect return value directly, since the ColorMode accepts bool values (True -> dark, False -> light)
mode = darkdetect.isDark()

win32mica.ApplyMica(hwnd, mode)
```

You can check out the [examples folder](https://github.com/martinet101/win32mica/tree/main/examples) for detailed use in Tk and PySide/PyQt.

## Result:

![image](https://user-images.githubusercontent.com/53119851/188261331-15e17447-590f-452a-be62-07c67a3db673.png)<br>
![image](https://user-images.githubusercontent.com/53119851/188261398-83f5d904-586f-47ce-b6af-d4521eb3f68f.png)

_Those are PySide2 windows with custom widgets._


## Troubleshooting:

For more information about possible errors/mistakes, make sure to add the following before using win32mica:


```python
# Add these lines at the very start of your script
import win32mica
win32mica.debugging = True
```
