from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
from entities.projectiles.BombProjectile import BombProjectile
import pygame


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
        self._time_since_last_shot = 0

    def _initialize_sprite(self, x, y):
        """
        Initializes the tank enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.image = pygame.Surface((Constants.TANK_ENEMY_WIDTH,
                                   Constants.TANK_ENEMY_HEIGHT))
        self.image.fill(Colors.PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

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
        
        # Reverse direction at edges
        if self.rect.left <= 0:
            self.rect.left = 0
            self._speed = abs(self._speed)
        elif self.rect.right >= Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            self._speed = -abs(self._speed)

    def _update_behavior(self, dt, terrain=None):
        """
        Updates specific tank enemy behaviors.
        In this case, there are no additional behaviors to update.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (not used by this enemy)
        """
        pass

    def _attack(self, dt, target, enemies_projectiles):
        """
        Launches a bomb that falls vertically and explodes on impact.

        :param dt: Time since last update
        :param target: Target position (not used for bombs)
        :param enemies_projectiles: Group of enemy projectiles
        """
        self._time_since_last_shot += dt
        
        if self._time_since_last_shot >= Constants.TANK_ENEMY_SHOOT_FREQUENCY:
            self._time_since_last_shot = 0
            
            # Create bomb image
            bomb_image = pygame.Surface((Constants.TANK_BOMB_WIDTH, Constants.TANK_BOMB_HEIGHT))
            bomb_image.fill(Colors.PURPLE)
            
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
