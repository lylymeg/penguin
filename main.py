import pygame
import random
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Little Penguin & Ice Floe Simulator")
clock = pygame.time.Clock()

# Couleurs (Thème Polaire Doux & Nuit Bleutée)
BG_COLOR = (14, 22, 38)
WATER_COLOR = (24, 52, 84)
WATER_WAVE = (55, 105, 155)
ICE_TOP = (226, 242, 255)
ICE_SIDE = (158, 194, 226)
PENGUIN_BLACK = (36, 44, 62)
PENGUIN_BELLY = (248, 250, 255)
BEAK_ORANGE = (248, 152, 52)
TEXT_COLOR = (242, 246, 255)
GRAY = (130, 148, 174)

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

class JumpingFish:
    def __init__(self, x, water_y):
        self.x = float(x)
        self.y = float(water_y)
        self.vx = random.uniform(-2.2, 2.2)
        self.vy = random.uniform(-6.5, -4.5)
        self.color = random.choice([(255, 135, 180), (110, 225, 255), (255, 205, 95)])
        self.facing_right = self.vx >= 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.22  # Gravité douce

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        pygame.draw.ellipse(surface, self.color, (cx - 10, cy - 5, 20, 10))
        tail_dir = -1 if self.facing_right else 1
        pygame.draw.polygon(surface, self.color, [
            (cx + tail_dir * 9, cy),
            (cx + tail_dir * 16, cy - 5),
            (cx + tail_dir * 16, cy + 5)
        ])
        eye_x = cx + (4 if self.facing_right else -4)
        pygame.draw.circle(surface, (20, 25, 35), (eye_x, cy - 1), 2)

class Penguin:
    def __init__(self, x, y, name="Pipo"):
        self.x = float(x)
        self.y = float(y)
        self.target_x = float(x)
        self.name = name
        self.facing_right = True
        self.waddle_phase = random.uniform(0, math.pi * 2)
        self.wait_timer = random.randint(40, 110)

    def update(self, floe_left, floe_right):
        self.wait_timer -= 1
        if self.wait_timer <= 0:
            self.wait_timer = random.randint(60, 140)
            self.target_x = random.uniform(floe_left + 35, floe_right - 35)

        dx = self.target_x - self.x
        if abs(dx) > 4:
            self.facing_right = dx >= 0
            step = min(abs(dx), 1.3)
            self.x += step if dx > 0 else -step
            self.waddle_phase += 0.22

    def draw(self, surface):
        cx, cy = int(self.x), int(self.y)
        waddle = int(math.sin(self.waddle_phase) * 2.5)
        dir_sign = 1 if self.facing_right else -1

        # Petits pieds orange
        foot_shift = int(math.sin(self.waddle_phase) * 3)
        pygame.draw.ellipse(surface, BEAK_ORANGE, (cx - 12 + foot_shift, cy + 16, 11, 6))
        pygame.draw.ellipse(surface, BEAK_ORANGE, (cx + 2 - foot_shift, cy + 16, 11, 6))

        # Corps du pingouin
        pygame.draw.ellipse(surface, PENGUIN_BLACK, (cx - 15, cy - 14 + waddle, 30, 32))
        pygame.draw.ellipse(surface, PENGUIN_BELLY, (cx - 9 + dir_sign * 2, cy - 8 + waddle, 18, 23))

        # Petite aile
        wing_x = cx - dir_sign * 13
        pygame.draw.ellipse(surface, PENGUIN_BLACK, (wing_x - 4, cy - 6 + waddle, 8, 16))

        # Tête, yeux et bec
        head_x = cx + dir_sign * 2
        head_y = cy - 20 + waddle
        pygame.draw.circle(surface, PENGUIN_BLACK, (head_x, head_y), 11)
        pygame.draw.circle(surface, (25, 30, 40), (head_x + dir_sign * 5, head_y - 2), 2)
        pygame.draw.polygon(surface, BEAK_ORANGE, [
            (head_x + dir_sign * 8, head_y + 1),
            (head_x + dir_sign * 15, head_y + 3),
            (head_x + dir_sign * 8, head_y + 5)
        ])

        # Prénom au-dessus du pingouin
        label = font_small.render(self.name, True, TEXT_COLOR)
        surface.blit(label, (cx - label.get_width() // 2, head_y - 26))

PENGUIN_NAMES = ["Pipo", "Flocon", "Glaçon", "Mochi", "Bibi", "Plume", "Nori"]

water_y = HEIGHT - 185
floe_left = WIDTH // 2 - 190
floe_right = WIDTH // 2 + 190
floe_top = water_y - 12

penguins = [Penguin(WIDTH // 2 - 40, floe_top - 16, "Pipo")]
jumping_fish = []
snowflakes = [
    [random.uniform(0, WIDTH), random.uniform(75, HEIGHT), random.uniform(1.5, 3.0), random.uniform(0.8, 1.7)]
    for _ in range(60)
]

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and mouse_pos[1] > 80:
                # Clic gauche : Faire bondir de petits poissons dans l'eau
                for _ in range(3):
                    fx = mouse_pos[0] + random.randint(-35, 35)
                    jumping_fish.append(JumpingFish(fx, water_y + 8))

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if len(penguins) < 6:
                    pname = PENGUIN_NAMES[len(penguins) % len(PENGUIN_NAMES)]
                    px = random.uniform(floe_left + 40, floe_right - 40)
                    penguins.append(Penguin(px, floe_top - 16, pname))
            elif event.key == pygame.K_r:
                penguins = [Penguin(WIDTH // 2 - 40, floe_top - 16, "Pipo")]
                jumping_fish = []

    # Mise à jour de la neige douce
    for flake in snowflakes:
        flake[0] = (flake[0] + math.sin(flake[1] * 0.02) * 0.5) % WIDTH
        flake[1] += flake[2]
        if flake[1] > HEIGHT:
            flake[1] = 75
            flake[0] = random.uniform(0, WIDTH)

    # Mise à jour des poissons bondissants
    for fish in jumping_fish[:]:
        fish.update()
        if fish.y > HEIGHT + 20:
            jumping_fish.remove(fish)

    # Mise à jour des pingouins
    for p in penguins:
        p.update(floe_left, floe_right)

    # --- RENDU GRAPHIQUE ---
    screen.fill(BG_COLOR)

    # Eau de l'océan polaire
    pygame.draw.rect(screen, WATER_COLOR, (0, water_y, WIDTH, HEIGHT - water_y))

    # Petites vagues douces sur l'eau
    wave_shift = int(math.sin(pygame.time.get_ticks() * 0.002) * 10)
    for wx in range(30, WIDTH - 20, 95):
        wy = water_y + 28 + ((wx // 95) % 3) * 26
        pygame.draw.line(screen, WATER_WAVE, (wx + wave_shift, wy), (wx + 32 + wave_shift, wy), 2)

    # Banquise flottante
    pygame.draw.rect(screen, ICE_SIDE, (floe_left, floe_top + 10, floe_right - floe_left, 24), border_bottom_left_radius=12, border_bottom_right_radius=12)
    pygame.draw.rect(screen, ICE_TOP, (floe_left - 8, floe_top, (floe_right - floe_left) + 16, 16), border_radius=8)

    # Pingouins sur la banquise
    for p in penguins:
        p.draw(screen)

    # Poissons qui bondissent
    for fish in jumping_fish:
        fish.draw(screen)

    # Flocons de neige
    for flake in snowflakes:
        pygame.draw.circle(screen, (240, 248, 255), (int(flake[0]), int(flake[1])), int(flake[3]))

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("LITTLE PENGUIN & ICE FLOE — BANQUISE INTERACTIVE", True, TEXT_COLOR)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 12))

    stats_txt = font_small.render(f"Pingouins : {len(penguins)} | Poissons en l'air : {len(jumping_fish)}", True, ICE_TOP)
    screen.blit(stats_txt, (40, 42))

    inst_txt = font_small.render("CLIC GAUCHE : Faire bondir des poissons | P : Ajouter un pingouin | R : Reset", True, GRAY)
    screen.blit(inst_txt, (WIDTH - inst_txt.get_width() - 40, 42))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()