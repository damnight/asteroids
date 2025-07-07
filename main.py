import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from slash import Slash

def main():
 
    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    spacerocks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    single_use = pygame.sprite.Group()
    delayed_kill = pygame.sprite.Group()
    attacks = pygame.sprite.Group()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock()
    dt = 0
    Player.containers = (updateable, drawable)
    Asteroid.containers = (updateable, drawable, spacerocks)
    AsteroidField.containers = (updateable)
    Shot.containers = (updateable, drawable, projectiles)
    Slash.containers = (updateable, drawable, delayed_kill, attacks)

    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_x]:
            exit()

        screen.fill("black")

        updateable.update(dt)
        for c in drawable:
            c.draw(screen)
        for a in spacerocks:
            for b in projectiles:
                if a.collision(b):
                    a.split()
                    b.kill()
            for atk in attacks:
                if a.collision(atk):
                    a.split()

            if player.collision(a):
                print(f"Game Over!")
                exit()

        pygame.display.flip()



        dt = clock.tick(60) / 1000
        
        for s in single_use:
            s.kill()

        for d in delayed_kill:
            d.kill_delayed(dt)



if __name__ == "__main__":
    main()
