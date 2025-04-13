import pygame
from config.Constants import Constants
from src.entities.Ability import CriticalShot
from src.entities.players.AbstractPlayer import AbstractPlayer
import math


class Rain(AbstractPlayer):
    """
    Lieutenant Rain - Precision and survival specialist
    Basic attack: Precision rifle with very slow reload
    Special ability: Survival Mode (speed and reload buff)
    """

    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):
        super().__init__(x, y)
        old_center = self.rect.center

        self.sprite_idle = pygame.image.load(
            "assets/sprites/players/RainIdle.png").convert_alpha()
        self.sprite_idle = pygame.transform.scale(
            self.sprite_idle,
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        walk_sheet = pygame.image.load(
            "assets/sprites/players/RainWalk.png").convert_alpha()
        walk_sheet = pygame.transform.scale(
            walk_sheet, (Constants.PLAYER_WIDTH * 2, Constants.PLAYER_HEIGHT)
        )

        frame1 = walk_sheet.subsurface(
            (0, 0, Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)).copy()
        frame2 = walk_sheet.subsurface((Constants.PLAYER_WIDTH, 0,
                                        Constants.PLAYER_WIDTH,
                                        Constants.PLAYER_HEIGHT)).copy()
        self.sprite_walk_frames = [frame1, frame2]

        self.sprite_jump = pygame.image.load(
            "assets/sprites/players/RainJump.png").convert_alpha()
        self.sprite_jump = pygame.transform.scale(
            self.sprite_jump,
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        self.image = self.sprite_idle
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        self._charging_critical = 0
        self.time_projectile_generation = 0

        weapon_width = 70
        weapon_height = 70

        self.weapon_original = pygame.image.load(
            "assets/sprites/weapons/PrecisionRifle.png").convert_alpha()
        self.weapon_original = pygame.transform.scale(self.weapon_original, (
        weapon_width, weapon_height))

        self.special_weapon_original = pygame.image.load(
            "assets/sprites/weapons/SpecialPrecisionRifle.png").convert_alpha()
        self.special_weapon_original = pygame.transform.scale(
            self.special_weapon_original, (weapon_width, weapon_height))

        self.current_weapon_original = self.weapon_original.copy()
        self.weapon_image = self.current_weapon_original.copy()  # inicia sem rotação
        self.weapon_rect = self.weapon_image.get_rect(center=self.rect.center)

    def update(self, keys, terrain, dt, *args, **kwargs):
        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def update_weapon(self):
        if pygame.mouse.get_pressed()[2]:
            self.current_weapon_original = self.special_weapon_original.copy()
            offset_x, offset_y = 50, 0
        else:
            self.current_weapon_original = self.weapon_original.copy()
            offset_x, offset_y = 50, 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))
        self.weapon_angle = angle
        self.weapon_image = pygame.transform.rotate(
            self.current_weapon_original, angle)
        new_center = (
        self.rect.centerx + offset_x, self.rect.centery + offset_y)
        self.weapon_rect = self.weapon_image.get_rect(center=new_center)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.weapon_image, self.weapon_rect)

    def get_projectile_origin(self):
        return pygame.math.Vector2(self.weapon_rect.center)

    def get_player_color(self):
        return pygame.Color('darkgreen')

    def get_initial_health(self):
        return int(Constants.PLAYER_MAX_HEALTH * 0.9)

    def get_projectile_color(self):
        return pygame.Color('lime')

    def get_projectile_image(self):
        image = pygame.image.load(
            "assets/sprites/projectiles/PrecisionRifleProjectile.png").convert_alpha()
        return pygame.transform.scale(image, (15, 15))

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED * 2.0

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5

    def get_projectile_damage(self):
        return int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.8)

    def get_time_cooldown_ability(self):
        return int(self.time_cooldown_ability)

    def get_ready_ability(self):
        return self._ready_ability

    # TODO: probably remove ability parameter
    def choose_ability(self, ability_image):
        special_projectile_image = pygame.image.load(
            "assets/sprites/projectiles/SpecialPrecisionRifleProjectile.png").convert_alpha()
        special_projectile_image = pygame.transform.scale(
            special_projectile_image, (25, 25))
        return CriticalShot(
            self,
            Constants.ABILITY_SPEED * 3,
            special_projectile_image,
            Constants.ABILITY_DAMAGE
        )

    def _compute_cooldown_ability(self, dt):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:

            self.time_projectile_generation += dt
            if self.time_projectile_generation >= 1 / (
                    Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.1):
                self._charging_critical += 1
                if self._charging_critical <= Constants.NORMAL_SHOTS_REQUIRED:
                    self.time_cooldown_ability = self._charging_critical * Constants.ABILITY_COOLDOWN / Constants.NORMAL_SHOTS_REQUIRED
            if self._charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                self._ready_ability = True

    def _compute_duration_ability(self, dt):
        if pygame.mouse.get_pressed()[2]:
            self._ready_ability = False
            if self._charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                self._charging_critical = 0
                self.time_projectile_generation = 0
                self.time_cooldown_ability = 0

    # TODO: Implement special ability - Survival Mode (speed and reload buff)

    def to_dict(self):
        """
        Converts the player's state into a dictionary, including Rain-specific attributes.
        """
        data = super().to_dict()
        data["charging_critical"] = self._charging_critical
        data["time_projectile_geration"] = self.time_projectile_generation
        return data

    # TODO: Implement special ability - Survival Mode (speed and reload buff)
    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of Rain from a dictionary.
        """
        instance = cls()
        instance.rect.centerx = data["centerx"]
        instance.rect.bottom = data["bottom"]
        instance._health_points = data["health"]
        instance._is_jumping = data["is_jumping"]
        instance._y_speed = data["y_speed"]
        instance._ready_ability = data["ready_ability"]
        instance.time_cooldown_ability = data["time_cooldown_ability"]
        instance._time_duration_ability = data["time_duration_ability"]
        instance._charging_critical = data.get("charging_critical", 0)
        instance.time_projectile_generation = data.get(
            "time_projectile_geration", 0)
        return instance
