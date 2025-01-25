import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Glowing Line with Gradient Effect')

# Function to interpolate between two colors
def interpolate_color(color1, color2, factor):
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

# Function to draw a line with a gradient glow effect
def draw_glowing_line(screen, start_pos, end_pos, line_color, glow_color1, glow_color2, thickness):
    for i in range(thickness, 0, -1):
        factor = i / thickness  # Factor for interpolation
        current_glow_color = interpolate_color(glow_color1, glow_color2, factor)
        
        # Calculate alpha (transparency)
        alpha = max(0, 255 - (thickness - i) * 10)
        
        # Create a surface for the glow with per-pixel alpha
        glow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        
        # Draw the glow line
        pygame.draw.line(glow_surface, (*current_glow_color, alpha), start_pos, end_pos, i)
        
        # Blit the glow surface onto the screen
        screen.blit(glow_surface, (0, 0))

    # Finally, draw the base line on top
    pygame.draw.line(screen, line_color, start_pos, end_pos, 2)

# Colors
line_color = (255, 255, 255)    # White line
glow_color1 = (255, 0, 0)       # Red start of gradient
glow_color2 = (0, 0, 255)       # Blue end of gradient

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((0, 0, 0))  # Black background

    # Draw the glowing line with gradient
    draw_glowing_line(screen, (100, 300), (700, 300), line_color, glow_color1, glow_color2, 20)

    # Update display
    pygame.display.flip()
