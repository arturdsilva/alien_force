import random

import pygame

from config.Constants import Constants, Colors
from src.entities.enemies.AbstractEnemy import AbstractEnemy


class BouncingEnemy(AbstractEnemy):
    """
    Enemy that moves horizontally and occasionally drops quickly,
    rising slowly afterward.
    """

    # Enemy states
    MOVING = 'moving'  # Moving horizontally
    PREPARING = 'preparing'  # Preparing to drop
    FALLING = 'falling'  # Falling
    WAITING = 'waiting'  # Waiting after falling/rising
    RISING = 'rising'  # Rising

    def __init__(self, x=Constants.WIDTH,
                 y=Constants.BOUNCING_ENEMY_BASE_HEIGHT):
        """
        Initializes an enemy that alternates between horizontal and vertical movement.

        :param x: Initial enemy x coordinate
        :param y: Initial enemy y coordinate
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.BOUNCING_ENEMY_MAX_HEALTH
        self._velocity_x = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED  # Starts moving left
        self._state = self.MOVING
        self._timer = 0
        self._wait_timer = 0
        self._fall_time = random.uniform(
            Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
            Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
        )
        self._original_y = y

    def _initialize_sprite(self, x, y):
        """
        Initializes the enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.image = pygame.Surface((Constants.BOUNCING_ENEMY_WIDTH,
                                     Constants.BOUNCING_ENEMY_HEIGHT))
        self.image.fill(Colors.ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def _move(self, dt, terrain=None):
        """
        Updates enemy position based on current state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group
        """
        if self._state == self.MOVING:
            # Constant horizontal movement
            self.rect.x += self._velocity_x * dt

            # Reverse direction at edges
            if self.rect.left <= 0:
                self.rect.left = 0
                self._velocity_x = Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED
            elif self.rect.right >= Constants.WIDTH:
                self.rect.right = Constants.WIDTH
                self._velocity_x = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED

        elif self._state == self.FALLING:
            # Fast falling movement
            self.rect.y += Constants.BOUNCING_ENEMY_FALL_SPEED * dt

            # Check terrain collision
            if terrain:
                hits = pygame.sprite.spritecollide(self, terrain, False)
                if hits:
                    self.rect.bottom = hits[0].rect.top
                    self._state = self.WAITING
                    self._timer = 0
                    return

        elif self._state == self.RISING:
            # Slow rising movement
            self.rect.y -= Constants.BOUNCING_ENEMY_RISE_SPEED * dt
            if self.rect.centery <= self._original_y:
                # Only change state, don't force Y position
                self._state = self.MOVING
                self._timer = 0
                self._fall_time = random.uniform(
                    Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
                    Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
                )

    def _update_behavior(self, dt, terrain=None):
        """
        Updates enemy state and timers.

        :param dt: Time since last update
        :param terrain: Terrain sprite group
        """
        if self._state == self.MOVING:
            self._timer += dt
            if self._timer >= self._fall_time:
                self._state = self.PREPARING
                self._timer = 0

        elif self._state == self.PREPARING:
            self._timer += dt
            if self._timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self._state = self.FALLING
                self._timer = 0

        elif self._state == self.FALLING:
            # Terrain collision check is in _move method
            pass

        elif self._state == self.WAITING:
            self._timer += dt
            if self._timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self._state = self.RISING
                self._timer = 0

    def _attack(self, dt, target, enemies_projectiles):
        pass

    def _compute_damage(self, player_projectiles):
        """
        Computes projectile collision and damage taken.

        :param player_projectiles: Player projectiles on screen.
        """
        for projectile in player_projectiles:
            if pygame.sprite.collide_rect(self, projectile):
                self._health_points -= projectile.damage
                projectile.kill()

    def update(self, dt, player_projectiles, enemies_projectiles, player, terrain):
        """
        Updates enemy state and position.

        :param dt: Time since last update
        :param player_projectiles: Player projectiles on screen
        :param enemies_projectiles: Enemies projectiles on screen.
        :param player: Player sprite
        :param terrain: Terrain sprite group
        """
        self._move(dt, terrain)
        self._update_behavior(dt, terrain)
        self._compute_damage(player_projectiles)
        self._attack(dt, player, enemies_projectiles)
        
        # Verifica colisão com o player durante a queda
        if self._state == self.FALLING and player and pygame.sprite.collide_rect(self, player.sprite):
            player.sprite._health_points -= Constants.BOUNCING_ENEMY_FALL_DAMAGE

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary, including BouncingEnemy-specific attributes.
        """
        data = super().to_dict()
        data["velocity_x"] = self._velocity_x
        data["state"] = self._state
        data["timer"] = self._timer
        data["wait_timer"] = self._wait_timer
        data["fall_time"] = self._fall_time
        data["original_y"] = self._original_y
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of BouncingEnemy from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._speed = data["speed"]
        instance._velocity_x = data.get("velocity_x",
                                        -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED)
        instance._state = data.get("state", cls.MOVING)
        instance._timer = data.get("timer", 0)
        instance._wait_timer = data.get("wait_timer", 0)
        instance._fall_time = data.get("fall_time", random.uniform(
            Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
            Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL))
        instance._original_y = data.get("original_y", instance.rect.centery)
        return instance

