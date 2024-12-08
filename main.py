import pygame
import math
import random
import pygame_gui

# Initialize Pygame and pygame_gui
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.1  # Gravity for pendulum motion
LENGTH = 250    # Length of the pendulum
MASS = 10       # Mass of the pendulum bob
CENTER = (WIDTH // 2, HEIGHT // 4)  # Center of pendulum pivot

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand Pendulum Art")
clock = pygame.time.Clock()

# Create GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Pendulum variables
angle = math.pi / 4  # Initial angle
angle_velocity = 0   # Initial angular velocity
angle_acceleration = 0
prev_x, prev_y = None, None  # Previous position for trail effect

# Sand particles
sand_particles = []

# Function to update pendulum physics
def update_pendulum():
    global angle, angle_velocity, angle_acceleration
    
    angle_acceleration = (-GRAVITY / LENGTH) * math.sin(angle)
    angle_velocity += angle_acceleration
    angle += angle_velocity

# Function to draw the pendulum and leave traces of its path
def draw_pendulum():
    x = int(CENTER[0] + LENGTH * math.sin(angle))  # Top-down view x-coordinate
    y = int(CENTER[1] + LENGTH * math.cos(angle))  # Top-down view y-coordinate

    # Draw the line (trace) from the previous point to the current point
    if prev_x is not None and prev_y is not None:
        pygame.draw.line(screen, (255, 255, 255), (prev_x, prev_y), (x, y), 1)

    return x, y

# Function to generate sand particles
def generate_sand(x, y, speed_factor):
    # Create a particle at the position of the pendulum bob
    sand_particles.append([x, y, random.uniform(-speed_factor, speed_factor), random.uniform(-speed_factor, speed_factor)])

# Function to draw sand particles
def draw_sand():
    global sand_particles
    for particle in sand_particles:
        particle[0] += particle[2]
        particle[1] += particle[3]
        pygame.draw.circle(screen, (255, 255, 255), (int(particle[0]), int(particle[1])), 2)
        # Remove particles that move off-screen
        if particle[0] < 0 or particle[0] > WIDTH or particle[1] < 0 or particle[1] > HEIGHT:
            sand_particles.remove(particle)

# Create the slider for controlling the speed of sand particles
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(0, HEIGHT - 50, WIDTH, 50),
    value_range=(1.0, 10.0),  # Range of values for the slider
    start_value=5.0,          # Initial value of the slider
    manager=manager
)



# Main game loop
running = True
while running:
    time_delta = clock.tick(FPS) / 1000.0
    screen.fill((0, 0, 0))  # Black background
    draw_sand()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Process GUI events
        manager.process_events(event)

    # Get the speed factor from the slider
    speed_factor = speed_slider.get_current_value()

    update_pendulum()

    # Get new position of pendulum and generate sand particles
    x, y = draw_pendulum()
    generate_sand(x, y, speed_factor)  # Generate sand at the pendulum's tip

    prev_x, prev_y = x, y  # Update the previous position for next trace

    # Update the GUI
    manager.update(time_delta)
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
