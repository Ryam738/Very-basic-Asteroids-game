import random
from collections.abc import Callable

import pygame
from asteroid import Asteroid
from constants import *

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]


class AsteroidField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.game_timer = 0.0

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        self.game_timer += dt
        t7 = min(15, 1 + int(self.game_timer * 0.05))
        kinds = [1, 2, 3, 4, 7]
        weights = [20, 40, 35, 25, t7]


        # Never let the spawn interval go below 0.1 seconds
        spawn_interval = max(0.25, ASTEROID_SPAWN_RATE_SECONDS - (self.game_timer * 0.001))

        if self.spawn_timer > spawn_interval:
            self.spawn_timer = 0

            # Ensure min_speed can never exceed max_speed
            min_speed = 40 + int(self.game_timer * 0.05)
            max_speed = 100 + int(self.game_timer * 0.03)
            edge = random.choice(self.edges)
            position = edge[1](random.uniform(0, 1))
            if self.game_timer < 30:
                kind = random.choices([1, 2, 3], weights=[20, 22, 21])[0]
            else:
                kind = random.choices(kinds, weights=weights)[0]
            if kind == 7:
                speed = random.randint(min_speed - 35, max_speed - 75)
            elif kind == 4:
                speed = random.randint(min_speed - 10, max_speed - 25)
            else:
                speed = random.randint(min_speed, max_speed)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
