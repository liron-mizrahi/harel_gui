import threading
import time
from nicegui import ui
import pygame
from pygame_main import visual_stim
from frontend import webserver
import queue

def run_nicegui():
    webserver()
    ui.run(reload=False,  host="127.0.0.1", port=8000)
    
# Start nicegui in a separate thread
frontend_thread = threading.Thread(target=run_nicegui )
frontend_thread.daemon=True
frontend_thread.start()

visual = visual_stim()
visual.run()