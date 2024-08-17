# frontnd.py
from nicegui import Client, app, core, run, ui
from nicegui import events
# from osc import osc
from oscpy.server import OSCThreadServer




    

class webserver():
    def __init__(self):
        # super().__init__()
        # start manager osc server  
        self.osc_int(port=9001)
          

    
        @ui.page('/', dark=True)
        def main_page():
            with ui.column(): 
                ui.button('Visual Stimulation', on_click=lambda: self.osc_send(9002, [1, 2, 3, 4]) )
                ui.select({0: 'spiral', 1: 'prism', 2: 'smoke', 3: 'wave'}, value=0,
                          on_change=lambda x: self.osc_send(9002,['effect', x.value]))
                
                with ui.row(): 
                    ui.button('left')
                    ui.button('right')  
                with ui.row():     
                    ui.button('show',  on_click=lambda: self.osc_send(9002, ['screen', 1]) )  
                    ui.button('hide',  on_click=lambda: self.osc_send(9002, ['screen', 0]) )
                    
                knob = ui.knob(0.3, show_value=True)
                switch = ui.switch('switch me')
                ui.label('Switch!').bind_visibility_from(switch, 'value')
                
                slider = ui.slider(min=0, max=100, value=50)
                ui.label().bind_text_from(slider, 'value')


                    
    def osc_int(self, port=9999):
        self.osc = OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
    def osc_send(self, port, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=port)

                
                
        # @ui.page('/visual', dark=True, )
        # def visual_page(): 
        #     ui.link('main',main_page)
                
            
            
                

# if __name__ == '__main__': 
#     webserver()
#     ui.run(dark=True,fullscreen=False)




    
