import pygame
import moderngl
from pygame.typing import Point, SequenceLike
import bezier
import numpy as np
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, surf):
        pygame.draw.polygon(surf, (255, 255, 255), self.triangle(), 2)
        points = self.bezier_coords(5.1, 0.01)
        surf.set_at(points[1], (255, 0, 255))
        surf.set_at(points[3], (0, 255, 0))


    def bezier_coords(self, eval, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        future_scale = 1
        angle = 275
        distance = dt # 2*pi
        current_pos = self.position
        future_pos = current_pos + forward * PLAYER_SPEED * dt * future_scale
        triangle_pos = pygame.Vector2(self.position.x + distance * np.cos(angle), self.position.y + distance * np.sin(angle))
        
        nodes = np.asfortranarray([
                                  [self.position.x, triangle_pos.x, future_pos.x],
                                  [self.position.y, triangle_pos.y, future_pos.y],
        ])

        curve = bezier.Curve(nodes, degree=2)
        
        new_position = curve.evaluate(eval)

        res = [pygame.Vector2(current_pos), pygame.Vector2(triangle_pos), pygame.Vector2(future_pos), pygame.Vector2(new_position)]
        return res

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_cd -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt * (-1))
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(dt * (-1))
        if keys[pygame.K_SPACE]:
            self.shoot()


    def move(self, dt):
        points = self.bezier_coords(2.1, dt)
        self.position = pygame.Vector2(points[3])

    def shoot(self):
        if self.shot_cd > 0:
            return
        else:
            self.shot_cd = PLAYER_SHOOT_COOLDOWN
            x, y = self.position
            shot = Shot(x, y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
