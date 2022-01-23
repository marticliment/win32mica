import ctypes, sys, platform

class MICAMODE():
    DARK = True
    LIGHT = False


def ApplyMica(HWND: int, ColorMode: bool = MICAMODE.LIGHT) -> int:
    """Apply the new mica effect on a window making use of the hidden win32api and return an integer depending on the result of the operation
    
    Keyword arguments:
    HWND -- a handle to a window
    ColorMode -- MICAMODE.DARK or MICAMODE.LIGHT, depending on the preferred UI theme. A boolean value can also be passed, True meaning dark and False meaning light
    """
    
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

        DWM_UNDOCUMENTED_MICA_ENTRY = 1029 # Undocumented MICA (Windows 11 22523-)
        DWM_UNDOCUMENTED_MICA_VALUE = 0x01 # Undocumented MICA (Windows 11 22523-)
        
        DWM_DOCUMENTED_MICA_ENTRY = 38     # Documented MICA (Windows 11 22523+)
        DWM_DOCUMENTED_MICA_VALUE = 0x02   # Documented MICA (Windows 11 22523+)


        SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
        DwmSetWindowAttribute = dwm.DwmSetWindowAttribute 

        Acp = AccentPolicy()
        Acp.GradientColor = int("00cccccc", base=16)
        Acp.AccentState = 5

        Wca = WindowCompositionAttribute()
        Wca.Attribute = 19
        Wca.SizeOfData = ctypes.sizeof(Acp)
        Wca.Data = ctypes.cast(ctypes.pointer(Acp), ctypes.POINTER(ctypes.c_int))
        
        SetWindowCompositionAttribute(HWND, Wca)
        
        if ColorMode == MICAMODE.DARK:
            Wca.Attribute = 26
            SetWindowCompositionAttribute(HWND, Wca)

        if sys.getwindowsversion().build < 22523: # If mica is not a public API
            return DwmSetWindowAttribute(HWND, DWM_UNDOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_UNDOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))
        else: # If mica is present in the public API
            return DwmSetWindowAttribute(HWND, DWM_DOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_DOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))    
    else:
        print(f"Win32Mica Error: {sys.platform} version {sys.getwindowsversion().build} is not supported")
        return 0x32
