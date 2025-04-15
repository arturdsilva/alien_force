import pygame
from config.Constants import Constants, Sounds
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.Ability import LaserBeam
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator
import math

class Cyborg(AbstractPlayer):
    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):

        super().__init__(x, y)
        self._initial_health = Constants.PLAYER_MAX_HEALTH
        self._health_points = self._initial_health
        self._ability_cooldown = Constants.LASER_COOLDOWN
        self._ability_duration = Constants.LASER_DURATION
        self._ability_time_left = Constants.LASER_DURATION
        self._has_durable_ability = True

        projectile_image = pygame.image.load(
            "assets/sprites/projectiles/AssaultRifleProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (10, 10))
        projectile_speed = Constants.PROJECTILE_DEFAULT_SPEED * 1.5
        projectile_frequency = Constants.PROJECTILE_DEFAULT_FREQUENCY * 1.5
        projectile_damage = int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.2)
        projectile_sound = Sounds.GUN_SHOT

        self._projectile_generator = ProjectileGenerator(self,
                                                         projectile_speed,
                                                         projectile_frequency,
                                                         projectile_image,
                                                         projectile_damage,
                                                         projectile_sound,
                                                         is_player_projectile=True
                                                         )

        self._sprite_idle = pygame.image.load(
            "assets/sprites/players/CyborgIdle.png").convert_alpha()
        self._sprite_idle = pygame.transform.scale(
            self._sprite_idle, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )


        walk_sheet = pygame.image.load(
            "assets/sprites/players/CyborgWalk.png").convert_alpha()
        sheet_width, sheet_height = walk_sheet.get_size()
        frame_width = sheet_width // 2
        frame_height = sheet_height
        frame1 = walk_sheet.subsurface((0, 0, frame_width, frame_height)).copy()
        frame2 = walk_sheet.subsurface((frame_width, 0, frame_width, frame_height)).copy()
        frame1 = pygame.transform.scale(frame1, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        frame2 = pygame.transform.scale(frame2, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        self._sprite_walk_frames = [frame1, frame2]


        self._sprite_jump = pygame.image.load(
            "assets/sprites/players/CyborgJump.png").convert_alpha()
        self._sprite_jump = pygame.transform.scale(
            self._sprite_jump, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        self.image = self._sprite_idle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        weapon_width = 100
        weapon_height = 100

        self.weapon_original = pygame.image.load("assets/sprites/weapons/AssaultRifle.png").convert_alpha()
        self.weapon_original = pygame.transform.scale(self.weapon_original, (
        weapon_width, weapon_height))

        self.plasma_weapon_original = pygame.image.load("assets/sprites/weapons/PlasmaCannon.png").convert_alpha()
        self.plasma_weapon_original = pygame.transform.scale(
            self.plasma_weapon_original, (weapon_width, weapon_height))

        self.current_weapon_original = self.weapon_original.copy()
        self.weapon_image = self.current_weapon_original.copy()  # inicia sem rotação
        self.weapon_rect = self.weapon_image.get_rect(center=self.rect.center)
        self._special_weapon_offset = pygame.Vector2(20, -10)

    def update(self, keys, terrain, dt, *args, **kwargs):
        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def update_weapon(self):
        if pygame.mouse.get_pressed()[2]:
            self.current_weapon_original = self.plasma_weapon_original.copy()
            offset_x = 50 + self._special_weapon_offset.x
            offset_y = 0 + self._special_weapon_offset.y
        else:
            self.current_weapon_original = self.weapon_original.copy()
            offset_x, offset_y = 50, 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

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

    def get_ability_cooldown(self):
        return self._ability_cooldown

    def get_ability_downtime(self):
        return self._ability_downtime

    def get_ability_duration(self):
        return self._ability_duration

    def get_ability_time_left(self):
        return self._ability_time_left

    def get_ready_ability(self):
        return self._ready_ability

    def choose_ability(self):
        return LaserBeam(self)

    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """
        if not self._ready_ability:
            self._ability_downtime += dt
            if self._ability_downtime >= self._ability_cooldown:
                self._ability_time_left = self._ability_duration
                self._ready_ability = True

    def _compute_duration_ability(self, dt):
        """
        Updates the duration logic for the character's ability based on character type.

        :param dt: The duration of one iteration.
        """
        if pygame.mouse.get_pressed()[2] and self._ready_ability:
            self._ability_time_left -= dt
            if self._ability_time_left <= 0:
                self._ability_time_left = 0
                self._ready_ability = False

    def to_dict(self):
        """
        Utilizes the method from the abstract class to obtain common data.
        Add any specific attributes of Cyborg to the dictionary if necessary.
        """
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of Cyborg from a dictionary.
        """
        instance = cls(data["centerx"], data["bottom"])
        instance._health_points = data["health"]
        instance._is_jumping = data["is_jumping"]
        instance._y_speed = data["y_speed"]
        instance._ready_ability = data["ready_ability"]
        instance._ability_downtime = data["time_cooldown_ability"]
        instance._time_duration_ability = data["time_duration_ability"]
        return instance
