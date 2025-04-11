import pygame
from abc import ABC, abstractmethod
from config.Constants import Constants


class BaseProjectile(pygame.sprite.Sprite, ABC):
    """
    Abstract base class for all projectile types.
    Defines the common interface that all projectiles must implement.
    """
    
    def __init__(self, position, velocity, image, damage):
        """
        Initializes a base projectile.

        :param position: Initial position of the projectile
        :param velocity: Velocity vector of the projectile
        :param image: Projectile image
        :param damage: Damage caused by the projectile
        """
        super().__init__()
        self._position = position
        self._velocity = velocity
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self._damage = damage

    @abstractmethod
    def update(self, dt, terrain=None, player=None):
        """
        Updates the projectile state.
        Abstract method that must be implemented by child classes.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        :param player: Player sprite (optional)
        """
        pass

    def _handle_bounds(self):
        """
        Removes projectiles that go out of screen bounds.
        """
        if (self.rect.right < 0 or
                self.rect.left > Constants.WIDTH or
                self.rect.bottom < 0 or self.rect.top > Constants.HEIGHT):
            self.kill()

    @abstractmethod
    def draw(self, screen):
        """
        Draws the projectile on screen.
        Abstract method that must be implemented by child classes.

        :param screen: Screen surface
        """
        pass

    @property
    def damage(self):
        """
        Returns the damage caused by the projectile.
        """
        return self._damage 