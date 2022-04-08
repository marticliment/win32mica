
import tkinter as tk
from ctypes import windll
try:
    import win32mica as mc
    from PySide2 import QtWidgets, QtCore
except ImportError:
    import os
    os.system("pip install win32mica PySide2")


app=tk.Tk()
app.title("Tk Dark")
app.configure(bg="#000000")
app.wm_attributes("-transparent", "#000000")
app.update()
HWND=windll.user32.GetParent(app.winfo_id())
mc.ApplyMica(HWND, ColorMode=mc.MICAMODE.DARK)


app2=tk.Tk()
app2.title("Tk Light")
app2.configure(bg="#000000")
app2.wm_attributes("-transparent", "#000000")
app2.update()
HWND=windll.user32.GetParent(app2.winfo_id())
mc.ApplyMica(HWND, ColorMode=mc.MICAMODE.LIGHT)


app.mainloop()