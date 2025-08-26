import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Paddle
paddle_width = 100
paddle_height = 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 30
paddle_speed = 6

# Ball
ball_radius = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = -4

# Bricks
brick_rows = 5
brick_cols = 8
brick_width = 60
brick_height = 20
brick_padding = 10
brick_offset_top = 50
brick_offset_left = 35

bricks = []
for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        rect = pygame.Rect(
            brick_offset_left + col * (brick_width + brick_padding),
            brick_offset_top + row * (brick_height + brick_padding),
            brick_width,
            brick_height
        )
        brick_row.append(rect)
    bricks.append(brick_row)

# Score and lives
score = 0
lives = 3

# Font
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Move ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Wall collision
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_dx = -ball_dx
    if ball_y <= ball_radius:
        ball_dy = -ball_dy

    # Paddle collision
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    if paddle_rect.collidepoint(ball_x, ball_y + ball_radius):
        ball_dy = -ball_dy

    # Brick collision
    for row in bricks:
        for brick in row:
            if brick.collidepoint(ball_x, ball_y):
                ball_dy = -ball_dy
                row.remove(brick)
                score += 1
                break

    # Ball falls below paddle
    if ball_y > HEIGHT:
        lives -= 1
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 4
        ball_dy = -4
        if lives == 0:
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Draw paddle
    pygame.draw.rect(screen, BLUE, paddle_rect)

    # Draw ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    # Draw bricks
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, GREEN, brick)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (5, 5))
    screen.blit(lives_text, (WIDTH - 110, 5))

    # Check win condition
    if all(len(row) == 0 for row in bricks):
        print("YOU WIN!")
        pygame.quit()
        sys.exit()

    pygame.display.flip()
    clock.tick(FPS)
