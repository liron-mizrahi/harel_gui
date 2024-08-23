# frontnd.py
from nicegui import Client, app, core, run, ui
from nicegui import events
# from osc import osc
from oscpy.server import OSCThreadServer




    

class webserver():
    
    def menu(self): 
        with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
            ui.label('Audio Visual Stimulation Panel')
            ui.button(on_click=lambda: right_drawer.toggle(), icon='menu').props('flat color=white')
        with ui.right_drawer(fixed=False, ).style('background-color: black;').props('width=120 bordered') as right_drawer:
            # ui.label('RIGHT DRAWER')  
            ui.button('Home', on_click=lambda: ui.open('/'))
            ui.button('Movies', on_click=lambda: ui.open('/movies'))
            ui.button('AVS', on_click=lambda: ui.open('/avs'))
            ui.button('AVS2', on_click=lambda: ui.open('/avs2'))
            ui.separator()
            ui.button('Camera', on_click=lambda: ui.open('/camera'))
            ui.button('Music', on_click=lambda: ui.open('/music'))
            switch = ui.switch('Camera', on_change=lambda x: self.osc_send(9003,['video_start']) if x.value == 1 else self.osc_send(9003,['video_stop']))
            ui.separator()
            ui.button('Quit', on_click=lambda _: self.osc_send(9000,['quit_app']))
            
            
    def __init__(self):
        # start manager osc server  
        self.osc_int(port=9001)
          
          
    
        @ui.page('/', dark=True)
        def main_page():
            self.menu()
            
        @ui.page('/movies', dark=True)
        def movies_page():
            self.menu()    
            
            for q in range(10): 
                src = 'https://picsum.photos/id/565/640/360'
                ui.interactive_image(src, on_mouse=lambda _: ui.notify('img clicked'), events=['mousedown'],cross=False).classes('w-128')

                
        @ui.page('/avs', dark=True)
        def avs_page():
            self.menu()
            
            effects_dict = {0: 'spiral', 1: 'prism', 2: 'smoke', 3: 'wave'}
            with ui.row():
                ui.select({0: 'spiral', 1: 'prism', 2: 'smoke', 3: 'wave'}, value=0,
                          on_change=lambda x: self.osc_send(9002,['effect', x.value])).classes('w-64').style('font-size: 20px;')
                
                ui.select({0: 'music 1', 1: 'music 2', 2: 'music 3', 3: 'music 4'}, value=0,
                          on_change=lambda x: self.osc_send(9002,['music', x.value])).classes('w-64').style('font-size: 20px;')
 
 
            with ui.row():
                ui.button('Start',  on_click=lambda: self.osc_send(9000, ['screen_start']) )  
                ui.button('Stop',  on_click=lambda: self.osc_send(9002, ['screen_stop']) )  
                
            with ui.row(): 
                ui.joystick(color='blue', size=50,
                    on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),
                    on_end=lambda _: coordinates.set_text('0, 0'))
 
                ui.joystick(color='red', size=50)
            with ui.row(): 
                coordinates = ui.label('0, 0',)
                coordinates2 = ui.label('0, 0')
            
            
            
        @ui.page('/camera', dark=True)
        def camera_page():
            self.menu()     
             
        @ui.page('/music', dark=True)
        def music_page():
            self.menu()              
 
        @ui.page('/avs2', dark=True) 
        def moveis_page(): 
            self.menu()   
            with ui.row(): 
                with ui.column(): 
                    left_slider = ui.slider(min=20, max=2000, value=500, 
                                            on_change=lambda x: self.osc_send(9004, ['frequency_left', x.value])).classes('w-64')
                    ui.label().bind_text_from(left_slider, 'value')
                with ui.column(): 
                    right_slider = ui.slider(min=20, max=2000, value=505, 
                                             on_change=lambda x: self.osc_send(9004, ['frequency_right', x.value])).classes('w-64')
                    ui.label().bind_text_from(right_slider, 'value')                                              
            with ui.row():
                ui.button('Start', on_click=lambda _: self.osc_send(9000, ['avs2_start']) )  
                ui.button('Stop',  on_click=lambda _: self.osc_send(9004, ['avs2_stop']) )    
            ui.knob(1.0, min = 0.0, max = 50.,  show_value=True,  on_change=lambda x: self.osc_send(9004, ['amplitude', x.value]) )         
            ui.switch('Flicker', value=True, on_change=lambda x: self.osc_send(9004,['flicker', x.value]))        

        @ui.page('/avs_', dark=True) 
        def moveis_page(): 
            self.menu()   
            
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
                with ui.row(): 
                    ui.joystick(color='blue', size=50)
                        # on_move=lambda e: coordinates.set_text(f'{e.x:.3f}, {e.y:.3f}'),
                        # on_end=lambda _: coordinates.set_text('0, 0'))
                    
                    
                    ui.joystick(color='red', size=50)
                    # coordinates = ui.label('0, 0',)
                    # coordinates2 = ui.label('0, 0', visible=False)
                    

                                
    def osc_int(self, port=9999):
        self.osc = OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
    def osc_send(self, port, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=port)


  

# if __name__ == '__main__': 
#     webserver()
#     ui.run(dark=True,fullscreen=False)




    
