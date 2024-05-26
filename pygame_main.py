import pygame
import time

class visual_stim(): 
    def __init__(self): 
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        
    def run(self): 
        # Main Pygame loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                         running = False
                        
                    
                

            #     font = pygame.font.SysFont("Arial", 36)
            #     txtsurf = font.render(shared_data['score'], True, (255,255,255)))
            #     self.screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
   
            # Render here
            self.screen.fill((0, 0, 0))
            pygame.display.flip()

            time.sleep(0.01)
        
        pygame.quit()