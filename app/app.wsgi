#!/usr/bin/python3
import sys
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flask")

from app import app as application
application.secret_key = 'your_secret_key'

class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        if event.event_type in ('modified', 'created', 'deleted'):
            application.logger.info('Detected file change, reloading...')
            os.kill(os.getpid(), signal.SIGINT)

observer = Observer()
observer.schedule(ReloadHandler(), path='/var/www/flask/app/', recursive=True)
observer.start()