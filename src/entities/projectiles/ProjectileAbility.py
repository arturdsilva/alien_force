import pygame
import numpy as np
from .BaseProjectile import BaseProjectile

class ProjectileAbility(BaseProjectile):
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
        self._position = position
        self._velocity = velocity
        self._lifetime = lifetime
        self._initialize_sprite(position, angle, image)
        self._time_alive = 0
        self.__lifetime = lifetime

    def update(self, dt, terrain=None, player=None):
        """
        Update the projectile behavior (lifetime)

        :param dt: Duration of one iteration
        """
        if self.__lifetime is not None:
            self._time_alive += dt
        if self._time_alive >= self.__lifetime:
            self.kill()
            return
        if hasattr(self.image, "set_alpha"):
            alpha = int(255 * (1 - self._time_alive / self.__lifetime))
            self.image.set_alpha(alpha)
        self._move(dt)

    def _move(self, dt):
        """
        Move the projectile along its trajectory

        :param dt: Duration of one iteration
        """
        self._position += self._velocity * dt
        self.rect.center = self._position

    def _initialize_sprite(self, position, angle, image):
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