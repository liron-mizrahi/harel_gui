# frontnd.py
from nicegui import Client, app, core, run, ui
from nicegui import events
from osc_server import osc



class webserver():
    def __init__(self):
        # super().__init__()

        @ui.page('/', dark=True)
        def main_page():
            with ui.column(): 
                ui.button('Visual Stimulation', )
                
                with ui.row(): 
                    ui.button('left')
                    ui.button('right')  

                
                
        # @ui.page('/visual', dark=True, )
        # def visual_page(): 
        #     ui.link('main',main_page)
                
            
            
                

# if __name__ == '__main__': 
#     webserver()
#     ui.run(dark=True,fullscreen=False)




    
