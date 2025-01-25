import pygame
import librosa
import pickle
import numpy as np

audio_file = "Bilateral Music Therapy.mp3"

pitches=np.load('Bilateral Music Therapy_pitches.npy')
sr = 44100 # sample rate
# Initialize Pygame and the mixer module
pygame.init()
pygame.mixer.init()

# Load a sound file

sound = pygame.mixer.music.load(audio_file)

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Play the sound
# sound.play()
pygame.mixer.music.play()

# Start the game loop
running = True
start_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # if event.type == pygame.KEYDOWN: 
        #     if event.key == pygame.K_RIGHT: 
        #         pygame.mixer.music.set_pos(audio_pos //10 + 20)

    # Get the current position of the audio
    audio_pos = pygame.mixer.music.get_pos()

    # Convert audio position to seconds (optional)
    audio_pos_sec = audio_pos / 1000.0
    
    # # Example: Change color or move objects based on time
    color = (int(audio_pos_sec * 50) % 256, 100, 150)
    screen.fill(color)
    # screen.fill((0, 0, 0))
    
    pitches_index = int(audio_pos * sr / 1000 / 512)

    pitch_list = pitches[pitches_index]
    
    for pitch in pitch_list: 
        if pitch[1]>0:
            radius = int(100 + pitch[1] / 100)
            color = pygame.Color(255, 255, 255)
            pygame.draw.circle( screen, color, (400, 300), radius, 1) #int(1*pitch[0]))
            

    # Sync visuals based on the audio position
    current_time = pygame.time.get_ticks() - start_time
    
    


    font = pygame.font.SysFont("Arial", 16)
    txtsurf = font.render(f'{audio_pos}  {current_time}  {audio_pos-current_time}', True, (0,255,255))
    screen.blit(txtsurf,(50,50))
    txtsurf2 = font.render(f'{pitches_index} ', True, (0,255,255))
    screen.blit(txtsurf2,(50,80))
                       
    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(10)

pygame.quit()

