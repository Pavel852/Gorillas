import pygame
import random
import math
import sys

pygame.init()

# -------------------------------------------------
#  ZÁKLADNÍ NASTAVENÍ HRY
# -------------------------------------------------
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 30

# Barvy v RGB
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
YELLOW = (255, 255,   0)
GRAY   = (150, 150, 150)
BROWN  = (139,  69,  19)

# Fyzika
GRAVITY = 9.8              # (m/s^2)
PIXELS_PER_METER = 30      # 1m = 30px => viditelný, pomalejší pohyb

# Pomocná funkce na vykreslení textu
def draw_text(surface, text, x, y, size=30, color=WHITE, center=True):
    font = pygame.font.SysFont("arial", size, bold=True)
    rend = font.render(text, True, color)
    rect = rend.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rend, rect)


# -------------------------------------------------
#  TŘÍDA PRO BUDOVU
# -------------------------------------------------
class Building:
    def __init__(self, x, w, h):
        self.x = x  
        self.w = w  
        self.h = h  

        self.color = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )

        # Matice "oken" (souřadnice + boolean pro rozsvícení)
        self.window_positions = []
        self.window_lit = []
        base_y = SCREEN_HEIGHT - self.h
        step_x = 20
        step_y = 20
        for wx in range(self.x + 5, self.x + self.w - 5, step_x):
            col = []
            col_lit = []
            for wy in range(base_y + 5, SCREEN_HEIGHT - 5, step_y):
                col.append((wx, wy))
                # ~30% šance na rozsvícené okno
                col_lit.append(random.random() < 0.3)
            self.window_positions.append(col)
            self.window_lit.append(col_lit)

    def draw(self, surface):
        base_y = SCREEN_HEIGHT
        pygame.draw.rect(surface, self.color, (self.x, base_y - self.h, self.w, self.h))
        # Okna:
        for ix, col in enumerate(self.window_positions):
            for iy, (wx, wy) in enumerate(col):
                if self.window_lit[ix][iy]:
                    pygame.draw.rect(surface, YELLOW, (wx, wy, 5, 5))

    def flicker(self):
        """
        Jednou za čas přepneme stav jediného okna (True->False/False->True)
        abychom dosáhli efektu pomalého blikání. 
        """
        if random.random() < 0.02:
            ix = random.randrange(len(self.window_positions))
            if self.window_positions[ix]:
                iy = random.randrange(len(self.window_positions[ix]))
                self.window_lit[ix][iy] = not self.window_lit[ix][iy]


# -------------------------------------------------
#  TŘÍDA PRO GORILU
# -------------------------------------------------
class Gorilla:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.color_body = BROWN
        self.color_head = (255, 200, 150)

    def draw(self, surface):
        # TĚLO (ovál)
        body_rect = pygame.Rect(0, 0, 40, 50)
        body_rect.center = (self.x, self.y)
        pygame.draw.ellipse(surface, self.color_body, body_rect)

        # HLAVA (kruh)
        head_x = self.x
        head_y = self.y - 40
        pygame.draw.circle(surface, self.color_head, (head_x, head_y), 12)

        # OČI
        pygame.draw.circle(surface, BLACK, (head_x - 4, head_y - 3), 2)
        pygame.draw.circle(surface, BLACK, (head_x + 4, head_y - 3), 2)

        # RUCE (úsečky)
        left_arm = (self.x - 20, self.y)
        right_arm = (self.x + 20, self.y)
        pygame.draw.line(surface, self.color_body, left_arm, (self.x - 10, self.y - 10), 4)
        pygame.draw.line(surface, self.color_body, right_arm, (self.x + 10, self.y - 10), 4)


# -------------------------------------------------
#  TŘÍDA PRO BANÁN
# -------------------------------------------------
class Banana:
    def __init__(self, x, y, angle_deg, velocity, wind):
        self.x = x
        self.y = y
        self.radius = 8
        self.color = YELLOW

        self.angle = math.radians(angle_deg)
        self.vx = velocity * math.cos(self.angle) * PIXELS_PER_METER
        self.vy = -velocity * math.sin(self.angle) * PIXELS_PER_METER
        self.wind = wind
        self.active = True

    def update(self, dt):
        self.x += (self.vx + self.wind) * dt
        g_pix = GRAVITY * PIXELS_PER_METER
        self.y += self.vy * dt + 0.5 * g_pix * (dt ** 2)
        self.vy += g_pix * dt

        if self.x < 0 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT:
            self.active = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# -------------------------------------------------
#  GENEROVÁNÍ MĚSTA
# -------------------------------------------------
def generate_city():
    buildings = []
    x = 0
    while x < SCREEN_WIDTH:
        w = random.randint(60, 90)
        h = random.randint(100, 250)
        b = Building(x, w, h)
        buildings.append(b)
        x += w
    return buildings

def find_top_of_building(buildings, desired_x):
    for b in buildings:
        if b.x <= desired_x <= b.x + b.w:
            return SCREEN_HEIGHT - b.h
    return SCREEN_HEIGHT


# -------------------------------------------------
#  VYKRESLENÍ VEKTORU HODU
# -------------------------------------------------
def draw_throw_vector(surface, gorilla_x, gorilla_y, angle_deg, velocity, color=RED):
    """
    Vykreslí vektor (šipku) trochu nad hlavou gorily,
    s délkou úměrnou velocity, směr podle angle_deg.
    Posunuli jsme výchozí bod o pár pixelů výš,
    aby šipka nezasahovala gorile do hlavy.
    """
    # Gorila: tělo střed (gorilla_x, gorilla_y).
    # Hlava ~ 40 px výš => šipku posuneme ještě trochu nad hlavu, např. + 20 px.
    offset = 60  # tj. 40 (hlava) + 20 navíc
    start_x = gorilla_x
    start_y = gorilla_y - offset

    # Délka šipky roste se zadanou rychlostí.
    length = velocity * 2.0
    rad = math.radians(angle_deg)
    end_x = start_x + length * math.cos(rad)
    end_y = start_y - length * math.sin(rad)  # minus, bo y roste dolů

    # Hlavní čára
    pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 3)

    # Na konci malé "křidélko" do stran
    arrow_size = 8
    left_angle = rad + math.radians(150)
    right_angle = rad - math.radians(150)

    left_x = end_x + arrow_size * math.cos(left_angle)
    left_y = end_y - arrow_size * math.sin(left_angle)
    right_x = end_x + arrow_size * math.cos(right_angle)
    right_y = end_y - arrow_size * math.sin(right_angle)

    pygame.draw.line(surface, color, (end_x, end_y), (left_x, left_y), 2)
    pygame.draw.line(surface, color, (end_x, end_y), (right_x, right_y), 2)


# -------------------------------------------------
#  HLAVNÍ HERNÍ CYKLUS
# -------------------------------------------------
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gorillas in Python")
    clock = pygame.time.Clock()

    # Vygenerujeme město
    buildings = generate_city()

    # Vítr
    wind = random.randint(-50, 50)

    # Gorila 1
    g1_x = 100
    top1 = find_top_of_building(buildings, g1_x)
    gorilla1 = Gorilla("Hráč 1", g1_x, top1 - 25)

    # Gorila 2
    g2_x = SCREEN_WIDTH - 100
    top2 = find_top_of_building(buildings, g2_x)
    gorilla2 = Gorilla("Hráč 2", g2_x, top2 - 25)

    current_player = 1
    banana = None
    angle = 45
    velocity = 25
    run_game = True

    # Časovač pro "blikání" oken
    flicker_timer = 0.0

    # Zobrazení nápovědy
    show_help = False

    while run_game:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            elif event.type == pygame.KEYDOWN:
                # ESC – ukončení hry nebo ukončení nápovědy
                if event.key == pygame.K_ESCAPE:
                    if show_help:
                        show_help = False
                    else:
                        run_game = False

                # F1 – přepnout / vypnout nápovědu
                elif event.key == pygame.K_F1:
                    show_help = not show_help

                if not show_help:  
                    # Jen pokud nápověda není zapnutá, zpracováváme ovládání hry
                    if event.key == pygame.K_UP:
                        angle = min(angle + 1, 180)
                    elif event.key == pygame.K_DOWN:
                        angle = max(angle - 1, 0)
                    elif event.key == pygame.K_RIGHT:
                        velocity = min(velocity + 1, 100)
                    elif event.key == pygame.K_LEFT:
                        velocity = max(velocity - 1, 5)
                    elif event.key == pygame.K_SPACE:
                        if current_player == 1:
                            banana = Banana(gorilla1.x, gorilla1.y - 45, angle, velocity, wind)
                        else:
                            banana = Banana(gorilla2.x, gorilla2.y - 45, 180 - angle, velocity, wind)

        # Pokud je zobrazená nápověda, jen ji vykreslíme a vynecháme zbytek hry
        if show_help:
            # Vykreslíme poloprůhledný overlay
            screen.fill(BLACK)
            # Můžeme např. vykreslit obdélník se 70% průhledností
            # V pygame není nativní alfa pro primitive fill, tak často stačí:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  
            s.set_alpha(200)    # 0 - zcela průhledné, 255 - zcela neprůhledné
            s.fill((50, 50, 50))
            screen.blit(s, (0, 0))

            # Texty
            draw_text(screen, "Nápověda / Info", SCREEN_WIDTH//2, 100, size=40)
            draw_text(screen, "Autor: PB", SCREEN_WIDTH//2, 180, size=30)
            draw_text(screen, "Ovládání:", SCREEN_WIDTH//2, 240, size=35)
            draw_text(screen, "← / → mění rychlost hodu", SCREEN_WIDTH//2, 280, size=25)
            draw_text(screen, "↑ / ↓ mění úhel hodu", SCREEN_WIDTH//2, 310, size=25)
            draw_text(screen, "Mezerník = hod banánem", SCREEN_WIDTH//2, 340, size=25)
            draw_text(screen, "F1 = zapnout / vypnout tuto nápovědu", SCREEN_WIDTH//2, 370, size=25)
            draw_text(screen, "ESC = ukončit hru (nebo nápovědu)", SCREEN_WIDTH//2, 400, size=25)

            pygame.display.flip()
            continue

        # Pokud nápověda není zapnutá, běží běžná logika hry

        # Občas flicker oken
        flicker_timer += dt
        if flicker_timer >= 1.0:
            flicker_timer = 0.0
            for b in buildings:
                b.flicker()

        # Aktualizace banánu
        if banana and banana.active:
            banana.update(dt)
            # Kolize s gorilou 1
            dist1 = math.hypot(banana.x - gorilla1.x, banana.y - gorilla1.y)
            if dist1 < (25 + banana.radius):
                print("Zásah do Hráče 1!")
                banana.active = False
            # Kolize s gorilou 2
            dist2 = math.hypot(banana.x - gorilla2.x, banana.y - gorilla2.y)
            if dist2 < (25 + banana.radius):
                print("Zásah do Hráče 2!")
                banana.active = False

            if not banana.active:
                current_player = 1 if current_player == 2 else 2
                angle = 45
                velocity = 25

        # Vykreslení scény
        screen.fill(BLACK)

        # Budovy
        for b in buildings:
            b.draw(screen)

        # Gorily
        gorilla1.draw(screen)
        gorilla2.draw(screen)

        # Banán
        if banana and banana.active:
            banana.draw(screen)

        # Horní info
        info_text = (
            f"Na tahu: Hráč {current_player} | "
            f"Úhel: {angle}° | Rychlost: {velocity} m/s | Vítr: {wind} px/s"
        )
        draw_text(screen, info_text, SCREEN_WIDTH // 2, 20, size=24, color=WHITE)

        # Vektor nad gorilou, která je na tahu
        if current_player == 1:
            draw_throw_vector(screen, gorilla1.x, gorilla1.y, angle, velocity, color=RED)
        else:
            # Hráč 2 – zrcadlový úhel
            draw_throw_vector(screen, gorilla2.x, gorilla2.y, 180 - angle, velocity, color=RED)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# -------------------------------------------------
#  SPUŠTĚNÍ
# -------------------------------------------------
if __name__ == "__main__":
    main()
