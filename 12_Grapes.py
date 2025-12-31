import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("12 Grapes Wish Game 2026")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

player_x, player_y = 450, 320
player_speed = 5
player_size = 25

GRAPE_COUNT = 12
grapes = []
for _ in range(GRAPE_COUNT):
    x = random.randint(40, WIDTH - 40)
    y = random.randint(40, HEIGHT - 40)
    grapes.append([x, y])

p = 0
pulse_dir = 1

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
wishes = []

# Wish input screen
def get_wish_input(month):
    text = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 45:
                        text += event.unicode

        screen.fill((15, 15, 25))
        label = font.render(f"Write your wish for {month}:", True, (255, 215, 0))
        typed = font.render(text, True, (200, 255, 200))

        screen.blit(label, (50, 200))
        screen.blit(typed, (50, 260))

        pygame.display.flip()
        clock.tick(30)

def final_screen():
    save_wishes()

    running = True
    while running:
        screen.fill((20, 20, 35))

        title = font.render("Hope your wishes get fulfilled in 2026!", True, (255, 230, 0))
        screen.blit(title, (150, 40))

        y = 120
        for m, w in zip(months, wishes):
            line = font.render(f"{m}: {w}", True, (255, 255, 255))
            screen.blit(line, (50, y))
            y += 30

        exit_msg = font.render("Press ESC to exit", True, (255, 150, 150))
        screen.blit(exit_msg, (330, 580))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(30)

def save_wishes():
    with open("2026_WISHES.txt", "w", encoding="utf-8") as f:
        f.write("=============================================\n")
        f.write("        🎉 12 Grapes Wish List for 2026 🎉\n")
        f.write("=============================================\n\n")

        for m, w in zip(months, wishes):
            f.write(f"🌙 {m}\n")
            f.write(f"   ➤ Wish: {w}\n")
            f.write("---------------------------------------------\n")

        f.write("\n✨ May all your wishes come true in 2026! ✨\n")
        f.write("=============================================\n")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:  player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_UP]:    player_y -= player_speed
    if keys[pygame.K_DOWN]:  player_y += player_speed

    player_x = max(20, min(player_x, WIDTH - 20))
    player_y = max(20, min(player_y, HEIGHT - 20))

    for grape in grapes[:]:
        gx, gy = grape
        distance = ((player_x - gx) ** 2 + (player_y - gy) ** 2) ** 0.5

        if distance < 35:  # eat grape
            grapes.remove(grape)
            wish = get_wish_input(months[len(wishes)])
            wishes.append(wish)

            if len(wishes) == GRAPE_COUNT:
                final_screen()

    screen.fill((10, 10, 20))

    p += pulse_dir
    if p > 8 or p < 0:
        pulse_dir *= -1

    for gx, gy in grapes:
        pygame.draw.circle(screen, (150, 0, 200), (gx, gy), 12 + p)

    pygame.draw.circle(screen, (255, 255, 0), (player_x, player_y), player_size)

    mouth_polygon = [
        (player_x, player_y),
        (player_x + 30, player_y - 10),
        (player_x + 30, player_y + 10)
    ]
    pygame.draw.polygon(screen, (10, 10, 20), mouth_polygon)

    msg = font.render(f"Grapes left: {len(grapes)}", True, (255, 255, 255))
    screen.blit(msg, (10, 10))

    pygame.display.flip()
    clock.tick(60)
