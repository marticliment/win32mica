import ctypes
import sys
import threading
import time
import winreg

import MicaTheme
import MicaStyle

def __read_registry(aKey, sKey, default, storage=winreg.HKEY_CURRENT_USER):
    registry = winreg.ConnectRegistry(None, storage)
    reg_keypath = aKey
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return default
    except Exception as e:
        print(e)
        return default
    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == sKey:
                return value
        except OSError:
            return default
        except Exception as e:
            print(e)
            return default

def __null_function() -> None:
    pass

def ApplyMica(
        HWND: int,
        Theme: bool = MicaTheme.LIGHT,
        Style: bool = MicaStyle.DEFAULT,
        OnThemeChange = __null_function,
    ) -> int:
    """Applies the mica backdrop effect on a specific hWnd

    Parameters
    ----------
    HWND : int
        The handle to the window on which the effect has to be applied
    Theme : MicaTheme, int
        The theme of the backdrop effect: MicaTheme.DARK, MicaTheme.LIGHT, MicaTheme.AUTO
    Style : MicaStyle, int
        The style of the mica backdrop effect: MicaStyle.DEFAULT, MicaStyle.ALT
    OnThemeChange : function
        A callback function to call when the system theme changes (will only work if Theme is set to MicaTheme.AUTO)

    Returns
    -------
    int
        the integer result of the win32 api call to apply the mica backdrop effect. This value will equal to 0x32 if the system is not compatible with the mica backdrop
    """

    if HWND == 0:
        raise ValueError("The parameter HWND cannot be zero")
    if Theme not in (MicaTheme.DARK, MicaTheme.LIGHT, MicaTheme.AUTO):
        raise ValueError("The parameter ColorMode has an invalid value")
    if Style not in (MicaStyle.DEFAULT, MicaStyle.ALT):
        raise ValueError("The parameter Style has an invalid value")
    
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
                ("AnimationId", ctypes.c_uint),
            ]

        class WindowCompositionAttribute(ctypes.Structure):
            _fields_ = [
                ("Attribute", ctypes.c_int),
                ("Data", ctypes.POINTER(ctypes.c_int)),
                ("SizeOfData", ctypes.c_size_t),
            ]

        class _MARGINS(ctypes.Structure):
            _fields_ = [
                ("cxLeftWidth", ctypes.c_int),
                ("cxRightWidth", ctypes.c_int),
                ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int),
            ]

        DWM_UNDOCUMENTED_MICA_ENTRY = 1029  
        DWM_UNDOCUMENTED_MICA_VALUE = 0x01 if Style == MicaStyle.DEFAULT else 0x04

        DWM_DOCUMENTED_MICA_ENTRY = 38
        DWM_DOCUMENTED_MICA_VALUE = 0x02 if Style == MicaStyle.DEFAULT else 0x04
        DWMW_USE_IMMERSIVE_DARK_MODE = 20

        SetWindowCompositionAttribute = user32.SetWindowCompositionAttribute
        DwmSetWindowAttribute = dwm.DwmSetWindowAttribute
        DwmExtendFrameIntoClientArea = dwm.DwmExtendFrameIntoClientArea

        THEME = 0x00

        def __apply_theme():
            nonlocal THEME
            OldTheme = -1
            while True:
                CurrentTheme = __read_registry(
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                    "AppsUseLightTheme",
                    0,
                )
                if OldTheme != CurrentTheme:
                    OldTheme = CurrentTheme
                    if THEME == 0x01:
                        ThemeToSet = 0x01
                    elif THEME == 0x00:
                        ThemeToSet = 0x00
                    else:
                        ThemeToSet = 0x00 if CurrentTheme != 0 else 0x01
                        try:
                            OnThemeChange()
                        except:
                            pass
                    DwmSetWindowAttribute(
                        HWND,
                        DWMW_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(ctypes.c_int(ThemeToSet)),
                        ctypes.sizeof(ctypes.c_int),
                    )
                    time.sleep(0.5)
                    DwmSetWindowAttribute(
                        HWND,
                        DWMW_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(ctypes.c_int(ThemeToSet)),
                        ctypes.sizeof(ctypes.c_int),
                    )
                    time.sleep(0.5)
                    DwmSetWindowAttribute(
                        HWND,
                        DWMW_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(ctypes.c_int(ThemeToSet)),
                        ctypes.sizeof(ctypes.c_int),
                    )
                    time.sleep(0.5)
                    DwmSetWindowAttribute(
                        HWND,
                        DWMW_USE_IMMERSIVE_DARK_MODE,
                        ctypes.byref(ctypes.c_int(ThemeToSet)),
                        ctypes.sizeof(ctypes.c_int),
                    )
                    time.sleep(0.5)
                time.sleep(0.1)

        if Theme == MicaTheme.LIGHT:
            THEME = 0x00
        elif Theme == MicaTheme.DARK:
            THEME = 0x01
        elif Theme == MicaTheme.AUTO:
            THEME = 0x02
            threading.Thread(target=__apply_theme, daemon=True, name="Win32mica helper").start()

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
                return DwmSetWindowAttribute(
                    HWND,
                    DWM_UNDOCUMENTED_MICA_ENTRY,
                    ctypes.byref(ctypes.c_int(DWM_UNDOCUMENTED_MICA_VALUE)),
                    ctypes.sizeof(ctypes.c_int),
                )
            else:
                return DwmSetWindowAttribute(
                    HWND,
                    DWM_DOCUMENTED_MICA_ENTRY,
                    ctypes.byref(ctypes.c_int(DWM_DOCUMENTED_MICA_VALUE)),
                    ctypes.sizeof(ctypes.c_int),
                )
        else:
            print(
                f"Win32Mica Error: {sys.platform} version {sys.getwindowsversion().build} is not supported"
            )
            return 0x32
    except Exception as e:
        print("Win32mica: " + str(type(e)) + ": " + str(e))
