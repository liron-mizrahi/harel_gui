import pygame
import numpy as np
import time

# Initialize Pygame mixer for stereo sound (2 channels)
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Audio-Driven Flicker")

# Parameters for the sine waves
sample_rate = 44100  # Samples per second
duration = 2.0       # Duration of the sound in seconds
frequency_left = 440.0  # Initial frequency for the left channel (A4 note)
frequency_right = 442.0  # Initial frequency for the right channel (C#5 note)
frequency_step = 10.0  # Frequency change step
amplitude = 0.5  # Initial amplitude
amplitude_step = 0.1  # Amplitude change step

# Colors
color = (255, 0, 0)  # Flicker color (red)
background_color = (0, 0, 0)  # Background color (black)

def generate_sound(frequency_left, frequency_right, amplitude):
    """Generate a stereo sine wave sound based on the given frequencies and amplitude."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_left = amplitude * np.sin(2 * np.pi * frequency_left * t)
    wave_right = amplitude * np.sin(2 * np.pi * frequency_right * t)
    stereo_wave = np.stack((wave_left, wave_right), axis=-1)
    sound_array = np.int16(stereo_wave * 32767)
    return pygame.sndarray.make_sound(sound_array)

def flicker_screen(flicker_frequency, slope_up, slope_down):
    """Flicker the screen based on the calculated frequency and custom slopes."""
    flicker_period = 1.0 / flicker_frequency
    on_time = flicker_period * slope_up
    off_time = flicker_period * slope_down
    
    # On phase
    screen.fill(color)
    pygame.display.flip()
    time.sleep(on_time)
    
    # Off phase
    screen.fill(background_color)
    pygame.display.flip()
    time.sleep(off_time)

# Generate the initial sound
sound = generate_sound(frequency_left, frequency_right, amplitude)
sound.play(loops=-1)  # Play sound continuously

# Main loop
try:
    while True:
        flicker_frequency = abs(frequency_right - frequency_left)
        slope_up = 1.  # Example slope for On-to-Off transition
        slope_down = 1.  # Example slope for Off-to-On transition
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise KeyboardInterrupt
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Decrease frequency
                    frequency_left = max(20, frequency_left - frequency_step)
                    frequency_right = max(20, frequency_right - frequency_step)
                    sound.stop()
                    sound = generate_sound(frequency_left, frequency_right, amplitude)
                    sound.play(loops=-1)
                elif event.key == pygame.K_RIGHT:
                    # Increase frequency
                    frequency_left += frequency_step
                    frequency_right += frequency_step
                    sound.stop()
                    sound = generate_sound(frequency_left, frequency_right, amplitude)
                    sound.play(loops=-1)
                elif event.key == pygame.K_UP:
                    # Increase amplitude
                    amplitude = min(1.0, amplitude + amplitude_step)
                    sound.stop()
                    sound = generate_sound(frequency_left, frequency_right, amplitude)
                    sound.play(loops=-1)
                elif event.key == pygame.K_DOWN:
                    # Decrease amplitude
                    amplitude = max(0.1, amplitude - amplitude_step)
                    sound.stop()
                    sound = generate_sound(frequency_left, frequency_right, amplitude)
                    sound.play(loops=-1)
        
        # Flicker the screen based on the calculated frequency difference
        if flicker_frequency > 0:
            flicker_screen(flicker_frequency, slope_up, slope_down)
        else:
            screen.fill(background_color)
            pygame.display.flip()

        # Prevent high CPU usage
        pygame.time.wait(10)

except KeyboardInterrupt:
    pass
finally:
    sound.stop()
    pygame.quit()
