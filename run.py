import re
import pywintypes
import pystray

import win32api as w
import win32con as c
from PIL import Image
from pystray import MenuItem as item
from pynput import keyboard


def checkSuperDisplay(deviceName):
    displayNo = re.search('\d+$', deviceName).group()
    print(deviceName)
    regVideoPath = w.RegQueryValueEx(HKEY_DEVICEMAP, '\Device\Video' + displayNo)[0]  # returns path to video in registry corresponding to display
    regVideoPath = regVideoPath[regVideoPath.find('System'):]

    hkey_video = w.RegOpenKeyEx(c.HKEY_LOCAL_MACHINE, regVideoPath)
    desc = w.RegQueryValueEx(hkey_video, "DriverDesc")[0]  # driver description string
    return desc.startswith('SuperDisplay')


def getSuperDisplayName():
    monitors = w.EnumDisplayMonitors()
    for m in monitors:
        mInfo = w.GetMonitorInfo(m[0])
        print(mInfo)

        if checkSuperDisplay(mInfo['Device']):
            return mInfo['Device']


def getOrientation(deviceName):
    return w.EnumDisplaySettings(deviceName).DisplayOrientation


def flip():
    global FLIP_TOGGLE
    FLIP_TOGGLE ^= 1

    deviceName = getSuperDisplayName()
    if deviceName is not None:
        settings = w.EnumDisplaySettings(deviceName)
        devmode = pywintypes.DEVMODEType()
        devmode.DisplayOrientation = FLIP_TOGGLE*3  # toggles between 0 (portrait) and 3 (landscape 270)
        devmode.PelsWidth, devmode.PelsHeight = settings.PelsHeight, settings.PelsWidth
        devmode.Fields = c.DM_DISPLAYORIENTATION | c.DM_PELSWIDTH | c.DM_PELSHEIGHT

        return w.ChangeDisplaySettingsEx(deviceName, devmode, 0)

    return 0


def onQuit():
    icon.visible = False
    icon.stop()


DEVICEMAP = 'HARDWARE\DEVICEMAP\VIDEO'
HKEY_DEVICEMAP = w.RegOpenKeyEx(c.HKEY_LOCAL_MACHINE, DEVICEMAP)
FLIP_TOGGLE = getOrientation(getSuperDisplayName()) & 1

listener = keyboard.GlobalHotKeys({'<ctrl>+<alt>+f': flip})
listener.start()

image = Image.open('icon.png')
menu = (
        item('Flip', flip, default=True),
        item('Quit', onQuit)
        )

icon = pystray.Icon("name", image, "SuperDisplayFlip", menu)
icon.run()
