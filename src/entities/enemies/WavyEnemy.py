import numpy as np
import pygame

from config.Constants import Constants
from config.Constants import Sounds
from src.entities.enemies.AbstractEnemy import AbstractEnemy
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator


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
        self._update_sprite(self._speed)
        self.__timer = 0
        self.__amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self.__angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY

        projectile_image = pygame.image.load(
            "assets/sprites/projectiles/WavyEnemyProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (
            Constants.WAVY_ENEMY_PROJECTILE_WIDTH,
            Constants.WAVY_ENEMY_PROJECTILE_HEIGHT))
        self.__projectile_generator = ProjectileGenerator(200, 1,
                                                          projectile_image,
                                                          5, Sounds.LASER_SHOT)

    def _initialize_sprite(self, x, y):
        """
        Initializes the wavy enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.original_image = pygame.image.load(
            "assets/sprites/enemies/WavyEnemy.png").convert_alpha()
        self.original_image = pygame.transform.scale(
            self.original_image,
            (Constants.WAVY_ENEMY_WIDTH, Constants.WAVY_ENEMY_HEIGHT)
        )
        self.original_image = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.original_image.get_rect()
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
            self.__angular_frequency * self.__timer
        )

        self.__timer = (self.__timer + dt) % (
                2 * np.pi / self.__angular_frequency)

        if self._limit_bounds():
            self._speed = -self._speed

    def _attack(self, dt, target, projectiles):
        """
        Attacks an enemy by shooting projectiles.

        :param target: Point where projectile will be headed.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """
        origin = pygame.math.Vector2(self.rect.center)
        self.__projectile_generator.generate(origin, target, dt, projectiles)

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
