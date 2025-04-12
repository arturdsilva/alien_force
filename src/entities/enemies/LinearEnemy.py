from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator
import pygame

from config.Constants import Constants, Colors
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
        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH,
             Constants.PROJECTILE_DEFAULT_HEIGHT))
        projectile_image.fill(Colors.RED)
        self._projectile_generator = ProjectileGenerator(self, 150, 1,
                                                         projectile_image, 10)

    def _initialize_sprite(self, x, y):
        """
        Initializes the linear enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.image = pygame.image.load(
            "assets/sprites/enemies/LinearEnemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (
            Constants.LINEAR_ENEMY_WIDTH, Constants.LINEAR_ENEMY_HEIGHT))
        self.rect = self.image.get_rect(center=(x, y))

    def _move(self, dt, terrain=None):
        """
        Updates the linear enemy position.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        self.rect.x += self._speed * dt

        if self._limit_bounds():
            self._speed = -self._speed
            self.image = pygame.transform.flip(self.image, True, False)

    def _update_behavior(self, dt, terrain=None):
        """
        Updates specific linear enemy behaviors.
        In this case, there are no additional behaviors to update.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        pass

    def _attack(self, dt, target, projectiles):
        """
        Attacks an enemy by shooting projectiles.

        :param target: Point where projectile will be headed at.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """
        origin = pygame.math.Vector2(self.rect.center)
        self._projectile_generator.generate(origin, target, dt, projectiles)

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
