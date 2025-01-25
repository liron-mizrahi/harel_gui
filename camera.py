
import datetime

class video(): 
    from oscpy.server import OSCThreadServer
    import cv2
    def __init__(self, webcam_queue=None): 
        self.running = False
        self.webcam_queue = webcam_queue
        self.osc_int(port=9003)
        
    def osc_int(self, port=9999):
        self.osc = self.OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
                
            if values[0] == 'video_start':
                self.running=True  
                print(self.running)           
            if values[0] == 'video_stop':
                self.running=False  
                print(self.running)   
                
    def osc_send(self, port, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=port)
        
                
    def init_webcam(self): 
       # OpenCV is used to access the webcam.
        self.cap = self.cv2.VideoCapture(0)
        self.cap.set(self.cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(self.cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Define the codec and create a VideoWriter object
        fourcc = self.cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
        self.out = self.cv2.VideoWriter('output'+timestamp+'.mp4', fourcc, 20.0, (640, 480))  # Output file name, codec, frame rate, frame size
        
        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return False         

                            
    def run(self): 
        print('video_run')
        while True: 

            if self.running:
                if not hasattr(self,'cap'): 
                    self.init_webcam()
                    print('init webcam')
                elif not self.cap.isOpened():
                    self.init_webcam()
                    print('init webcam again')
            
                

                # Capture frame-by-frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Could not read frame.")
                    break
                
                # Get the current date and time
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Put the timestamp on the frame
                font = self.cv2.FONT_HERSHEY_SIMPLEX
                self.cv2.putText(frame, timestamp, (10, 50), font, 0.5, (255, 255, 255), 1, self.cv2.LINE_AA)
                # Write the frame to the file
                self.out.write(frame)
                # Display the frame
                # self.cv2.imshow('Webcam', frame)
                # Convert the frame from BGR to RGB
                frame_rgb = self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB)
                # send frmae via webcam_queue
                self.webcam_queue.put(frame_rgb)
                
                # Break the loop on 'q' key press
                if self.cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            # TODO  : 
            # if (not self.running) & (not self.cap.isOpened()): 
            #     # Release everything when job is finished
            #     try:
            #         self.cap.release()
            #         self.out.release()
            #     except: 
            #         pass
                    
        # self.cv2.destroyAllWindows()

    def close(self): 
        try: 
            self.cap.release()
            self.out.release()
            self.cv2.destroyAllWindows()
        except: 
            pass
        
        
if __name__ == '__main__': 
    vid=video()
    vid.run()
