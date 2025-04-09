from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
from src.entities.Projectile import ProjectileGenerator
import numpy as np
import pygame


class WavyEnemy(AbstractEnemy):
    """
    Represents an enemy with sinusoidal movement.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 3):
        """
        Initializes a wavy enemy.

        :param x: The initial enemy x coordinate.
        :param y: The initial enemy y coordinate.
        """

        super().__init__(x=x, y=y)
        self.image = pygame.Surface((Constants.WAVY_ENEMY_WIDTH,
                                     Constants.WAVY_ENEMY_HEIGHT))
        self.image.fill(Colors.BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._speed = 1.5 * Constants.ENEMY_SPEED
        self._health_points = Constants.WAVY_ENEMY_MAX_HEALTH
        self.__timer = 0
        self.__amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self.__angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY
        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH,
             Constants.PROJECTILE_DEFAULT_HEIGHT))
        projectile_image.fill(Colors.GREEN)
        self._projectile_generator = ProjectileGenerator(self, 300, 1,
                                                         projectile_image, 5)

    def _move(self, dt):
        """
        Updates the wavy enemy position.

        :param dt: The duration of one iteration.
        """

        self.rect.x += self._speed * dt
        self.rect.y = Constants.WAVY_ENEMY_Y + self.__amplitude * np.sin(
            self.__angular_frequency * self.__timer)
        self.__timer = (self.__timer + dt) % (
                2 * np.pi / self.__angular_frequency)

        if self._limit_bounds():
            self._speed = -self._speed

    def _attack(self, dt, target, projectiles):
        """
        Attacks an enemy by shooting projectiles.

        :param target: Point where projectile will be headed at.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """

        self._projectile_generator.generate(target, dt, projectiles)
