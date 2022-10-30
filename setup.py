import os
from win32com.client import Dispatch


def createShortcut(target, dest):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(dest)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.getcwd()
    shortcut.save()


runBatchText = f'cd "{os.getcwd()}" & .venv\\Scripts\\activate & pythonw run.py'
with open('run.bat', 'w') as f:
    f.write(runBatchText)

startupPath = os.path.join(os.getenv('userprofile'), 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')
programPath = os.path.join(os.getenv('userprofile'), 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs')
createShortcut(os.path.join(os.getcwd(), 'run.vbs'), os.path.join(startupPath, 'SuperDisplayFlip.lnk'))
createShortcut(os.path.join(os.getcwd(), 'run.vbs'), os.path.join(programPath, 'SuperDisplayFlip.lnk'))
