import pygame
from circleshape import CircleShape
import constants
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0.0
        self.cooldown = 0.0
        self.reverse_cooldown = 0.0
        self.shots = 0
        self.shots_hit = 0
        self.clock = 0.0

    def collides_with(self, other) -> bool:
        points = self.triangle()

        # 1. Check if circle center is inside the triangle
        if self._point_in_triangle(other.position, points[0], points[1], points[2]):
            return True

        # 2. Check if circle intersects any of the 3 edges
        edges = [(points[0], points[1]), (points[1], points[2]), (points[2], points[0])]
        for p1, p2 in edges:
            if self._circle_intersects_segment(other.position, other.radius, p1, p2):
                return True

        return False

    def _point_in_triangle(self, p: pygame.Vector2, a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2) -> bool:
        # Cross product sign test: p is inside if it's on the same side of all 3 edges
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def _circle_intersects_segment(self, center: pygame.Vector2, radius: float, a: pygame.Vector2, b: pygame.Vector2) -> bool:
        # Vector from a to b
        ab = b - a
        ab_length_sq = ab.length_squared()
        if ab_length_sq == 0:
            return center.distance_to(a) <= radius

        # Project center onto line segment ab, clamped to [0, 1]
        t = max(0.0, min(1.0, (center - a).dot(ab) / ab_length_sq))
        closest_point = a + ab * t

        return center.distance_to(closest_point) <= radius

    def accuracy(self) -> str:
        if self.shots == 0:
            return "0.00%"
        return f"{self.shots_hit / self.shots * 100:.2f}%"

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), constants.LINE_WIDTH)
        pygame.font.init()
        font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
        text = font.render(f"Accuracy: {self.accuracy()}", True, "white")
        text_clock = font.render(f"Time: {self.clock:.2f}", True, "white")

        screen.blit(text, (10, 30))
        screen.blit(text_clock, (10, 50))


    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt: float) -> None:
        self.rotation += constants.PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * constants.PLAYER_SHOOT_SPEED
        self.shots += 1

    def update(self, dt: float) -> None:
        self.position.x = max(0, min(self.position.x, constants.SCREEN_WIDTH))
        self.position.y = max(0, min(self.position.y, constants.SCREEN_HEIGHT))
        self.clock += dt
        self.cooldown -= dt
        self.reverse_cooldown -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if self.reverse_cooldown <= 0:
                self.rotation += 180
                self.reverse_cooldown = constants.PLAYER_REVERSE_COOLDOWN_SECONDS
        if keys[pygame.K_SPACE]:
            if self.cooldown <= 0:
                self.shoot()
                self.cooldown = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
