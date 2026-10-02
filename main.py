import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot
from score import Score

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Score.containers = (drawable)
    score = Score(0)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    clock = pygame.time.Clock()
    dt = 0.0
    asteroid_field = AsteroidField()
    god_mode = True
    while True: #game loop
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if not god_mode:
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Score: {score.score}")
                    print(f"Accuracy: {player.accuracy()}")
                    sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    player.shots_hit += 1
                    log_event("asteroid_shot")
                    asteroid.split()
                    score.increment(5)
                    shot.kill()
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":

    main()
