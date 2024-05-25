# frontnd.py
from nicegui import Client, app, core, run, ui
from nicegui import events


with ui.row(): 
    ui.button('left', on_click=lambda: ui.notify('left'))
    ui.button('right', on_click=lambda: ui.notify('right'))
    
