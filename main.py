import threading
import time
from nicegui import ui
import pygame
from pygame_main import visual_stim
from osc_server import osc_server
from frontend import webserver
import queue


def run_nicegui(queue):
    webserver(queue)
    ui.run(reload=False,  host="127.0.0.1", port=8000)

def run_osc_server(msg_queue): 
    osc= osc_server(msg_queue)
    osc.run()
    
msg_queue=queue.Queue()
 
# start osc_server thread
osc_Server_thread = threading.Thread( target=run_osc_server, args=(msg_queue, ))    
osc_Server_thread.daemon=True
osc_Server_thread.start()
    
# Start nicegui in a separate thread
frontend_thread = threading.Thread(target=run_nicegui, args=(msg_queue, ))
frontend_thread.daemon=True
frontend_thread.start()

visual = visual_stim()
visual.run()