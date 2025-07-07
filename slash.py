import pygame
from constants import *
from circleshape import CircleShape

class Slash(CircleShape):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, SLASH_RADIUS)
        self.angle = 0
        self.rotation = rotation
        self.slash_speed = PLAYER_SLASH_SPEED

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
 
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 165, 0), self.triangle())
        
        end1 = self.aoe_cone()
        pygame.draw.line(screen, (255, 0, 0), start_pos=self.position, end_pos=end1)

    def aoe_cone(self, cone_range=15):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + self.angle) * self.radius / 1.5

        end1 = self.position + forward * (PLAYER_RADIUS + cone_range) - right

        return end1



    def update(self, dt):
        self.angle += self.slash_speed * dt
