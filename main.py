import threading
import time
from nicegui import ui
import pygame
from pygame_mixer_main import visual_stim
from frontend import webserver
from oscpy.server import OSCThreadServer
import queue 

control_queue = queue.Queue()

def run_nicegui():
    webserver()
    ui.run(reload=False,  host='0.0.0.0', port=8000, show=False)

# start manager osc server    
osc_server = OSCThreadServer(encoding='utf8') 
osc_server.listen(address='0.0.0.0', port=9000, default=True)

@osc_server.address(b'/cmd')
def callback(*values):
    print("got values: {}".format(values))
    
    control_queue.put(values[0])




# Start nicegui in a separate thread
frontend_thread = threading.Thread(target=run_nicegui )
frontend_thread.daemon=True
frontend_thread.start()


# main loop 
while True: 
    time.sleep(0.1)
    msg = control_queue.get()
    if msg: 
        print(msg)
    
    if msg == 'screen_start': 
        audio_file = "Bilateral Music Therapy.mp3"
        visual = visual_stim(audio_file)
        # visual = visual_stim()
        visual.run()   
    
    
    if msg == 'quit_app': 
        raise OSError('timeout while waiting for success message.')
    
