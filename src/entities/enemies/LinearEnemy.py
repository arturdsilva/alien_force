from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator
import pygame

from config.Constants import Constants, Sounds
from src.entities.enemies.AbstractEnemy import AbstractEnemy


class LinearEnemy(AbstractEnemy):
    """
    Enemy that moves in a straight line.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 2):
        """
        Initializes a linear enemy.

        :param x: Initial enemy x coordinate
        :param y: Initial enemy y coordinate
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.LINEAR_ENEMY_MAX_HEALTH
        self._speed = Constants.LINEAR_ENEMY_SPEED
        projectile_image = pygame.image.load("assets/sprites/projectiles/LinearEnemyProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (
            Constants.LINEAR_ENEMY_PROJECTILE_WIDTH,
            Constants.LINEAR_ENEMY_PROJECTILE_HEIGHT))

        self.__projectile_generator = ProjectileGenerator(150, 1,
                                                          projectile_image,
                                                          10, Sounds.PLASMA)
        self._update_sprite(self._speed)

    def _initialize_sprite(self, x, y):
        """
        Initializes the linear enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.original_image = pygame.image.load(
            "assets/sprites/enemies/LinearEnemy.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (
            Constants.LINEAR_ENEMY_WIDTH, Constants.LINEAR_ENEMY_HEIGHT))
        self.rect = self.original_image.get_rect(center=(x, y))

    def _move(self, dt, terrain=None):
        """
        Updates the linear enemy position.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        self.rect.x += self._speed * dt

        if self._limit_bounds():
            self._speed = -self._speed

    def _attack(self, dt, target, projectiles):
        """
        Attacks an enemy by shooting projectiles.

        :param target: Point where projectile will be headed at.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """
        origin = pygame.math.Vector2(self.rect.center)
        self.__projectile_generator.generate(origin, target, dt, projectiles)

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary.
        """
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of LinearEnemy from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._speed = data["speed"]
        return instance
