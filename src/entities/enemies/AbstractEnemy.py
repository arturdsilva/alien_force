import pygame
from config.Constants import Constants, Colors
from src.entities.Projectile import Projectile, ProjectileGenerator


class AbstractEnemy(pygame.sprite.Sprite):
    """
    Represents an enemy.
    """

    def __init__(self, x=0, y=Constants.HEIGHT / 10):
        """
        Initializes an enemy.

        :param x: The initial enemy x coordinate.
        :param y: The initial enemy y coordinate.
        """

        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(Colors.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._speed = 1 * Constants.ENEMY_SPEED
        self._health_points = None

    def update(self, dt, player_projectiles, enemies_projectiles, player):
        """
        Updates the enemy.

        :param dt: The duration of one iteration.
        :param player_projectiles: Player projectiles on screen.
        :param enemies_projectiles: Enemies projectiles on screen.
        :param player: The player to be targeted.
        """

        self._move(dt)
        self._limit_bounds()
        self._compute_damage(player_projectiles)

        if player:
            target = pygame.math.Vector2(player.sprite.rect.centerx,
                                         player.sprite.rect.centery)
            self._attack(dt, target, enemies_projectiles)

        if self.is_dead():
            self.kill()

    def _move(self, dt):
        """
        Updates the enemy position.

        :param dt: The duration of one iteration.
        """

        self.rect.x += self._speed * dt
        if self._limit_bounds():
            self._speed = -self._speed

    def _limit_bounds(self):
        """
        Limits enemy position to inside screen boundaries.
        """

        out_of_bounds = False
        if self.rect.left < 0:
            self.rect.left = 0
            out_of_bounds = True
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            out_of_bounds = True
        if self.rect.top < 0:
            self.rect.top = 0
            out_of_bounds = True
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
            out_of_bounds = True

        return out_of_bounds

    def _compute_damage(self, player_projectiles):
        """
        Computes projectile collision and damage taken.

        :param player_projectiles: Player projectiles on scree.
        """

        for projectile in player_projectiles:
            if pygame.sprite.collide_rect(self, projectile):
                self._health_points -= projectile.damage
                projectile.kill()

    def is_dead(self):
        """
        If enemy is out of health points.
        """

        return self._health_points <= 0

    def _attack(self, dt, target, projectiles):
        raise NotImplementedError("Attack method not implemented")
