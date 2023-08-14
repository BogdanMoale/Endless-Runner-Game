import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Endless Runner Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
font = pygame.font.Font(None, 36)

# Player settings
player_width, player_height = 50, 50
player_x = width // 2 - player_width // 2
player_y = height - player_height
player_speed = 1

# Obstacle settings
obstacle_width, obstacle_height = 50, 50
obstacle_spawn_delay = 1000  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# List to hold obstacles
obstacles = []

# Game difficulty
obstacle_speed_increment = 0.001
initial_obstacle_speed = 0.5

# Scoring
score = 0

# Game over flag
game_over = False

# Maximum number of obstacles on the screen
max_obstacles = 21

# Main loop
clock = pygame.time.Clock()
running = True

def spawn_obstacle():
    x = random.randint(0, width - obstacle_width)
    y = -obstacle_height
    obstacles.append([x, y])

def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, red, (obs[0], obs[1], obstacle_width, obstacle_height))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed

        current_time = pygame.time.get_ticks()

        # Spawn obstacles
        if current_time - last_spawn_time > obstacle_spawn_delay and len(obstacles) < max_obstacles:
            spawn_obstacle()
            last_spawn_time = current_time

        # Update obstacle positions
        for obs in obstacles:
            obs[1] += initial_obstacle_speed

            # Remove obstacles that have gone off the screen
            if obs[1] > height:
                obstacles.remove(obs)

        # Check for collision
        for obs in obstacles:
            if (
                player_x < obs[0] + obstacle_width
                and player_x + player_width > obs[0]
                and player_y < obs[1] + obstacle_height
                and player_y + player_height > obs[1]
            ):
                game_over = True

        # Increase obstacle speed over time
        initial_obstacle_speed += obstacle_speed_increment

        # Update score
        score += 0.01

        # update player speed
        player_speed += 0.001


    # Clear the screen
    screen.fill(white)

    if game_over:
        # Draw game over screen
        text = font.render("Game Over", True, black)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        score_text = font.render(f"Score: {int(score)}", True, black)
        score_rect = score_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(score_text, score_rect)

        restart_text = font.render("Press 'R' to Restart", True, black)
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 100))
        screen.blit(restart_text, restart_rect)

        if keys[pygame.K_r]:
            # Restart the game
            obstacles.clear()
            initial_obstacle_speed = 1
            player_speed = 1
            score = 0
            game_over = False
    else:
        # Draw player
        pygame.draw.rect(screen, black, (player_x, player_y, player_width, player_height))

        # Draw obstacles
        draw_obstacles()

        # Draw score
        score_text = font.render(f"Score: {int(score)}", True, black)
        screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
