from abc import ABC, abstractmethod

from config.Constants import Constants, Sounds
from src.utils.AudioManager import AudioManager
import pygame


class AbstractPlayer(pygame.sprite.Sprite, ABC):
    """
    Represents an abstract player.
    """

    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):
        """
        Initializes a player.

        :param x: The initial player x coordinate.
        :param y: The initial player y coordinate.
        """

        super().__init__()
        self._is_jumping = False
        self._y_speed = 0
        self._initial_health = 0
        self._health_points = 0
        self._ready_ability = True
        self._time_cooldown_ability = Constants.ABILITY_COOLDOWN
        self._time_duration_ability = 0
        self._prev_mouse_pressed = False
        self._audio_manager = AudioManager()
        self.walk_frame_index = 0
        self.walk_frame_timer = 0
        self.walk_frame_duration = 0.3
        self._facing_left = False
        self._sprite_idle = None
        self._sprite_jump = None
        self._sprite_walk_frames = None
        self._projectile_generator = None
        self.ability_generator = self.choose_ability()
        self._special_weapon_offset = pygame.Vector2(0, 0)

    @abstractmethod
    def get_time_cooldown_ability(self):
        """
        Returns the time cooldown ability of the player.
        """

        pass

    def get_initial_health(self):
        return self._initial_health

    @abstractmethod
    def get_ready_ability(self):
        """
        Returns the ready ability of the player.
        """

        pass

    @abstractmethod
    def choose_ability(self):
        """
        Returns the correct skill to the player.
        """

        pass

    @abstractmethod
    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """

        pass

    @abstractmethod
    def _compute_duration_ability(self, dt):
        """
        Updates the duration logic for the character's ability based on character type.

        :param dt: The duration of one iteration.
        """

    pass

    def update(self, keys, terrain, dt, player_projectiles,
               enemies_projectiles, abilities):
        self._handle_input(terrain, keys, dt, player_projectiles, abilities)
        self._limit_bounds()
        self._compute_damage(enemies_projectiles)

        if self._is_jumping:
            self.image = self._sprite_jump
        elif keys[pygame.K_a] or keys[pygame.K_d]:
            self.walk_frame_timer += dt
            if self.walk_frame_timer >= self.walk_frame_duration:
                self.walk_frame_timer = 0
                self.walk_frame_index = (self.walk_frame_index + 1) % len(
                    self._sprite_walk_frames)
            self.image = self._sprite_walk_frames[
                self.walk_frame_index]
        else:
            self.image = self._sprite_idle

        if self._facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

        if self._health_points <= 0:
            self.kill()

    def _handle_input(self, terrain, keys, dt, projectiles, abilities):
        self._compute_vertical_position(terrain, keys, dt)
        self._compute_horizontal_position(terrain, keys, dt)

        if (pygame.mouse.get_pressed()[0] and not
        (pygame.mouse.get_pressed()[2] and self._ready_ability)):
            target = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                         pygame.mouse.get_pos()[1])
            origin = (
                self.get_projectile_origin()
                if hasattr(self, "get_projectile_origin")
                else pygame.math.Vector2(self.rect.center)
            )
            self._projectile_generator.generate(origin, target, dt,
                                                projectiles)
        self._compute_cooldown_ability(dt)

        if pygame.mouse.get_pressed()[2]:
            target_ability = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                                 pygame.mouse.get_pos()[1])
            if self._ready_ability:
                self.ability_generator.generate(target_ability, dt, abilities)
        self._compute_duration_ability(dt)

        if keys[pygame.K_a]:
            self._facing_left = True
        elif keys[pygame.K_d]:
            self._facing_left = False

    def _compute_vertical_position(self, terrain, keys, dt):
        """
        Computes player's vertical position.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        """

        if (keys[pygame.K_w] or keys[
            pygame.K_SPACE]) and not self._is_jumping:
            self._y_speed = -Constants.JUMP_SPEED
            self._is_jumping = True

        self._y_speed += + Constants.GRAVITY * dt
        self.rect.y += self._y_speed * dt

        hits = pygame.sprite.spritecollide(self, terrain, False)
        for block in hits:
            self.rect.bottom = block.rect.y
            self._is_jumping = False
            self._y_speed = 0

    def _compute_horizontal_position(self, terrain, keys, dt):
        """
        Computes player's horizontal position.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        """

        if keys[pygame.K_a]:
            self.rect.x -= Constants.PLAYER_SPEED * dt

        if keys[pygame.K_d]:
            self.rect.x += Constants.PLAYER_SPEED * dt

        hits = pygame.sprite.spritecollide(self, terrain, False)
        for block in hits:
            if keys[pygame.K_a]:
                self.rect.x = block.rect.right
            if keys[pygame.K_d]:
                self.rect.right = block.rect.x

    def _limit_bounds(self):
        """
        Limits player position to inside screen boundaries.
        """

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT

    def _compute_damage(self, enemies_projectiles):
        """
        Computes projectile collision and damage taken.
        :param enemies_projectiles: Enemies projectiles on screen.
        """
        for projectile in enemies_projectiles:
            projectile.compute_collision(self)

    def inflict_damage(self, damage):
        """
        inflicts damage on the player

        :param damage: The damage to be inflicted on the player.
        """
        self._health_points -= damage
        self._audio_manager.play_sound(Sounds.HIT)

    def to_dict(self):
        """
        Converts the player's state into a dictionary.
        """
        return {
            "type": self.__class__.__name__,
            "centerx": self.rect.centerx,
            "bottom": self.rect.bottom,
            "health": self._health_points,
            "is_jumping": self._is_jumping,
            "y_speed": self._y_speed,
            "ready_ability": self._ready_ability,
            "time_cooldown_ability": self._time_cooldown_ability,
            "time_duration_ability": self._time_duration_ability
        }
