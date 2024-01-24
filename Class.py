import ctypes
from ctypes import wintypes


class PHYSICAL_MONITOR(ctypes.Structure):
    PHYSICAL_MONITOR_DESCRIPTION_SIZE = 128
    _fields_ = [('hPhysicalMonitor', wintypes.HANDLE),
                ('szPhysicalMonitorDescription', ctypes.c_wchar * PHYSICAL_MONITOR_DESCRIPTION_SIZE)]

# 用C语言进行DDC/CI协议数据的交换
user32 = ctypes.windll.user32
h_wnd = user32.GetDesktopWindow()
MONITOR_DEFAULTTOPRIMARY = 1
h_monitor = user32.MonitorFromWindow(h_wnd, MONITOR_DEFAULTTOPRIMARY)
dxva2 = ctypes.windll.Dxva2
nummons = wintypes.DWORD()
dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(h_monitor, ctypes.byref(nummons))
physical_monitors = (PHYSICAL_MONITOR * nummons.value)()
dxva2.GetPhysicalMonitorsFromHMONITOR(h_monitor, nummons, physical_monitors)
physical_monitor = physical_monitors[0]
min_brightness = wintypes.DWORD()
max_brightness = wintypes.DWORD()
cur_brightness = wintypes.DWORD()


def get_brightness():
    bres = dxva2.GetMonitorBrightness(physical_monitor.hPhysicalMonitor, ctypes.byref(
        min_brightness), ctypes.byref(cur_brightness), ctypes.byref(max_brightness))
    return cur_brightness


def set_brightness(x):
    bres = dxva2.SetMonitorBrightness(physical_monitor.hPhysicalMonitor, x)


class Brightness:
    def __init__(self):
        self.now_brightness=get_brightness().value

    def acquire(self):
        return get_brightness().value

    def increase(self):
        set_brightness(self.now_brightness+1)
        self.now_brightness+=1

    def reduce(self):
        set_brightness(self.now_brightness-1)
        self.now_brightness -= 1

    def set(self,x):
        set_brightness(x)


