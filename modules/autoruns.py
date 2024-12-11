from watchdog.events import    FileSystemEventHandler
from watchdog.observers import Observer

import threading
import datetime
import modules
import winreg
import time
import os

name = os.getlogin()

with open('config/REG_AUTORUN_CHECK_TIMEOUT', 'r') as f:
    REG_AUTORUN_CHECK_TIMEOUT = int(f.read())

file_paths = [
    r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp',
    f'C:\\Users\\{name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
]

registry_paths = {
    "HKEY_CURRENT_USER": r"Software\Microsoft\Windows\CurrentVersion\Run",
    "HKEY_LOCAL_MACHINE": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
}



class MonitorAutoruns(FileSystemEventHandler):
    def on_modified(self, event):
        modules.base.notify(f'Autoruns ({event.event_type}): {event.src_path} [{datetime.datetime.now()}]')
    
    def on_created(self, event):
        modules.base.notify(f'Autoruns ({event.event_type}): {event.src_path} [{datetime.datetime.now()}]')

observer = Observer()
for path in file_paths:
    observer.schedule(MonitorAutoruns(), path, recursive=False)

def reg_get_autoruns():
    autostart_entries = {}

    for hive, subkey in registry_paths.items():
        try:
            with winreg.OpenKey(getattr(winreg, hive), subkey) as key:
                entries = {}
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        entries[name] = value
                        i += 1
                    except OSError:
                        break

                autostart_entries[hive] = entries
        except:
            autostart_entries[hive] = None
    
    return autostart_entries

def_reg_autoruns = reg_get_autoruns()

def reg_checknew():
    global def_reg_autoruns
    c_autoruns = reg_get_autoruns()
    new_entries = {}
    
    for hive, programs in c_autoruns.items():
        if hive not in def_reg_autoruns:
            new_entries[hive] = programs
        else:
            new_entries[hive] = {
                name: path for name, path in programs.items()
                if name not in def_reg_autoruns[hive]
            }
    
    def_reg_autoruns = c_autoruns
    return new_entries

def run_regcheck():
    while True:
        time.sleep(REG_AUTORUN_CHECK_TIMEOUT)
        reg_checknew()

def run():
    observer.start()
    threading.Thread(target=reg_checknew, daemon=True).start()