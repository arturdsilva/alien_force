from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
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
        self._timer = 0
        self._amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self._angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY
        self._health_points = Constants.WAVY_ENEMY_MAX_HEALTH

    def move(self, dt):
        """
        Updates the wavy enemy position.

        :param dt: The duration of one iteration.
        """

        self.rect.x += self._speed * dt
        self.rect.y = Constants.WAVY_ENEMY_Y + self._amplitude * np.sin(
            self._angular_frequency * self._timer)
        self._timer = (self._timer + dt) % (
                2 * np.pi / self._angular_frequency)

        if self.limit_bounds():
            self._speed = -self._speed
