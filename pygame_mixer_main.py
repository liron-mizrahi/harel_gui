import pygame
import time
from visual_effect import * 
from oscpy.server import OSCThreadServer

class visual_stim(): 
    def __init__(self, audio_file= None, pitches=None): 
        # Initialize Pygame
        pygame.init()
        if audio_file: 
            pygame.mixer.init()
            self.audio_samplerate = 44100
            self.sound = pygame.mixer.music.load(audio_file)
            self.audio_pitches =np.load('Bilateral Music Therapy_pitches.npy')
        
        self.screen = pygame.display.set_mode((640, 480))#, pygame.FULLSCREEN)
        
        self.effect_functions = [draw_spiral, draw_prism, draw_smoke, draw_wave]
        self.current_effect = 0
        self.osc_int(port=9002)
        self.window_hide = False
     
    def osc_int(self, port=9999):
        self.osc = OSCThreadServer(encoding='utf8') 
        self.osc.listen(address='0.0.0.0', port=port, default=True)
        
        @self.osc.address(b'/cmd')
        def callback(*values):
            print("got values: {}".format(values))
            
            if values[0] == 'effect':
                print('set effect : '+ str(values[1]))
                self.current_effect = values[1]
                            
            if values[0] == 'screen':
                if values[1] == 0: 
                    # self.screen = pygame.display.set_mode((1,1)) 
                    self.running=False
                if values[1] == 1: 
                    # self.screen = pygame.display.set_mode((640, 480))    
                    self.running=True             
            
    def osc_send(self, data:list=[]): 
        self.osc.send_message(b'/cmd', data,ip_address='0.0.0.0', port=9000)
     
    
    
        
    def run(self): 
        # Main Pygame loop
        self.running = True
        msg = ''
        start_time = pygame.time.get_ticks()
        color = pygame.Color(255, 255, 255)
        clock = pygame.time.Clock()
        # Create a list of smoke particles
        particles = []
        
        pygame.mixer.music.play()
        while self.running:
            # keyboad control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                         self.running = False
                    if event.key == pygame.K_SPACE:
                        self.current_effect = (self.current_effect + 1) % len(self.effect_functions)
                        color = pygame.Color(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))

            
                
                
            current_time = pygame.time.get_ticks() - start_time
            # Render here
            self.screen.fill((0, 0, 0))
              # Get the current position of the audio
            self.audio_pos = pygame.mixer.music.get_pos()

            # Convert audio position to seconds (optional)
            self.audio_pos_sec = self.audio_pos / 1000.0
            
            pitches_index = int(self.audio_pos * self.audio_samplerate / 1000 / 512)
            pitch_list = self.audio_pitches[pitches_index]
            
            for pitch in pitch_list: 
                if pitch[1]>0:
                    radius = int(100 + pitch[1] / 100)
                    color = pygame.Color(255, 255, 255)
                    pygame.draw.circle( self.screen, color, (400, 300), radius, 1) #int(1*pitch[0]))
                    
            
            # visual effects
            if self.effect_functions[self.current_effect] == draw_smoke: 
                # Create new smoke particles
                if len(particles) < 5000:
                    particles.append(SmokeParticle(400, 300))

                # Move and draw particles
                for particle in particles:
                    particle.move()
                    particle.draw(self.screen)

                # Remove particles that are too small or fully transparent
                particles = [p for p in particles if p.size > 0 and p.alpha > 0]
            else: 
                self.effect_functions[self.current_effect](self.screen, color, current_time / 1000.0)
    
    
            font = pygame.font.SysFont("Arial", 36)
            txtsurf = font.render('msg_example', True, (0,255,255))
            self.screen.blit(txtsurf,(200,200))
   
            
            
            pygame.display.flip()

            time.sleep(0.01)
            # clock.tick(60)
        
        pygame.quit()