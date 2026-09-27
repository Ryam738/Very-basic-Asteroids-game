
import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, 0)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "White", self.position, self.radius, 2)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
