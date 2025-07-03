import pygame
import moderngl
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from shaders import *

def main():
 
    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    updateable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    spacerocks = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    
    clock = pygame.time.Clock()
    dt = 0
    Player.containers = (updateable, drawable)
    Asteroid.containers = (updateable, drawable, spacerocks)
    AsteroidField.containers = (updateable)
    Shot.containers = (updateable, drawable, projectiles)

    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()
    
    t = 0
    is_running = True
    while is_running:
        
        dt = clock.tick(60) / 1000
        t += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        
        updateable.update(dt)

        
        # drawing
        display.fill((0, 0, 0))

        ## display surface
        for c in drawable:
            c.draw(display)


        ## shaders
        frame_tex = surf_to_texture(display)
        frame_tex.use(0)
        program['tex'] = 0
        program['time'] = t
        render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        for a in spacerocks:
            for b in projectiles:
                if a.collision(b):
                    a.split()
                    b.kill()
            if player.collision(a):
                print(f"Game Over!")
                exit()


        # flips the display where on one side we render and the other we display (DOUBLEBUF)
        pygame.display.flip()
        
        # free up texture as we create a new one each loop
        frame_tex.release()




if __name__ == "__main__":
    main()
