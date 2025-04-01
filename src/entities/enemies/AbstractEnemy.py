import pygame
from config.Constants import Constants, Colors
from src.entities.Projectile import Projectile, ProjectileGenerator


class AbstractEnemy(pygame.sprite.Sprite):
    """
    Represents an enemy.
    """

    def __init__(self, x=0, y=Constants.HEIGHT / 10):
        """
        Initializes an enemy.

        :param x: The initial enemy x coordinate.
        :param y: The initial enemy y coordinate.
        """

        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(Colors.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._speed = 1 * Constants.ENEMY_SPEED
        self._health_points = None
        self.projectile_generator = None

    def update(self, dt):
        """
        Updates the enemy.

        :param dt: The duration of one iteration.
        """

        self.move(dt)
        self.limit_bounds()

    def move(self, dt):
        """
        Updates the enemy position.

        :param dt: The duration of one iteration.
        """

        self.rect.x += self._speed * dt
        if self.limit_bounds():
            self._speed = -self._speed

    def limit_bounds(self):
        """
        Limits enemy position to inside screen boundaries.
        """

        out_of_bounds = False
        if self.rect.left < 0:
            self.rect.left = 0
            out_of_bounds = True
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            out_of_bounds = True
        if self.rect.top < 0:
            self.rect.top = 0
            out_of_bounds = True
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
            out_of_bounds = True

        return out_of_bounds
