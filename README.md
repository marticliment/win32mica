
![](https://img.shields.io/pypi/wheel/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/v/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/l/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/win32mica?style=for-the-badge)
![](https://img.shields.io/pypi/dm/win32mica?style=for-the-badge)
# Win32mica: A simple module to add the Mica effect and enable immersive dark mode on Python UI Windows
The aim of this project is to apply the Mica effect and enable immersive dark mode on python applications made with Python, like Tkinter, PyQt/PySide, WxPython, Kivy, etc.<br> This will work on any windows version, including the new released dev builds where the mica API is public.

View this project on [PyPi](https://pypi.org/project/win32mica/)
View this project on [GitHub](https://github.com/martinet101/win32mica)


https://github.com/marticliment/win32mica/assets/53119851/b0c4ce98-9845-449d-94e6-caaa37fc752a


## Installation:
```pwsh
python -m pip install win32mica
```

## Requirements:
 - Windows 11
 - A window set to not have a transparent background and to have extended composition enabled* (It might work with other settings, but nothing is guaranteed.)
 - The hWnd (identifier) of that window. More info: [what is a hWnd?](https://stackoverflow.com/questions/1635645/what-is-hwnd-in-vc) 
 - OPTIONAL: The window must have semi-transparent widgets/controls in order to recreate the transparency effect on the controls.
 - OPTIONAL: Know if Windows has dark or light mode enabled. This can be checked with the [`darkdetect` module](https://pypi.org/project/darkdetect/)

## Usage:

```python
######################################################################
#                                                                    #
# Those examples are oversimplified, please see the examples/ folder #
# for detailed usage with each UI library.                           #
#                                                                    #
######################################################################

hwnd = window.winId().__int__() # Get the hWnd of your window

from win32mica import ApplyMica, MicaTheme, MicaStyle

mode = MicaTheme.DARK  # Dark mode mica effect
mode = MicaTheme.LIGHT # Light mode mica effect
mode = MicaTheme.AUTO  # Apply system theme, and change it if system theme changes

style = MicaStyle.DEFAULT # Default backdrop effect
style = MicaStyle.ALT     # Alt backdrop effect

def callbackFunction(NewTheme):
    if newTheme == MicaTheme.DARK:
        print("Theme has changed to dark!")
    else:
        print("Theme has changed to light!")

win32mica.ApplyMica(HWND=hwnd, Theme=mode, Style=style, OnThemeChange=callbackFunction)

#    Parameters
#    ----------
#    HWND : int
#        The handle to the window on which the effect has to be applied
#    Theme : MicaTheme, int
#        The theme of the backdrop effect: MicaTheme.DARK, MicaTheme.LIGHT, MicaTheme.AUTO
#    Style : MicaStyle, int
#        The style of the mica backdrop effect: MicaStyle.DEFAULT, MicaStyle.ALT
#    OnThemeChange : function
#        A callback function that receives one parameter to call when the system theme changes (will only work if Theme is set to MicaTheme.AUTO)
#        The passed parameter will be either MicaTheme.DARK or MicaTheme.LIGHT, corresponding to the new system theme

```

You can check out the [examples folder](https://github.com/martinet101/win32mica/tree/main/examples) for detailed use in Tk and PySide/PyQt.

## Result:

![image](https://user-images.githubusercontent.com/53119851/188261331-15e17447-590f-452a-be62-07c67a3db673.png)<br>
![image](https://user-images.githubusercontent.com/53119851/188261398-83f5d904-586f-47ce-b6af-d4521eb3f68f.png)

_Those are PySide2 windows with custom widgets._

