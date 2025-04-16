import random

import pygame

from config.Constants import Constants, Sounds
from src.entities.enemies.AbstractEnemy import AbstractEnemy
from src.utils.AudioManager import AudioManager


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
        self._speed = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED
        self._update_sprite(self._speed)
        self.__state = self.MOVING
        self.__timer = 0
        self.__wait_timer = 0
        self.__fall_time = random.uniform(
            Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
            Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
        )
        self.__original_y = y
        self.__audio_manager = AudioManager()

    def _initialize_sprite(self, x, y):
        """
        Initializes the enemy sprite.

        :param x: Initial x coordinate
        :param y: Initial y coordinate
        """
        self.original_image = pygame.image.load(
            "assets/sprites/enemies/BouncingEnemy.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (
            Constants.BOUNCING_ENEMY_WIDTH, Constants.BOUNCING_ENEMY_HEIGHT))
        self.rect = self.original_image.get_rect(center=(x, y))

    def _move(self, dt, terrain=None):
        """
        Updates enemy position based on current state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group
        """
        if self.__state == self.MOVING:
            # Constant horizontal movement
            self.rect.x += self._speed * dt

            # Reverse direction at edges
        if self.rect.left <= 0:
            self.rect.left = 0
            self._speed = Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED
        elif self.rect.right >= Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            self._speed = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED


        elif self.__state == self.FALLING:
            # Fast falling movement
            self.rect.y += Constants.BOUNCING_ENEMY_FALL_SPEED * dt

            # Check terrain collision
            if terrain:
                hits = pygame.sprite.spritecollide(self, terrain, False)
                if hits:
                    self.__audio_manager.play_sound(Sounds.STOMP)
                    self.rect.bottom = hits[0].rect.top
                    self.__state = self.WAITING
                    self.__timer = 0
                    return

        elif self.__state == self.RISING:
            # Slow rising movement
            self.rect.y -= Constants.BOUNCING_ENEMY_RISE_SPEED * dt
            if self.rect.centery <= self.__original_y:
                # Only change state, don't force Y position
                self.__state = self.MOVING
                self.__timer = 0
                self.__fall_time = random.uniform(
                    Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
                    Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
                )
        self.__update_behavior(dt)

    def __update_behavior(self, dt):
        """
        Updates enemy state and timers.

        :param dt: Time since last update
        """
        if self.__state == self.MOVING:
            self.__timer += dt
            if self.__timer >= self.__fall_time:
                self.__state = self.PREPARING
                self.__timer = 0

        elif self.__state == self.PREPARING:
            self.__timer += dt
            if self.__timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self.__state = self.FALLING
                self.__timer = 0

        elif self.__state == self.FALLING:
            # Terrain collision check is in _move method
            pass

        elif self.__state == self.WAITING:
            self.__timer += dt
            if self.__timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self.__state = self.RISING
                self.__timer = 0

    def _attack(self, dt, target, enemies_projectiles):
        # Checks for collision during fall
        if (self.__state == self.FALLING and target and
                pygame.sprite.collide_rect( self, target.sprite)):
            target.sprite.inflict_damage(Constants.BOUNCING_ENEMY_FALL_DAMAGE)

    def update(self, dt, player_projectiles, ability_projectiles,
               enemies_projectiles, player,
               terrain=None, speed_multiplier=1.0):
        """
        Updates enemy state and position.

        :param dt: Time since last update
        :param player_projectiles: Player projectiles on screen
        :param ability_projectiles: Player abilities on screen
        :param enemies_projectiles: Enemies projectiles on screen
        :param player: Player sprite
        :param terrain: Terrain sprite group
        :param speed_multiplier: Speed multiplier for game difficulty
        """
        self._move(dt, terrain)
        self.__update_behavior(dt)
        self._compute_damage(player_projectiles, ability_projectiles)
        self._update_sprite(self._speed)
        self._attack(dt, player, enemies_projectiles)

    def to_dict(self):
        """
        Converts the enemy's state into a dictionary, including BouncingEnemy-specific attributes.
        """
        data = super().to_dict()
        data["velocity_x"] = self._speed
        data["state"] = self.__state
        data["timer"] = self.__timer
        data["wait_timer"] = self.__wait_timer
        data["fall_time"] = self.__fall_time
        data["original_y"] = self.__original_y
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of BouncingEnemy from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._speed = data["speed"]
        instance._speed = data.get("velocity_x",
                                   -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED)
        instance.__state = data.get("state", cls.MOVING)
        instance.__timer = data.get("timer", 0)
        instance.__wait_timer = data.get("wait_timer", 0)
        instance.__fall_time = data.get("fall_time", random.uniform(
            Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
            Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL))
        instance.__original_y = data.get("original_y", instance.rect.centery)
        return instance

