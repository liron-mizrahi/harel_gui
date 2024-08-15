import cv2
import datetime

class video(): 
    def __init__(self, msg_queue): 
        # OpenCV is used to access the webcam.
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4
        self.out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))  # Output file name, codec, frame rate, frame size
        self.msg_queue = msg_queue
        self.running = False
        
        
    def run(self): 
        # Check if the webcam is opened correctly
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return False

        while True:
            
            
            if self.running: 
                # Capture frame-by-frame
                ret, frame = self.cap.read()
                
                if not ret:
                    print("Error: Could not read frame.")
                    break
                
                
                # Get the current date and time
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Put the timestamp on the frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, timestamp, (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


                # Write the frame to the file
                self.out.write(frame)

                # Display the frame
                cv2.imshow('Webcam', frame)

                # Break the loop on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # Release everything when job is finished
        self.cap.release()
        self.out.release()
        self.cv2.destroyAllWindows()

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
