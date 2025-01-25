

class visual_stim(): 
    import pygame
    import time
    import visual_effect 
    from oscpy.server import OSCThreadServer
    import numpy as np 
    def __init__(self, audio_file= None, pitches=None, webcam_queue=None): 
        # Initialize Pygame
        self.pygame.init()
        self.audio_file = audio_file
        if audio_file: 
            self.pygame.mixer.init()
            self.audio_samplerate = 44100
            self.sound = self.pygame.mixer.music.load(audio_file)
            self.audio_pitches =self.np.load('Bilateral Music Therapy_pitches.npy')
        
        self.screen = self.pygame.display.set_mode((640, 480))#, pygame.FULLSCREEN)
        
        self.effect_functions = [self.visual_effect.draw_spiral, 
                                 self.visual_effect.draw_prism, 
                                 self.visual_effect.draw_smoke, 
                                 self.visual_effect.draw_wave]
        self.current_effect = 0
        self.osc_int(port=9002)
        self.window_hide = False
        self.webcam_queue=webcam_queue
        
    def osc_int(self, port=9999):
        self.osc = self.OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
            
            if values[0] == 'effect':
                print('set effect : '+ str(values[1]))
                self.current_effect = values[1]
                
            if values[0] == 'screen_stop':
                self.running=False  
                print('get : screen_stop')
                print(self.running)  
                 
        @self.osc.address(b'/webcam')
        def callback(*values):
            print(values[:5])
            
    def osc_send(self, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=9000)
     
    
    
        
    def run(self): 
        # Main Pygame loop
        self.running = True
        start_time = self.pygame.time.get_ticks()
        color = self.pygame.Color(255, 255, 255)
        clock = self.pygame.time.Clock()
        # Create a list of smoke particles
        particles = []
        if self.audio_file: 
            self.pygame.mixer.music.play()
            
        while self.running:
            # keyboad control
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.running = False
                    
                if event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_q:
                         self.running = False
                    if event.key == self.pygame.K_SPACE:
                        self.current_effect = (self.current_effect + 1) % len(self.effect_functions)
                        color = self.pygame.Color(self.np.random.randint(0, 255), self.np.random.randint(0, 255), np.random.randint(0, 255))

            
                
                
            current_time = self.pygame.time.get_ticks() - start_time
            # Render here
            self.screen.fill((0, 0, 0))
            if self.audio_file:
                # Get the current position of the audio
                self.audio_pos = self.pygame.mixer.music.get_pos()

                # Convert audio position to seconds (optional)
                self.audio_pos_sec = self.audio_pos / 1000.0
            
                pitches_index = int(self.audio_pos * self.audio_samplerate / 1000 / 512)
                pitch_list = self.audio_pitches[pitches_index]
            
                for pitch in pitch_list: 
                    if pitch[1]>0:
                        radius = int(100 + pitch[1] / 100)
                        color = self.pygame.Color(255, 255, 255)
                        self.pygame.draw.circle( self.screen, color, (400, 300), radius, 1) #int(1*pitch[0]))
                        
            
            # visual effects
            if self.effect_functions[self.current_effect] == self.visual_effect.draw_smoke: 
                # Create new smoke particles
                if len(particles) < 5000:
                    particles.append(self.visual_effect.SmokeParticle(400, 300))

                # Move and draw particles
                for particle in particles:
                    particle.move()
                    particle.draw(self.screen)

                # Remove particles that are too small or fully transparent
                particles = [p for p in particles if p.size > 0 and p.alpha > 0]
            else: 
                self.effect_functions[self.current_effect](self.screen, color, current_time / 1000.0)
    
    
            font = self.pygame.font.SysFont("Arial", 36)
            txtsurf = font.render('msg_example', True, (0,255,255))
            self.screen.blit(txtsurf,(200,200))
   
            
            
            
            if not self.webcam_queue.empty():
                frame_rgb = self.webcam_queue.get()
                frame_surface = self.pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
                self.screen.blit(frame_surface, (0, 0))
            
            
            self.pygame.display.flip()

            self.time.sleep(0.01)
            # clock.tick(60)
        
        self.pygame.quit()
        self.osc.stop_all()
        self.osc.terminate_server()