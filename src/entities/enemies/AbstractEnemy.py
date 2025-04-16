from abc import ABC, abstractmethod

from config.Constants import Constants
import pygame


class AbstractEnemy(pygame.sprite.Sprite, ABC):
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
        self.original_image = None
        self.image = None
        self.rect = None
        self._speed = Constants.ENEMY_SPEED
        self._health_points = None
        self._initialize_sprite(x, y)

    @abstractmethod
    def _initialize_sprite(self, x, y):
        pass

    def update(self, dt, player_projectiles, ability_projectiles,
               enemies_projectiles, player,
               terrain=None, speed_multiplier=1.0):
        """
        Updates the enemy state.

        :param ability_projectiles: projectiles originated from abilities
        :param dt: Time since last update
        :param player_projectiles: Player projectiles on screen
        :param enemies_projectiles: Enemies projectiles on screen.
        :param player: The player to be targeted.
        :param terrain: Terrain sprite group (optional)
        :param speed_multiplier: increases the enemy speed.
        """
        dt *= speed_multiplier

        self._move(dt, terrain)
        self._limit_bounds()
        self._compute_damage(player_projectiles, ability_projectiles)
        self._update_sprite(self._speed)

        if player:
            target = pygame.math.Vector2(player.sprite.rect.centerx,
                                         player.sprite.rect.centery)
            self._attack(dt, target, enemies_projectiles)


    @abstractmethod
    def _move(self, dt, terrain=None):
        """
        Abstract method to define enemy movement.
        Must be implemented by each child class.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        """

        pass

    def _update_sprite(self, velocity_x):
        if velocity_x > 0:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)

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

    def _compute_damage(self, player_projectiles, ability_projectiles):
        """
        Computes projectile collision and damage taken.

        :param player_projectiles: Player projectiles on screen.
        """

        for projectile in player_projectiles:
            if pygame.sprite.collide_rect(self, projectile):
                self._health_points -= projectile.damage
                projectile.kill()

        for ability in ability_projectiles:
            if hasattr(ability, 'radius'):
                distance = pygame.math.Vector2(
                    ability.rect.centerx - self.rect.centerx,
                    ability.rect.centery - self.rect.centery
                ).length()

                if distance <= ability.radius:
                    distance_factor = 1 - (distance / ability.radius)
                    actual_damage = ability.damage * distance_factor
                    self._health_points -= actual_damage

            elif pygame.sprite.collide_rect(self, ability):
                self._health_points -= ability.damage

                if hasattr(ability,
                           'create_explosion') and not ability.has_exploded:
                    ability.create_explosion(ability, ability_projectiles)
                elif hasattr(ability,
                             'create_hit_effect') and not ability.has_hit:
                    ability.create_hit_effect(ability, ability_projectiles)

                ability.kill()

    @abstractmethod
    def _attack(self, dt, target, projectiles):
        pass

    @property
    def health(self):
        """
        Returns the current enemy health.

        :return: Current health points
        """
        return self._health_points

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary.
        """
        return {
            "type": self.__class__.__name__,
            "centerx": self.rect.centerx,
            "bottom": self.rect.bottom,
            "health": self._health_points,
            "speed": self._speed,
        }
