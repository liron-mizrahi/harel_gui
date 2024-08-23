import threading
import time
from nicegui import ui
import pygame
from pygame_mixer_main import visual_stim
from pygame_avs2 import avs2
from frontend import webserver
from oscpy.server import OSCThreadServer
import queue 
import camera

control_queue = queue.Queue(maxsize=10)
webcam_queue = queue.Queue(maxsize=10)

def run_nicegui():
    webserver()
    ui.run(reload=False,  host='0.0.0.0', port=8000, show=False)

def run_camera(webcam_queue): 
    vid=camera.video(webcam_queue)
    vid.run()
    
# start manager osc server    
osc_server = OSCThreadServer(encoding='utf8') 
osc_server.listen(address='0.0.0.0', port=9000, default=True)

@osc_server.address(b'/cmd')
def callback(*values):
    print("got values: {}".format(values))
    control_queue.put(values[0])
    # print(values[0] + 'written to queue')




# Start nicegui in a separate thread
frontend_thread = threading.Thread(target=run_nicegui )
frontend_thread.daemon=True
frontend_thread.start()

# # Start opencv in a separate thread
opencv_thread = threading.Thread(target=run_camera, args=(webcam_queue,) )
opencv_thread.daemon=True
opencv_thread.start()

# frontend_thread.join()
# opencv_thread.join()

# main loop 
while True: 
    time.sleep(0.1)
    msg = control_queue.get()
    if msg: 
        print(msg)
    
    if msg == 'screen_start': 
        print('start visual_stim')
        audio_file = "Bilateral Music Therapy.mp3"
        visual = visual_stim(audio_file=audio_file, webcam_queue=webcam_queue)
        visual.run()   
 
    if msg == 'avs2_start': 
        flicker = avs2()
        flicker.run()
    
    if msg == 'quit_app': 
        raise OSError('timeout while waiting for success message.')
    
