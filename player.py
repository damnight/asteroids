import pygame
import moderngl
from pygame.typing import Point, SequenceLike
import numpy as np
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd = 0
        self.momentum = 0
        self.previous_position = pygame.Vector2() # previous dt position
        self.past_position = pygame.Vector2() # previous dt position
        self.acceleration = 1.1
        self.grip = 0.5
        self.mass = 100

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

    def slip(self, prev, curr, dt):
        # forward = pygame.Vector2(0, 1).rotate(self.rotation)
        future_position = linear_movement(curr, self.rotation, dt)
        vec1 = prev - curr
        vec2 = prev - future_position

        slip_angle = vec1.angle_to(vec2)

        # slip should be vector from the current position, at the slip angle multiplied by the momentum which is a decaying velocity
        slip = self.momentum * pygame.Vector2(0, 1).rotate(self.rotation).rotate(slip_angle)
        return slip


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

        self.move(dt, passive=True)


    def move(self, dt, passive=False):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        if not passive:
            self.momentum += self.mass * np.linalg.norm(self.past_position - self.position) * dt

        slip = self.slip(self.previous_position, self.position, dt)

        if np.linalg.norm(slip) < 1:
            slip = pygame.Vector2(0, 0)

        self.past_position = self.previous_position.copy()
        self.previous_position = self.position.copy()

        if not passive:
            self.position += dt * (PLAYER_SPEED + self.momentum) * forward + slip * dt
        if passive:
            self.position += dt * slip * self.momentum

        # decay
        if self.momentum > 0:
            self.momentum -= self.momentum * dt
        if self.momentum < 1:
            self.momentum = 0
        if self.momentum > 25:
            self.momentum = 25


    def shoot(self):
        if self.shot_cd > 0:
            return
        else:
            self.shot_cd = PLAYER_SHOOT_COOLDOWN
            x, y = self.position
            shot = Shot(x, y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED



def static_rotation(rotation, dt):
    return rotation + PLAYER_TURN_SPEED * dt

def linear_movement(position, rotation, dt):
    towards = pygame.Vector2(0, 1).rotate(static_rotation(rotation, dt))
    return position + dt * PLAYER_SPEED * towards

