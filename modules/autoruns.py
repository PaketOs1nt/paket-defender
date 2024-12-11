from watchdog.events import    FileSystemEventHandler
from watchdog.observers import Observer

import datetime
import modules
import os

name = os.getlogin()

with open('config/REG_AUTORUN_CHECK_TIMEOUT', 'r') as f:
    REG_AUTORUN_CHECK_TIMEOUT = int(f.read())

paths = [
    r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp',
    f'C:\\Users\\{name}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
]

class MonitorAutoruns(FileSystemEventHandler):
    def on_modified(self, event):
        modules.base.notify(f'Autoruns ({event.event_type}): {event.src_path} [{datetime.datetime.now()}]')
    
    def on_created(self, event):
        modules.base.notify(f'Autoruns ({event.event_type}): {event.src_path} [{datetime.datetime.now()}]')

observer = Observer()
for path in paths:
    observer.schedule(MonitorAutoruns(), path, recursive=False)

def run():
    observer.start()