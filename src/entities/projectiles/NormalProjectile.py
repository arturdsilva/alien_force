import pygame

from .AbstractProjectile import AbstractProjectile


class NormalProjectile(AbstractProjectile):
    """
    Normal projectile that moves in a straight line and causes damage upon hitting the target.
    """

    def __init__(self, position, velocity, image, damage):
        """
        Initializes a normal projectile.

        :param position: Initial position of the projectile
        :param velocity: Velocity vector of the projectile
        :param image: Projectile image
        :param damage: Damage caused by the projectile
        """
        super().__init__(position, velocity, image, damage)

    def update(self, dt, terrain=None, player=None):
        """
        Updates the projectile state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        :param player: Player sprite (optional)
        """
        # Update projectile position
        self._move(dt)
        self._handle_bounds()

        # Check terrain collision
        if terrain:
            hits = pygame.sprite.spritecollide(self, terrain, False)
            if hits:
                self.kill()

    def draw(self, screen):
        """
        Draws the projectile on screen.

        :param screen: Screen surface
        """
        screen.blit(self.image, self.rect)
