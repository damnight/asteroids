import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS



class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, color=(255, 255, 255), center=self.position,
                           radius=self.radius, width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            angle = random.uniform(20, 50)
            vecA = self.velocity.rotate(angle)
            vecB = self.velocity.rotate(-angle)
            radius = self.radius - ASTEROID_MIN_RADIUS
            x, y = self.position
            asteroid_1 = Asteroid(x, y, radius=radius)
            asteroid_2 = Asteroid(x, y, radius=radius)

            asteroid_1.velocity = vecA * 1.2
            asteroid_2.velocity = vecB * 1.2


