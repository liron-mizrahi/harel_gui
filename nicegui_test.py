from nicegui import ui
from frontend import webserver

web = webserver()
ui.run(reload=True,  host='127.0.0.1', port=8000, show=False)
