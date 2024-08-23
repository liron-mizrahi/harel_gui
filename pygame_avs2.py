class avs2(): 
    import pygame
    import time
    from oscpy.server import OSCThreadServer
    import numpy as np 
    
    def __init__(self): 
        self.pygame.init()
        self.pygame.mixer.pre_init(44100, -16, 2, 512)
        
        self.osc_int(port=9004)
        self.screen_width = 640
        self.screen_height = 480
        self.screen = self.pygame.display.set_mode((self.screen_width, self.screen_height))
        # self.pygame.display.set_caption("Audio-Driven Flicker")  
        
        # Parameters for the sine waves
        self.sample_rate = 44100  # Samples per second
        self.duration = 2.0       # Duration of the sound in seconds
        self.frequency_left = 440.0  # Initial frequency for the left channel (A4 note)
        self.frequency_right = 450.0  # Initial frequency for the right channel (C#5 note)
        self.amplitude = 0.5  # Initial amplitude
        self.amplitude_step = 0.1  # Amplitude change step

        # Colors
        self.color = (255, 0, 0)  # Flicker color (red)
        self.background_color = (0, 0, 0)  # Background color (black)
        


    def generate_sound(self,frequency_left, frequency_right, amplitude):
        """Generate a stereo sine wave sound based on the given frequencies and amplitude."""
        t = self.np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        wave_left = self.amplitude * self.np.sin(2 * self.np.pi * self.frequency_left * t)
        wave_right = self.amplitude * self.np.sin(2 * self.np.pi * self.frequency_right * t)
        stereo_wave = self.np.stack((wave_left, wave_right), axis=-1)
        sound_array = self.np.int16(stereo_wave * 32767)
        return self.pygame.sndarray.make_sound(sound_array)

    def flicker_screen(self,flicker_frequency, slope_up, slope_down):
        """Flicker the screen based on the calculated frequency and custom slopes."""
        self.flicker_period = 1.0 / flicker_frequency
        self.on_time = self.flicker_period * slope_up
        self.off_time = self.flicker_period * slope_down
        current_time = self.pygame.time.get_ticks() - self.start_time
        
        # On phase
        self.screen.fill(self.color)
        self.pygame.display.flip()
        self.time.sleep(self.on_time)
        
        # Off phase
        self.screen.fill(self.background_color)
        self.pygame.display.flip()
        self.time.sleep(self.off_time)
    
        
    def osc_int(self, port=9999):
        self.osc = self.OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
            
            if values[0] == 'frequency_left':
                if values[1] > 20: 
                    self.frequency_left = values[1]
                    self.update_config=True
            if values[0] == 'frequency_right':
                if values[1] > 20: 
                    self.frequency_right = values[1] 
                    self.update_config=True 
            if values[0] == 'amplitude': 
                if (values[1] > 0) & (values[1] < 50 ): 
                    self.amplitude = values[1]   
                    self.update_config=True   
            if values[0] == 'flicker': 
                if values[1]==0: 
                    self.flicker_runnung =False
                else: 
                    self.flicker_runnung =True
                    
            if values[0] == 'avs2_stop':
                self.running=False  
                print('get : avs2_stop')


            
    def osc_send(self, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=9000)
       
    def run(self): 
        self.running = True
        self.update_config = False
        self.flicker_runnung = True
        
        self.start_time = self.pygame.time.get_ticks()
        print(('start avs2', self.running))
        clock = self.pygame.time.Clock()
        # Generate the initial sound
        self.sound = self.generate_sound(self.frequency_left, 
                                        self.frequency_right, 
                                        self.amplitude)
        self.sound.play(loops=-1)  # Play sound continuously
        while self.running:
            current_time = self.pygame.time.get_ticks()
            flicker_frequency = abs(self.frequency_right - self.frequency_left)
            slope_up = 0.5  # Example slope for On-to-Off transition
            slope_down = 0.5  # Example slope for Off-to-On transition
            
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.running = False
                    
            if self.update_config: 
                self.sound.stop()
                self.sound = self.generate_sound(self.frequency_left, 
                                            self.frequency_right, 
                                            self.amplitude)
                self.sound.play(loops=-1)
                self.update_config = False
                
        
        
            # print(current_time)
            # Flicker the screen based on the calculated frequency difference
            if self.flicker_runnung & (flicker_frequency > 0):
                self.flicker_screen(flicker_frequency, slope_up, slope_down)
            else:
                self.screen.fill(self.background_color)
                self.pygame.display.flip()

            self.screen.fill(self.background_color)
            self.pygame.display.flip()   
            self.pygame.time.wait(10)
            
        self.pygame.quit()
        self.osc.stop_all()
        self.osc.terminate_server()
        print('pygame close')
        
        
        
if __name__ == '__main__': 
    flicker = avs2()
    flicker.run()