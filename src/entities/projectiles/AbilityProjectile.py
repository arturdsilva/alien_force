import numpy as np
import pygame

from .AbstractProjectile import AbstractProjectile


class ProjectileAbility(AbstractProjectile):
    """
    Base class for projectile-based abilities that move along a trajectory
    """

    def __init__(self, position, angle, velocity, image, damage,
                 lifetime=None):
        """
        Initializes a projectile ability

        :param position: position of the projectile
        :param angle: angle in radians (0 to 2pi)
        :param velocity: velocity vector of the projectile
        :param image: image of the projectile
        :param damage: damage caused by the projectile
        :param lifetime: lifetime in seconds (None for unlimited)
        """
        super().__init__(position, velocity, image, damage)
        self.__initialize_sprite(position, angle, image)
        self.__time_alive = 0
        self.__lifetime = lifetime

    def update(self, dt, terrain=None, player=None):
        """
        Update the projectile behavior (lifetime)

        :param dt: Duration of one iteration
        """
        if self.__lifetime is not None:
            self.__time_alive += dt
        if self.__time_alive >= self.__lifetime:
            self.kill()
            return
        if hasattr(self.image, "set_alpha"):
            alpha = int(255 * (1 - self.__time_alive / self.__lifetime))
            self.image.set_alpha(alpha)
        self._move(dt)

    def __initialize_sprite(self, position, angle, image):
        """
        Initialize the sprite for the projectile

        :param position: Position of the projectile
        :param angle: Angle in radians
        :param image: Image of the projectile
        """
        self._image = image
        self._original_image = image
        self._angle = np.degrees(angle)
        self.image = pygame.transform.rotate(self._image, self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def draw(self, screen):
        """
        Draws the projectile on screen.
        Abstract method that must be implemented by child classes.

        :param screen: Screen surface
        """
        pass
