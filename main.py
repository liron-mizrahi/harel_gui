import threading
import time
from nicegui import ui
import pygame
from pygame_main import visual_stim
from frontend import webserver
from oscpy.server import OSCThreadServer

def run_nicegui():
    webserver()
    ui.run(reload=False,  host='0.0.0.0', port=8000)
    
# start manager osc server    
osc_server = OSCThreadServer(encoding='utf8') 
osc_server.listen(address='0.0.0.0', port=9000, default=True)

@osc_server.address(b'/cmd')
def callback(*values):
    print("got values: {}".format(values))



# Start nicegui in a separate thread
frontend_thread = threading.Thread(target=run_nicegui )
frontend_thread.daemon=True
frontend_thread.start()

visual = visual_stim()
visual.run()