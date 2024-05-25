import threading
import time
from nicegui import ui
import pygame

import frontend

def run_nicegui():
    ui.run(reload=False,  host="127.0.0.1", port=8000)

# Start FastAPI in a separate thread
fastapi_thread = threading.Thread(target=run_nicegui, daemon=True)
fastapi_thread.start()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Main Pygame loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render here
    screen.fill((0, 0, 0))
    pygame.display.flip()

    time.sleep(0.01)

pygame.quit()