import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("12 Grapes Wish Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

player_size = 30
player = pygame.Rect(400, 300, player_size, player_size)
player_speed = 5

GRAPE_COUNT = 12
grapes = []
for _ in range(GRAPE_COUNT):
    x = random.randint(20, WIDTH - 40)
    y = random.randint(20, HEIGHT - 40)
    grapes.append(pygame.Rect(x, y, 20, 20))

wishes = []

def get_wish_input(grape_number):
    user_text = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_text
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 40:
                        user_text += event.unicode

        screen.fill((30, 30, 30))
        message = font.render(f"Enter Wish #{grape_number} and press ENTER:", True, (255, 255, 255))
        text_surface = font.render(user_text, True, (200, 255, 200))

        screen.blit(message, (40, 200))
        screen.blit(text_surface, (40, 260))

        pygame.display.flip()
        clock.tick(30)


def show_final_screen():
    running = True
    while running:
        screen.fill((10, 10, 20))

        title = font.render("Hope your wishes get fulfilled in 2026!", True, (255, 215, 0))
        screen.blit(title, (180, 50))

        y_offset = 120
        for i, wish in enumerate(wishes, start=1):
            line = font.render(f"{i}. {wish}", True, (255, 255, 255))
            screen.blit(line, (50, y_offset))
            y_offset += 30

        exit_text = font.render("Press ESC to exit", True, (255, 150, 150))
        screen.blit(exit_text, (280, 520))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()
    pygame.quit()
    sys.exit()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += player_speed

    player.x = max(0, min(player.x, WIDTH - player_size))
    player.y = max(0, min(player.y, HEIGHT - player_size))

    for grape in grapes[:]:
        if player.colliderect(grape):
            grapes.remove(grape)
            wish = get_wish_input(len(wishes) + 1)
            wishes.append(wish)

            if len(wishes) == GRAPE_COUNT:
                show_final_screen()

    screen.fill((0, 0, 20))

    pygame.draw.circle(screen, (255, 255, 0), player.center, player_size // 2)


    for grape in grapes:
        pygame.draw.circle(screen, (160, 32, 240), grape.center, 10)

    info = font.render(f"Grapes left: {len(grapes)}", True, (255, 255, 255))
    screen.blit(info, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
