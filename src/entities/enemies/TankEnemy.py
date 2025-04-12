import pygame

from config.Constants import Constants, Colors
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

    def _initialize_sprite(self, x, y):
        """
        Initializes the tank enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.image = pygame.image.load("assets/sprites/enemies/TankEnemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (
        Constants.TANK_ENEMY_WIDTH, Constants.TANK_ENEMY_HEIGHT))
        self._original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))

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
            # Para mover à direita, usa a imagem original
            self.image = self._original_image
        elif self.rect.right >= Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            self._speed = -abs(self._speed)
            # Para mover à esquerda, inverte horizontalmente a imagem original
            self.image = pygame.transform.flip(self._original_image, True,
                                               False)

    def _update_behavior(self, dt, terrain=None):
        """
        Updates specific tank enemy behaviors.
        In this case, there are no additional behaviors to update.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        pass

    def _attack(self, dt, target, enemies_projectiles):
        pass