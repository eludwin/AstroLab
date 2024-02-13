import pygame
import math


pygame.init()

WIDTH, HEIGHT = 1080, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstraLab")

AU = 149.6e6 * 1000
G = 6.67428e-11

SCALE = 100 / AU  # 100 / AU is 1AU = 100 pixels. Adjust the scale if needed
TIMESTEP = 3600 * 24  # 3600 * 24 = 1 day per frame. Adjust the timestep to slow down the simulation



Yellow = (255, 255, 0)
Blue = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WHITE = (255, 255, 255)

pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)

# New variables for zoom control
zoom_factor = 0.05  # How much each scroll zooms in or out


class Planet:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win, ofx,ofy):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = [(point[0] * SCALE + WIDTH / 2+ofx, point[1] * SCALE + HEIGHT / 2+ofy) for point in self.orbit]
            pygame.draw.lines(win, DARK_GREY, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (int(x) + ofx, int(y)+ofy), self.radius*SCALE*AU/200)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x) # theta is the angle
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * TIMESTEP
        self.y_velocity += total_fy / self.mass * TIMESTEP

        self.x += self.x_velocity * TIMESTEP
        self.y += self.y_velocity * TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    global SCALE  # Make SCALE modifiable globally
    running = True
    clock = pygame.time.Clock()

    # Planet definitions remain the same

    sun = Planet(0, 0, 30, Yellow, 1.98892 * 10 ** 30)  # Sun
    sun.sun = True

    mercury = Planet(0.387 * AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23)  # Mercury
    mercury.y_velocity = -47.4 * 1000

    venus = Planet(0.723 * AU, 0, 14, WHITE, 4.8685 * 10 ** 24)  # Venus
    venus.y_velocity = -35.02 * 1000

    earth = Planet(-1 * AU, 0, 16, Blue, 5.9742 * 10 ** 24)  # Earth
    earth.y_velocity = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 12, RED, 6.39 * 10 ** 23)  # Mars
    mars.y_velocity = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 28, (255, 165, 0), 1.898 * 10 ** 27)
    jupiter.y_velocity = 13.06 * 1000

    saturn = Planet(9.582 * AU, 0, 30, (204, 204, 102), 5.683 * 10 ** 26)
    saturn.y_velocity = 9.68 * 1000

    uranus = Planet(19.218 * AU, 0, 32, (173, 216, 230), 8.681 * 10 ** 25)
    uranus.y_velocity = 6.80 * 1000

    neptune = Planet(30.110 * AU, 0, 34, (65, 105, 225), 1.024 * 10 ** 26)
    neptune.y_velocity = 5.43 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    days_passed = 0
    ofx, ofy = 0, 0
    currx, curry = pygame.mouse.get_pos()

    while running:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, ofx,ofy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in
                if event.button == 4:
                    SCALE *= (1 + zoom_factor)
                # Zoom out
                if event.button == 5:
                    SCALE /= (1 + zoom_factor)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    currx = pygame.mouse.get_pos()[0] - ofx
                    curry = pygame.mouse.get_pos()[1] - ofy
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    ofx = pygame.mouse.get_pos()[0]- currx
                    ofy = pygame.mouse.get_pos()[1] - curry





        days_passed += TIMESTEP / (3600 * 24)
        days_text = font.render(f"Days passed: {int(days_passed)} Days", True, (255, 255, 255))
        WIN.blit(days_text, (10, 10))

        pygame.display.update()

    pygame.quit()

main()
