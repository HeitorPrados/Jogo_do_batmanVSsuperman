import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Fighting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Frame rate
clock = pygame.time.Clock()
FPS = 60

# Load images
background_image = pygame.image.load("images/background.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player1_image = pygame.image.load("images/player1.png").convert_alpha()
player2_image = pygame.image.load("images/player2.png").convert_alpha()

# Resize images to match the height of the stick figures (100 pixels)
player1_image = pygame.transform.scale(player1_image, (int(435 * (100 / 526)), 100))
player2_image = pygame.transform.scale(player2_image, (int(531 * (100 / 650)), 100))

# Character properties
CHAR_WIDTH1, CHAR_HEIGHT1 = player1_image.get_width(), player1_image.get_height()
CHAR_WIDTH2, CHAR_HEIGHT2 = player2_image.get_width(), player2_image.get_height()
char1_pos = [100, HEIGHT - CHAR_HEIGHT1 - 10]
char2_pos = [WIDTH - 150, HEIGHT - CHAR_HEIGHT2 - 10]
char1_vel = [0, 0]
char2_vel = [0, 0]
SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = 10
HEALTH = 100

# Health
char1_health = HEALTH
char2_health = HEALTH

# Victory counters
char1_victories = 0
char2_victories = 0

# Attack properties
ATTACK_WIDTH, ATTACK_HEIGHT = 10, 10
ATTACK_SPEED = 10
char1_attacking = False
char2_attacking = False
char1_attack_rect = pygame.Rect(0, 0, ATTACK_WIDTH, ATTACK_HEIGHT)
char2_attack_rect = pygame.Rect(0, 0, ATTACK_WIDTH, ATTACK_HEIGHT)

# Fonts
font = pygame.font.SysFont(None, 48)

# Game state
game_over = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def reset_game():
    global char1_pos, char2_pos, char1_vel, char2_vel, char1_health, char2_health, char1_attacking, char2_attacking, game_over
    char1_pos = [100, HEIGHT - CHAR_HEIGHT1 - 10]
    char2_pos = [WIDTH - 150, HEIGHT - CHAR_HEIGHT2 - 10]
    char1_vel = [0, 0]
    char2_vel = [0, 0]
    char1_health = HEALTH
    char2_health = HEALTH
    char1_attacking = False
    char2_attacking = False
    game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                reset_game()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    if not game_over:
        # Character 1 controls (WASD)
        if keys[pygame.K_a]:
            char1_vel[0] = -SPEED
        elif keys[pygame.K_d]:
            char1_vel[0] = SPEED
        else:
            char1_vel[0] = 0

        if keys[pygame.K_w] and char1_pos[1] == HEIGHT - CHAR_HEIGHT1 - 10:
            char1_vel[1] = -JUMP_STRENGTH

        if keys[pygame.K_v] and not char1_attacking:
            char1_attacking = True
            char1_attack_rect.x = char1_pos[0] + CHAR_WIDTH1
            char1_attack_rect.y = char1_pos[1] + CHAR_HEIGHT1 // 2 - ATTACK_HEIGHT // 2

        # Character 2 controls (Arrow keys)
        if keys[pygame.K_LEFT]:
            char2_vel[0] = -SPEED
        elif keys[pygame.K_RIGHT]:
            char2_vel[0] = SPEED
        else:
            char2_vel[0] = 0

        if keys[pygame.K_UP] and char2_pos[1] == HEIGHT - CHAR_HEIGHT2 - 10:
            char2_vel[1] = -JUMP_STRENGTH

        if keys[pygame.K_m] and not char2_attacking:
            char2_attacking = True
            char2_attack_rect.x = char2_pos[0] - ATTACK_WIDTH
            char2_attack_rect.y = char2_pos[1] + CHAR_HEIGHT2 // 2 - ATTACK_HEIGHT // 2

        # Apply gravity
        char1_vel[1] += GRAVITY
        char2_vel[1] += GRAVITY

        # Update character positions
        char1_pos[0] += char1_vel[0]
        char1_pos[1] += char1_vel[1]
        char2_pos[0] += char2_vel[0]
        char2_pos[1] += char2_vel[1]

        # Prevent characters from falling through the floor
        if char1_pos[1] >= HEIGHT - CHAR_HEIGHT1 - 10:
            char1_pos[1] = HEIGHT - CHAR_HEIGHT1 - 10
            char1_vel[1] = 0

        if char2_pos[1] >= HEIGHT - CHAR_HEIGHT2 - 10:
            char2_pos[1] = HEIGHT - CHAR_HEIGHT2 - 10
            char2_vel[1] = 0

        # Handle attacks
        if char1_attacking:
            char1_attack_rect.x += ATTACK_SPEED
            if char1_attack_rect.colliderect(pygame.Rect(*char2_pos, CHAR_WIDTH2, CHAR_HEIGHT2)):
                char2_health -= 10
                char1_attacking = False
            if char1_attack_rect.x > WIDTH:
                char1_attacking = False

        if char2_attacking:
            char2_attack_rect.x -= ATTACK_SPEED
            if char2_attack_rect.colliderect(pygame.Rect(*char1_pos, CHAR_WIDTH1, CHAR_HEIGHT1)):
                char1_health -= 10
                char2_attacking = False
            if char2_attack_rect.x < 0:
                char2_attacking = False

        # Check for game over
        if char1_health <= 0 or char2_health <= 0:
            game_over = True
            if char1_health <= 0:
                char2_victories += 1
            if char2_health <= 0:
                char1_victories += 1

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw floor
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 10, WIDTH, 10))

    # Draw characters
    screen.blit(player1_image, char1_pos)
    screen.blit(player2_image, char2_pos)

    # Draw attacks
    if char1_attacking:
        pygame.draw.rect(screen, RED, char1_attack_rect)
    if char2_attacking:
        pygame.draw.rect(screen, RED, char2_attack_rect)

    # Draw health bars
    pygame.draw.rect(screen, GREEN, (50, 50, char1_health, 10))
    pygame.draw.rect(screen, GREEN, (WIDTH - 150, 50, char2_health, 10))

    # Draw victory counters
    draw_text(f"Player 1 Victories: {char1_victories}", font, WHITE, screen, 200, 20)
    draw_text(f"Player 2 Victories: {char2_victories}", font, WHITE, screen, WIDTH - 200, 20)

    # Draw game over screen
    if game_over:
        draw_text("Game Over!", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Press R to Restart", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
