from abc import ABC, abstractmethod

from config.Constants import Constants, Colors
from entities.projectiles.ProjectileGenerator import ProjectileGenerator
from entities.projectiles.BaseProjectile import BaseProjectile
from src.entities.Ability import MissileBarrage
from src.entities.Ability import LaserBeam
from src.entities.Ability import CriticalShot
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
        self.image = pygame.Surface(
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        self.image.fill(self.get_player_color())
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._is_jumping = False
        self._y_speed = 0
        self._health_points = self.get_initial_health()
        self._ready_ability = True
        self.time_cooldown_ability = 0
        self._time_duration_ability = 0
        self._prev_mouse_pressed = False
        self.walk_frame_index = 0
        self.walk_frame_timer = 0
        self.walk_frame_duration = 0.3
        self._facing_left = False

        if hasattr(self, "get_projectile_image"):
            projectile_image = self.get_projectile_image()
        else:
            projectile_image = pygame.Surface((
                Constants.PROJECTILE_DEFAULT_WIDTH,
                Constants.PROJECTILE_DEFAULT_HEIGHT))
            projectile_image.fill(Constants.PROJECTILE_DEFAULT_COLOR)
        self.projectile_generator = ProjectileGenerator(self,
                                                        self.get_projectile_speed(),
                                                        self.get_projectile_frequency(),
                                                        projectile_image,
                                                        self.get_projectile_damage(),
                                                        is_player_projectile=True)

        ability_image = pygame.Surface(
            (Constants.ABILITY_WIDTH, Constants.ABILITY_HEIGHT)
        )
        ability_image.fill(Constants.ABILITY_DEFAULT_COLOR)
        self.ability_generator = self.choose_ability(ability_image)

    @abstractmethod
    def get_player_color(self):
        """
        Returns the color of the player.
        """

        pass

    @abstractmethod
    def get_initial_health(self):
        """
        Returns the initial health of the player.
        """

        pass

    @abstractmethod
    def get_projectile_color(self):
        """
        Returns the color of the projectiles.
        """

        pass

    @abstractmethod
    def get_projectile_speed(self):
        """
        Returns the speed of the projectiles.
        """

        pass

    @abstractmethod
    def get_projectile_frequency(self):
        """
        Returns the frequency of the projectiles.
        """

        pass

    @abstractmethod
    def get_projectile_damage(self):
        """
        Returns the damage of the projectiles.
        """

        pass

    @abstractmethod
    def get_time_cooldown_ability(self):
        """
        Returns the time cooldown ability of the player.
        """

        pass

    @abstractmethod
    def get_ready_ability(self):
        """
        Returns the ready ability of the player.
        """

        pass

    @abstractmethod
    def choose_ability(self, ability_image):
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
            try:
                self.image = self.sprite_jump
            except AttributeError:
                pass
        elif keys[pygame.K_a] or keys[pygame.K_d]:
            try:
                if hasattr(self, 'sprite_walk_frames'):
                    self.walk_frame_timer += dt
                    if self.walk_frame_timer >= self.walk_frame_duration:
                        self.walk_frame_timer = 0
                        self.walk_frame_index = (
                                                        self.walk_frame_index + 1) % len(
                            self.sprite_walk_frames)
                    self.image = self.sprite_walk_frames[
                        self.walk_frame_index]
                else:
                    self.image = self.sprite_walk
            except AttributeError:
                pass
        else:
            try:
                self.image = self.sprite_idle
            except AttributeError:
                pass

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
            self.projectile_generator.generate(origin, target, dt,
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
            if pygame.sprite.collide_rect(self, projectile):
                # Bomb only causes collision damage if it hasn't exploded yet.
                if hasattr(projectile, '_exploded'):
                    if not projectile._exploded:
                        self._health_points -= projectile.damage
                        projectile._explode(None, self)
                else:
                    self._health_points -= projectile.damage
                    projectile.kill()

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
            "time_cooldown_ability": self.time_cooldown_ability,
            "time_duration_ability": self._time_duration_ability
        }
