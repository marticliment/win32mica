import ctypes, sys, platform


def ApplyMica(HWND: int, darkMode: bool):
    if sys.platform == "win32" and sys.getwindowsversion().build >= 22000:
        user32 = ctypes.windll.user32
        dwm = ctypes.windll.dwmapi

        class AccentPolicy(ctypes.Structure):
            _fields_ = [
                ("AccentState", ctypes.c_uint),
                ("AccentFlags", ctypes.c_uint),
                ("GradientColor", ctypes.c_uint),
                ("AnimationId", ctypes.c_uint)
            ]

        class WindowCompositionAttribute(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.POINTER(ctypes.c_int)),
                ("SizeOfData", ctypes.c_size_t)
            ]

        SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
        DwmSetWindowAttribute = dwm.DwmSetWindowAttribute 

        ACC = AccentPolicy()
        ACC.GradientColor = int("00cccccc", base=16)
        ACC.AccentState = 5

        WCA = WindowCompositionAttribute()
        WCA.Attribute = 19
        WCA.SizeOfData = ctypes.sizeof(ACC)
        WCA.Data = ctypes.cast(ctypes.pointer(ACC), ctypes.POINTER(ctypes.c_int))
        
        SetWindowCompositionAttribute(HWND, WCA)
        
        if darkMode:
            WCA.Attribute = 26
            SetWindowCompositionAttribute(HWND, WCA)

        DwmSetWindowAttribute(HWND, 1029, ctypes.byref(ctypes.c_int(0x01)), ctypes.sizeof(ctypes.c_int))
    else:
        raise OSError(f"{sys.platform} version {sys.getwindowsversion().build} is not supported")


ApplyMica(0, False)