
from pythonosc.osc_server import ThreadingOSCUDPServer
from pythonosc.dispatcher import Dispatcher



class osc_server: 
    def __init__(self, msg_queue, ip="127.0.0.1", port=1337): 
        self.ip = ip
        self.port = port
        self.msg_queue = msg_queue
        
    def set_dispatcher(self): 
    
        def filter_handler(self, address, *args):
            print(f"{address}: {args}")
            
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/webui", filter_handler)

    def run(self):
        self.set_dispatcher()
        self.server = ThreadingOSCUDPServer((self.ip, self.port), self.dispatcher)
        print("Serving on {}".format(self.server.server_address))
        self.server.serve_forever()


