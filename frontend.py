# frontnd.py
from nicegui import Client, app, core, run, ui
from nicegui import events
from pythonosc.udp_client import SimpleUDPClient



class webserver():
    def __init__(self, msg_queue):
        # super().__init__()
        self.msg_queue = msg_queue
        self.osc_client = SimpleUDPClient('127.0.0.1', 1337)  # Create client 
        
        

        
        
        @ui.page('/', dark=True)
        def page():
            ui.label('Hi!')
            
            with ui.row(): 
                ui.button('left', on_click=lambda: self.send_msg('left'))
                ui.button('right', on_click=lambda: self.send_msg('right'))  
                
                
    def send_msg(self,msg):
        self.osc_client.send_message("/webui", msg)   
        print(msg)            

  
  
     


# if __name__ == '__main__': 
# webserver()
# ui.run()




    
