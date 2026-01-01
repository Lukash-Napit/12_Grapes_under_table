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

TABLE_TOP_HEIGHT = 120
LEG_WIDTH = 40

UNDER_X = 60
UNDER_Y = TABLE_TOP_HEIGHT
UNDER_W = WIDTH - 120
UNDER_H = HEIGHT - TABLE_TOP_HEIGHT - 30

player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5
player_size = 25

GRAPE_COUNT = 12
grapes = []
for _ in range(GRAPE_COUNT):
    x = random.randint(UNDER_X + 40, UNDER_X + UNDER_W - 40)
    y = random.randint(UNDER_Y + 40, UNDER_Y + UNDER_H - 40)
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

        screen.fill((20, 20, 20))
        draw_table()

        pygame.draw.rect(screen, (15, 15, 25), (UNDER_X+30, UNDER_Y+80, UNDER_W-60, 120))
        pygame.draw.rect(screen, (255, 255, 100), (UNDER_X+30, UNDER_Y+80, UNDER_W-60, 120), 2)

        label = font.render(f"Write your wish for {month}:", True, (255, 215, 0))
        typed = font.render(text, True, (200, 255, 200))
        screen.blit(label, (UNDER_X + 30, UNDER_Y + 40))
        screen.blit(typed, (UNDER_X + 50, UNDER_Y + 130))

        pygame.display.flip()
        clock.tick(30)


def final_screen():
    save_wishes()
    running = True
    while running:
        screen.fill((20, 20, 35))
        draw_table()

        title = font.render("Hope your wishes get fulfilled in 2026!", True, (255, 230, 0))
        screen.blit(title, (150, 40))

        y = TABLE_TOP_HEIGHT + 40
        for m, w in zip(months, wishes):
            line = font.render(f"{m}: {w}", True, (255, 255, 255))
            screen.blit(line, (UNDER_X + 20, y))
            y += 30

        exit_msg = font.render("Press ESC to exit", True, (255, 150, 150))
        screen.blit(exit_msg, (330, HEIGHT - 40))

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

def update_grapes():
    R = 14

    for g in grapes:
        g["x"] += g["vx"]
        g["y"] += g["vy"]

        if g["x"] < UNDER_X + R or g["x"] > UNDER_X + UNDER_W - R:
            g["vx"] *= -1
        if g["y"] < UNDER_Y + R or g["y"] > UNDER_Y + UNDER_H - R:
            g["vy"] *= -1

    for i in range(len(grapes)):
        for j in range(i + 1, len(grapes)):
            g1 = grapes[i]
            g2 = grapes[j]

            dx = g1["x"] - g2["x"]
            dy = g1["y"] - g2["y"]
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < R * 2:
                g1["vx"], g2["vx"] = g2["vx"], g1["vx"]
                g1["vy"], g2["vy"] = g2["vy"], g1["vy"]

def draw_table():
    
    pygame.draw.rect(screen, (120, 80, 40), (0, 0, WIDTH, TABLE_TOP_HEIGHT))

    pygame.draw.rect(screen, (100, 60, 30), (0, TABLE_TOP_HEIGHT, LEG_WIDTH-15, HEIGHT))

    pygame.draw.rect(screen, (100, 60, 30), (WIDTH - LEG_WIDTH, TABLE_TOP_HEIGHT, LEG_WIDTH, HEIGHT))

    pygame.draw.line(screen, (80, 40, 10), (LEG_WIDTH+10, TABLE_TOP_HEIGHT), (LEG_WIDTH+10,HEIGHT-40 ), 15)

    pygame.draw.line(screen, (80, 40, 10), (WIDTH - LEG_WIDTH-LEG_WIDTH-10,TABLE_TOP_HEIGHT), (WIDTH - LEG_WIDTH-LEG_WIDTH-10, HEIGHT-40), 15)

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

    player_x = max(UNDER_X + 20, min(player_x, UNDER_X + UNDER_W - 20))
    player_y = max(UNDER_Y + 20, min(player_y, UNDER_Y + UNDER_H - 20))

    update_grapes()

    for g in grapes[:]:
        dx = player_x - g["x"]
        dy = player_y - g["y"]
        if math.sqrt(dx*dx + dy*dy) < 35:
            grapes.remove(g)
            wish = get_wish_input(months[len(wishes)])
            wishes.append(wish)

            if len(wishes) == GRAPE_COUNT:
                final_screen()

    screen.fill((20, 20, 20))
    draw_table()

    p, pulse_dir
    p += pulse_dir
    if p > 8 or p < 0:
        pulse_dir *= -1

    for g in grapes:
        pygame.draw.circle(screen, (150, 0, 200), (int(g["x"]), int(g["y"])), 12 + p)

    pygame.draw.circle(screen, (255, 255, 0), (player_x, player_y), player_size)
    mouth = [
        (player_x, player_y),
        (player_x + 30, player_y - 10),
        (player_x + 30, player_y + 10)
    ]
    pygame.draw.polygon(screen, (20, 20, 20), mouth)

    msg = font.render(f"Grapes left: {len(grapes)}", True, (255, 255, 255))
    screen.blit(msg, (UNDER_X + 10, UNDER_Y + 10))

    pygame.display.flip()
    clock.tick(60)

