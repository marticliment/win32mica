import ctypes, sys, threading, time, winreg

class MICAMODE():
    DARK = True
    LIGHT = False


debugging = False

def readRegedit(aKey, sKey, default, storage=winreg.HKEY_CURRENT_USER):
    registry = winreg.ConnectRegistry(None, storage)
    reg_keypath = aKey
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError as e:
        return default
    except Exception as e:
        print(e)
        return default

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == sKey:
                return value
        except OSError as e:
            return default
        except Exception as e:
            print(e)
            return default


def ApplyMica(HWND: int, ColorMode: bool = MICAMODE.LIGHT, darkModeMode: int = 20) -> int:
    """Apply the new mica effect on a window making use of the hidden win32api and return an integer depending on the result of the operation
    
    Keyword arguments:
    HWND -- a handle to a window (it being an integer value)
    ColorMode -- MICAMODE.DARK or MICAMODE.LIGHT, depending on the preferred UI theme. A boolean value can also be passed, True meaning Dark and False meaning Light
    """
    try:
        HWND = int(HWND)
    except ValueError:
        HWND = int(str(HWND), 16)
    
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

    class _MARGINS(ctypes.Structure):
        _fields_ = [("cxLeftWidth", ctypes.c_int),
                    ("cxRightWidth", ctypes.c_int),
                    ("cyTopHeight", ctypes.c_int),
                    ("cyBottomHeight", ctypes.c_int)
                    ]

    DWM_UNDOCUMENTED_MICA_ENTRY = 1029 # Undocumented MICA (Windows 11 22523-)
    DWM_UNDOCUMENTED_MICA_VALUE = 0x01 # Undocumented MICA (Windows 11 22523-)
    
    DWM_DOCUMENTED_MICA_ENTRY = 38     # Documented MICA (Windows 11 22523+)
    DWM_DOCUMENTED_MICA_VALUE = 0x02   # Documented MICA (Windows 11 22523+)
    DWMW_USE_IMMERSIVE_DARK_MODE = 20
    

    SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
    DwmSetWindowAttribute = dwm.DwmSetWindowAttribute 
    DwmExtendFrameIntoClientArea = dwm.DwmExtendFrameIntoClientArea

    if ColorMode == MICAMODE.DARK: # Apply dark mode
        def setMode():
            oldMode = -1
            while True:
                mode = readRegedit(r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 0)
                if oldMode != mode:
                    oldMode = mode
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(0x01)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(0x01)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(0x01)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(0x01)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                time.sleep(0.1)
                    


        threading.Thread(target=setMode, daemon=True, name="win32mica: ensure dark mode").start()
        
    else: # Apply light mode
        DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(0x00)), ctypes.sizeof(ctypes.c_int)) 


    if sys.platform == "win32" and sys.getwindowsversion().build >= 22000:

        Acp = AccentPolicy()
        Acp.GradientColor = int("00cccccc", base=16)
        Acp.AccentState = 5
        Acp.AccentPolicy = 19

        Wca = WindowCompositionAttribute()
        Wca.Attribute = 20
        Wca.SizeOfData = ctypes.sizeof(Acp)
        Wca.Data = ctypes.cast(ctypes.pointer(Acp), ctypes.POINTER(ctypes.c_int))

        Mrg = _MARGINS(-1, -1, -1, -1)
        
        o = DwmExtendFrameIntoClientArea(HWND, ctypes.byref(Mrg))
        if debugging:
            if o != 0:
                print("Win32mica: Failed to DwmExtendFrameIntoClientArea", hex(o+0xffffffff))
            else:
                print("Win32mica: DwmExtendFrameIntoClientArea Ok")
        o = SetWindowCompositionAttribute(HWND, Wca)
        if debugging:
            if o != 0:
                print("Win32mica: Failed to SetWindowCompositionAttribute", o)
            else:
                print("Win32mica: SetWindowCompositionAttribute Ok")
        
        if ColorMode == MICAMODE.DARK:
            Wca.Attribute = 1
            o = SetWindowCompositionAttribute(HWND, Wca)
            if debugging:
                if o != 0:
                    print("Win32mica: Failed to SetWindowCompositionAttribute (dark mode)", o)
                else:
                    print("Win32mica: SetWindowCompositionAttribute OK (dark mode)", o)
        else:
            if debugging:
                print("Win32mica: No SetWindowCompositionAttribute (light mode)")

        if sys.getwindowsversion().build < 22523: # If mica is not a public API
            return DwmSetWindowAttribute(HWND, DWM_UNDOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_UNDOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))
        else: # If mica is present in the public API
            return DwmSetWindowAttribute(HWND, DWM_DOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_DOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))    
    else:
        print(f"Win32Mica Error: {sys.platform} version {sys.getwindowsversion().build} is not supported")
        return 0x32


