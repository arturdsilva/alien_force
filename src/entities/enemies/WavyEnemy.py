from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
from entities.projectiles.ProjectileGenerator import ProjectileGenerator
import numpy as np
import pygame

from config.Constants import Constants, Colors
from entities.projectiles.ProjectileGenerator import ProjectileGenerator
from src.entities.enemies.AbstractEnemy import AbstractEnemy


class WavyEnemy(AbstractEnemy):
    """
    Enemy that moves in a sinusoidal pattern.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 3):
        """
        Initializes a wavy enemy.

        :param x: Initial enemy x coordinate
        :param y: Initial enemy y coordinate
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.WAVY_ENEMY_MAX_HEALTH
        self._speed = Constants.WAVY_ENEMY_SPEED
        self.__timer = 0
        self.__amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self.__angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY
        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH,
             Constants.PROJECTILE_DEFAULT_HEIGHT))
        projectile_image.fill(Colors.GREEN)
        self._projectile_generator = ProjectileGenerator(self, 200, 1,
                                                         projectile_image, 5)

    def _initialize_sprite(self, x, y):
        """
        Initializes the wavy enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.image = pygame.Surface((Constants.WAVY_ENEMY_WIDTH,
                                     Constants.WAVY_ENEMY_HEIGHT))
        self.image.fill(Colors.BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def _move(self, dt, terrain=None):
        """
        Updates the wavy enemy position.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        self.rect.x += self._speed * dt
        self.rect.y = Constants.WAVY_ENEMY_Y + self.__amplitude * np.sin(
            self.__angular_frequency * self.__timer)

        if self._limit_bounds():
            self._speed = -self._speed

    def _update_behavior(self, dt, terrain=None):
        """
        Updates the timer for wavy movement.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        self.__timer = (self.__timer + dt) % (
                2 * np.pi / self.__angular_frequency)

    def _attack(self, dt, target, projectiles):
        """
        Attacks an enemy by shooting projectiles.

        :param target: Point where projectile will be headed at.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """

        self._projectile_generator.generate(target, dt, projectiles)

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary, including WavyEnemy-specific attributes.
        """
        data = super().to_dict()
        data["timer"] = self.__timer
        data["amplitude"] = self.__amplitude
        data["angular_frequency"] = self.__angular_frequency
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of WavyEnemy from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._speed = data["speed"]
        instance.__timer = data.get("timer", 0)
        instance.__amplitude = data.get("amplitude",
                                        Constants.WAVY_ENEMY_AMPLITUDE)
        instance.__angular_frequency = data.get("angular_frequency",
                                                Constants.WAVY_ENEMY_ANGULAR_FREQUENCY)
        return instance
