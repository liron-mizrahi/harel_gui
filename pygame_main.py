import pygame
import time
from visual_effect import * 

class visual_stim(): 
    def __init__(self): 
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        
        self.effect_functions = [draw_spiral, draw_prism, draw_smoke, draw_wave]
        self.current_effect = 0
     
     
    
    
    
    
        
    def run(self): 
        # Main Pygame loop
        running = True
        msg = ''
        start_time = pygame.time.get_ticks()
        color = pygame.Color(255, 255, 255)
        # Create a list of smoke particles
        particles = []
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                         running = False
                    if event.key == pygame.K_SPACE:
                        self.current_effect = (self.current_effect + 1) % len(self.effect_functions)
                        color = pygame.Color(np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
            # read queue            
            # while not self.msg_queue.empty(): 
            #     msg = self.msg_queue.get()
                # print('pygame: '+ msg)
            
                
                
            current_time = pygame.time.get_ticks() - start_time
            # Render here
            self.screen.fill((0, 0, 0))
            
            
            

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
        
        pygame.quit()