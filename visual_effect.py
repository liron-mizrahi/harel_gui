import numpy as np 
import pygame
import random

# Function to generate spiral
def draw_spiral(screen, color, time, center=(400, 300)):
    t = np.linspace(0, 4 * np.pi, 100)
    x = center[0] + t * np.cos(t + time)
    y = center[1] + t * np.sin(t + time)
    points = np.array([x, y]).T.astype(int)
    pygame.draw.lines(screen, color, False, points, 2)
    
    
def draw_prism(screen, color, time, center=(400, 300)):
    num_polygons = 10
    for i in range(num_polygons):
        points = []
        sides = 6
        radius = (i + 1) * 20
        for j in range(sides):
            angle = (2 * np.pi / sides) * j + time
            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, color, points, 2)
        
def draw_smoke(screen, color,time, center=(400, 300)):
    for i in range(20):
        radius = 10 + i * 5
        alpha = max(0, 255 - i * 12)
        color = (128, 128, 128, alpha)
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (radius, radius), radius)
        screen.blit(s, (center[0] - radius, center[1] - radius))
        
def draw_wave(screen, color, time, center=(400, 300)):
    amplitude = 100
    frequency = 2
    for x in range(0, 800, 5):
        y = int(center[1] + amplitude * np.sin(2 * np.pi * frequency * (x / 800) + time))
        pygame.draw.circle(screen, color, (x, y), 5)
        
        
        
# Particle class
class SmokeParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 5)
        self.color = (255, 200, 200)  # Light gray color for smoke
        self.alpha = 255
        self.velocity = [random.uniform(-1, 1), random.uniform(-2, 1)]  # Moving upwards

    def move(self):

         # Brownian motion: small random changes in position
        self.velocity[0] += random.uniform(-0.1, 0.1)
        self.velocity[1] += random.uniform(-0.1, 0.1)
        
        self.x += self.velocity[0]
        self.y += self.velocity[1]      
        self.size -= random.uniform(-0.1, 0.1) #0.01
        self.alpha -= 0.5
        if self.size < 0:
            self.size = 0
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        smoke_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(smoke_surface, (*self.color, int(self.alpha)), (self.size, self.size), self.size)
        surface.blit(smoke_surface, (int(self.x - self.size), int(self.y - self.size)))

