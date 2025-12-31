import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("12 Grapes Wish Game 2026")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)

# Player Pac-Man
player_x, player_y = 450, 320
player_speed = 5
player_size = 25

# Grapes (position + velocity)
GRAPE_COUNT = 12
grapes = []
for _ in range(GRAPE_COUNT):
    x = random.randint(60, WIDTH - 60)
    y = random.randint(60, HEIGHT - 60)
    vx = random.uniform(-1.2, 1.2)
    vy = random.uniform(-1.2, 1.2)
    grapes.append({"x": x, "y": y, "vx": vx, "vy": vy})

p = 0
pulse_dir = 1

months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
wishes = []

# Wish input
def get_wish_input(month):
    text = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
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
    with open("2026_WISHES_DECORATED.txt", "w", encoding="utf-8") as f:
        f.write("=============================================\n")
        f.write("        🎉 12 Grapes Wish List for 2026 🎉\n")
        f.write("=============================================\n\n")
        for m, w in zip(months, wishes):
            f.write(f"🌙 {m}\n")
            f.write(f"   ➤ Wish: {w}\n")
            f.write("---------------------------------------------\n")
        f.write("\n✨ May all your wishes come true in 2026! ✨\n")
        f.write("=============================================\n")


# BOUNCING GRAPES LOGIC
def update_grapes():
    R = 14  # radius of grape

    # Move grapes
    for g in grapes:
        g["x"] += g["vx"]
        g["y"] += g["vy"]

        # Bounce off walls
        if g["x"] < R or g["x"] > WIDTH - R:
            g["vx"] *= -1
        if g["y"] < R or g["y"] > HEIGHT - R:
            g["vy"] *= -1

    # Bounce grapes off each other
    for i in range(len(grapes)):
        for j in range(i + 1, len(grapes)):
            g1 = grapes[i]
            g2 = grapes[j]

            dx = g1["x"] - g2["x"]
            dy = g1["y"] - g2["y"]
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < R * 2:  # collision
                # Swap velocities (simple elastic collision)
                g1["vx"], g2["vx"] = g2["vx"], g1["vx"]
                g1["vy"], g2["vy"] = g2["vy"], g1["vy"]


# GAME LOOP
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

    # Update moving grapes
    update_grapes()

    # Check if Pac-Man eats a grape
    for g in grapes[:]:
        dx = player_x - g["x"]
        dy = player_y - g["y"]
        if math.sqrt(dx*dx + dy*dy) < 35:
            grapes.remove(g)
            wish = get_wish_input(months[len(wishes)])
            wishes.append(wish)

            if len(wishes) == GRAPE_COUNT:
                final_screen()

    # Draw background
    screen.fill((10, 10, 20))

    # Grape animation pulse
    p += pulse_dir
    if p > 8 or p < 0:
        pulse_dir *= -1

    # Draw floating/bouncing grapes
    for g in grapes:
        pygame.draw.circle(screen, (150, 0, 200), (int(g["x"]), int(g["y"])), 12 + p)

    # Draw Pac-Man
    pygame.draw.circle(screen, (255, 255, 0), (player_x, player_y), player_size)

    # Pac-Man mouth
    mouth = [
        (player_x, player_y),
        (player_x + 30, player_y - 10),
        (player_x + 30, player_y + 10)
    ]
    pygame.draw.polygon(screen, (10, 10, 20), mouth)

    msg = font.render(f"Grapes left: {len(grapes)}", True, (255, 255, 255))
    screen.blit(msg, (10, 10))

    pygame.display.flip()
    clock.tick(60)
