import ctypes, sys, threading, time, winreg

class MICAMODE():
    DARK = 1
    LIGHT = 0
    AUTO = 2

class MicaMode():
    DARK = 1
    LIGHT = 0
    AUTO = 2


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

def nullFunction():
    pass
    
def ApplyMica(HWND: int, ColorMode: bool = MicaMode.LIGHT, onThemeChange = nullFunction) -> int:
    """Apply the new mica effect on a window making use of the hidden win32api and return an integer depending on the result of the operation
    
    Keyword arguments:
    HWND -- a handle to a window (it being an integer value)
    ColorMode -- MicaMode.DARK or MicaMode.LIGHT, depending on the preferred UI theme. A boolean value can also be passed, True meaning Dark and False meaning Light
    onThemeChange -- a function to call when the system theme changes. Will be called only if ColorMode is set to MicaMode.AUTO
    """
    try:
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
        
        MODE = 0x00

        def setMode():
            nonlocal MODE
            OldMode = -1
            while True:
                CurrentMode = readRegedit(r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 0)
                if OldMode != CurrentMode:
                    
                    OldMode = CurrentMode
                    if MODE == 0x01:
                        ModeToSet = 0x01
                    elif MODE == 0x00:
                        ModeToSet = 0x00
                    else:
                        ModeToSet = 0x00 if CurrentMode != 0 else 0x01
                        try:
                            onThemeChange()
                        except:
                            pass
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(ModeToSet)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(ModeToSet)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(ModeToSet)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                    DwmSetWindowAttribute(HWND, DWMW_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(ModeToSet)), ctypes.sizeof(ctypes.c_int))
                    time.sleep(0.5)
                time.sleep(0.1)
        
        if ColorMode == MicaMode.DARK:
            MODE = 0x01
        elif ColorMode == MicaMode.LIGHT:
            MODE = 0x00
        else: # ColorMode == MicaMode.AUTO
            MODE = 0x02
        
        threading.Thread(target=setMode, daemon=True, name="win32mica: theme thread").start()

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
            try:
                o = SetWindowCompositionAttribute(HWND, Wca)
            except ctypes.ArgumentError:
                pass

            if sys.getwindowsversion().build < 22523:
                return DwmSetWindowAttribute(HWND, DWM_UNDOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_UNDOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))
            else:
                return DwmSetWindowAttribute(HWND, DWM_DOCUMENTED_MICA_ENTRY, ctypes.byref(ctypes.c_int(DWM_DOCUMENTED_MICA_VALUE)), ctypes.sizeof(ctypes.c_int))    
        else:
            print(f"Win32Mica Error: {sys.platform} version {sys.getwindowsversion().build} is not supported")
            return 0x32
    except Exception as e:
        print("Win32mica: "+str(type(e))+": "+str(e))


