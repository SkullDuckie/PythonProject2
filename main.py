import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Flippy Blick")

# Colors
WHITE = (255, 255, 255)

# Load images
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bird_img = pygame.image.load("flappy.png")
bird_size = 30
bird_img = pygame.transform.scale(bird_img, (bird_size, bird_size))

# Load sounds
pygame.mixer.init()
pygame.mixer.music.load("flippyblox.mp3")  # Background music
pygame.mixer.music.play(-1)  # Loop the music
jump_sound = pygame.mixer.Sound("boing.mp3")
death_sound = pygame.mixer.Sound("byebye.mp3")

# Font
font = pygame.font.SysFont(None, 40)

# Game settings based on levels
levels = {
    "Easy": {"gravity": 0.3, "pipe_speed": 3},
    "Medium": {"gravity": 0.5, "pipe_speed": 4},
    "Hard": {"gravity": 0.7, "pipe_speed": 5},
}

# Load high score
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0


def select_level():
    screen.fill((50, 150, 250))
    text = font.render("Select Level: 1-Easy  2-Medium  3-Hard", True, WHITE)
    screen.blit(text, (40, HEIGHT // 2))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                if event.key == pygame.K_2:
                    return "Medium"
                if event.key == pygame.K_3:
                    return "Hard"


def game_over_screen(score):
    global high_score
    death_sound.play()  # Play death sound
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

    screen.fill((0, 0, 0))
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    retry_text = font.render("Press R to Retry or Q to Quit", True, WHITE)
    screen.blit(text, (WIDTH // 4, HEIGHT // 3))
    screen.blit(high_score_text, (WIDTH // 4, HEIGHT // 2))
    screen.blit(retry_text, (WIDTH // 6, HEIGHT // 1.5))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False


def main():
    while True:
        level = select_level()
        if not level:
            return

        GRAVITY = levels[level]["gravity"]
        PIPE_SPEED = levels[level]["pipe_speed"]
        JUMP_STRENGTH = -5
        PIPE_GAP = 165
        PIPE_WIDTH = 60

        player_x = 50
        player_y = HEIGHT // 6
        player_velocity = 0
        pipes = []
        score = 0

        clock = pygame.time.Clock()
        running = True

        def create_pipe():
            height = random.randint(100, 400)
            pipes.append({"x": WIDTH, "top": height, "bottom": height + PIPE_GAP})

        def draw_pipes():
            for pipe in pipes:
                pygame.draw.rect(screen, (0, 200, 0), (pipe["x"], 0, PIPE_WIDTH, pipe["top"]))
                pygame.draw.rect(screen, (0, 200, 0), (pipe["x"], pipe["bottom"], PIPE_WIDTH, HEIGHT - pipe["bottom"]))

        def check_collision():
            for pipe in pipes:
                if player_x + bird_size > pipe["x"] and player_x < pipe["x"] + PIPE_WIDTH:
                    if player_y < pipe["top"] or player_y + bird_size > pipe["bottom"]:
                        return True
            if player_y > HEIGHT - bird_size or player_y < 0:
                return True
            return False

        while running:
            screen.blit(background_img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_velocity = JUMP_STRENGTH
                    jump_sound.play()  # Play jump sound

            player_velocity += GRAVITY
            player_y += player_velocity

            if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
                create_pipe()

            for pipe in pipes:
                pipe["x"] -= PIPE_SPEED

            pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]

            screen.blit(bird_img, (player_x, player_y))
            draw_pipes()

            if check_collision():
                if not game_over_screen(score):
                    return
                break

            for pipe in pipes:
                if pipe["x"] + PIPE_WIDTH == player_x:
                    score += 1

            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 40))

            pygame.display.update()
            clock.tick(30)


main()
