from src.entities.projectiles.BombProjectile import BombProjectile
import pygame

from config.Constants import Constants
from src.entities.enemies.AbstractEnemy import AbstractEnemy


class TankEnemy(AbstractEnemy):
    """
    Large and resistant enemy that moves slowly at the top of the screen.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.TANK_ENEMY_Y):
        """
        Initializes a tank enemy.

        :param x: Initial enemy x coordinate
        :param y: Initial enemy y coordinate (fixed at top)
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.TANK_ENEMY_MAX_HEALTH
        self._speed = Constants.TANK_ENEMY_SPEED
        self._update_sprite(self._speed)
        self.__time_since_last_shot = 0

    def _initialize_sprite(self, x, y):
        """
        Initializes the tank enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.original_image = pygame.image.load(
            "assets/sprites/enemies/TankEnemy.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (
            Constants.TANK_ENEMY_WIDTH, Constants.TANK_ENEMY_HEIGHT))
        self._original_image = self.original_image.copy()
        self.rect = self.original_image.get_rect(center=(x, y))

    def _move(self, dt, terrain=None):
        """
        Updates the tank enemy position.
        Moves only horizontally at the top of the screen.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        self.rect.x += self._speed * dt

        # Keep Y fixed at top
        self.rect.centery = Constants.TANK_ENEMY_Y

        # Reverse direction at edges e ajustar a orientação da imagem
        if self.rect.left <= 0:
            self.rect.left = 0
            self._speed = abs(self._speed)
        elif self.rect.right >= Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            self._speed = -abs(self._speed)

    def _attack(self, dt, target, enemies_projectiles):
        """
        Launches a bomb that falls vertically and explodes on impact.

        :param dt: Time since last update
        :param target: Target position (not used for bombs)
        :param enemies_projectiles: Group of enemy projectiles
        """
        self.__time_since_last_shot += dt

        if self.__time_since_last_shot >= Constants.TANK_ENEMY_SHOOT_FREQUENCY:
            self.__time_since_last_shot = 0

            bomb_image = pygame.image.load("assets/sprites/projectiles/TankEnemyProjectile.png").convert_alpha()
            bomb_image = pygame.transform.scale(bomb_image, (
            Constants.TANK_BOMB_WIDTH, Constants.TANK_BOMB_HEIGHT))

            # Create bomb with vertical velocity
            velocity = pygame.Vector2(0, Constants.TANK_BOMB_SPEED)
            bomb = BombProjectile(
                position=pygame.Vector2(self.rect.centerx, self.rect.bottom),
                velocity=velocity,
                image=bomb_image,
                damage=Constants.TANK_BOMB_DAMAGE,
                explosion_radius=Constants.TANK_BOMB_EXPLOSION_RADIUS
            )

            enemies_projectiles.add(bomb)

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary.
        """
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of TankEnemy from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._speed = data["speed"]
        return instance
