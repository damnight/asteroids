import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot
from slash import Slash
import numpy as np

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0
        self.slash_cd = 0


    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, (50, 50, 50), self.triangle(), width=1)
        pygame.draw.circle(screen, (0, 255, 0), radius=PLAYER_RADIUS, center=self.position, width=2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def set_rotation(self):
        x, y = pygame.mouse.get_pos()
        u, v = self.position

        angle = np.cos((x * u + y * v) / np.sqrt(x*x + y*y) * np.sqrt(u*u + v*v))

        print(angle * 180/np.pi)

        self.rotation = angle * 180/np.pi


    def update(self, dt):
        self.shot_cd -= dt
        self.slash_cd -= dt

        self.set_rotation()

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.strife(dt * (-1))
        if keys[pygame.K_d]:
            self.strife(dt)

#       if keys[pygame.K_w] and keys[pygame.K_a]:
#           self.rotate(dt * (-1))
#           self.move(dt)
#       if keys[pygame.K_w] and keys[pygame.K_d]:
#           self.rotate(dt)
#           self.move(dt)
        
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * (-1))
        
        if keys[pygame.K_SPACE]:
            self.slash()

    def strife(self, dt):
        lateral = pygame.Vector2(0,1).rotate(self.rotation + 90)
        self.position += lateral * PLAYER_SPEED * dt


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shot_cd > 0:
            return
        else:
            self.shot_cd = PLAYER_SHOOT_COOLDOWN
            x, y = self.position
            shot = Shot(x, y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def slash(self):
        if self.slash_cd > 0:
            return
        else:
            self.slash_cd = PLAYER_SLASH_COOLDOWN
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            x, y = self.position + forward * self.radius
            slash = Slash(x, y, self.rotation)
            slash.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SLASH_SPEED
