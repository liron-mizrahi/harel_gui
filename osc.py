
import time


class osc(): 
    from oscpy.server import OSCThreadServer
    from oscpy.client import OSCClient

    def __init__(self, address='0.0.0.0', port=8000, label=''): 
        self.address = address
        self.port= port
        self.clients = []
        self.label = label
        self.start_server()
    
    def start_server(self): 
        self.osc_server = self.OSCThreadServer(encoding='utf8') 
        sock = self.osc_server.listen(address=self.address, port=self.port, default=True)
        
        
        @self.osc_server.address(b'/add_client') 
        def add_client(*values): 
            print("got new client: {}".format(values))
            self.clients.append({'label': values[0], 'port': values[1]})

        @self.osc_server.address(b'/remove_client')
        def remove_client(*values): 
            # print("got  client to remove: {}".format(values))
            self.clients.remove({'label': values[0], 'port': values[1]})

            
            
        @self.osc_server.address(b'/msg')
        def callback(*values):
            print("got values: {}".format(values))
            
        @self.osc_server.address(b'/test')
        def callback(*values):
            for v in values:
                print(v, type(v)) 
                         


    def register_clients_list(self): 
        return self.clients
    
    def register_server(self, target_port:int, label:str=''): 
        if label=='': 
            label = self.label
        self.osc_server.send_message(b'/add_client', [label, self.port],ip_address='0.0.0.0', port=target_port)
        
    def unregister_server(self, target_port:int, label:str=''): 
        if label=='': 
            label = self.label
        self.osc_server.send_message(b'/remove_client', [label, self.port],ip_address='0.0.0.0', port=target_port)       
    
    def send(self, prefix, target_port:int, data:list):
         self.osc_server.send_message(prefix, data,ip_address='0.0.0.0', port=target_port)  
         
    
    def stop_server(self): 
        self.osc_server.stop()
            
    def wait(self):
        time.sleep(10)
        self.stop_server()

        

        
if __name__ == "__main__":
    
    server1 = osc(port=8001, label='srv1')  # init server on port 8001
    server2 = osc(port=8002) 
    
    # init list of servers as listener
    listener_server_list=[]
    for q in range(9000, 9010): 
        listener_server_list.append(osc(port=q, label='srv_'+str(q)) )
        
    for srv in listener_server_list: 
        # print(srv.osc_server.getaddress()[1])
        srv.register_server( target_port=server1.osc_server.getaddress()[1])
        
        
    # server2.osc_server.send_message(b'/add_client', [8002, 8003, 8003],*server1.osc_server.getaddress())
    #server2.osc_server.send_message(b'/add_client', [8002, 8003, 8003],ip_address='0.0.0.0', port=8001)
    # server2.osc_server.send_message(msg, from_addr=None, to_addrs=None, mail_options=[], rcpt_options=[])
    
    # server2.osc_server.send_message(b'/test', [8002, 8003, 'abc'],ip_address='0.0.0.0', port=8001)
    
    # server1.unregister_server( target_port=8002)
    # server2.register_server(target_port=8001)
    


    time.sleep(1)
    # print(server2.register_clients_list())
    print(server1.register_clients_list())
    
    # time.sleep(1)
    # server1.stop_server()
    # server2.stop_server()
    

    
    
    
    
    
        




