import pygame

class Score(pygame.sprite.Sprite):
    def __init__(self, score: int = 0) -> None:
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = score

    def draw(self, screen: pygame.Surface) -> None:
        font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))


    def increment(self, amount: int) -> None:
        self.score += amount
