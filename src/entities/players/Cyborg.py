import pygame
from config.Constants import Constants, Sounds
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator
from src.entities.abilities.LaserBeam import LaserBeam

class Cyborg(AbstractPlayer):
    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):

        super().__init__(x, y)
        self._initial_health = Constants.PLAYER_MAX_HEALTH
        self._health_points = self._initial_health
        self._ability_cooldown = Constants.LASER_COOLDOWN
        self._time_duration_ability = Constants.LASER_DURATION
        self._ability_time_left = Constants.LASER_DURATION
        self._has_durable_ability = True

        projectile_image = pygame.image.load(
            "assets/sprites/projectiles/AssaultRifleProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (10, 10))
        projectile_speed = Constants.PROJECTILE_DEFAULT_SPEED * 1.5
        projectile_frequency = Constants.PROJECTILE_DEFAULT_FREQUENCY * 1.5
        projectile_damage = int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.2)
        projectile_sound = Sounds.GUN_SHOT

        self._projectile_generator = ProjectileGenerator(projectile_speed,
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

        self._weapon_original_image = pygame.image.load(
            "assets/sprites/weapons/AssaultRifle.png").convert_alpha()
        self._weapon_original_image = pygame.transform.scale(
            self._weapon_original_image, (
                weapon_width, weapon_height))

        self._special_weapon_original_image = pygame.image.load(
            "assets/sprites/weapons/PlasmaCannon.png").convert_alpha()
        self._special_weapon_original_image = pygame.transform.scale(
            self._special_weapon_original_image, (weapon_width, weapon_height))

        self._current_weapon_original_image = self._weapon_original_image.copy()
        self._weapon_image = self._current_weapon_original_image.copy()
        self._weapon_rect = self._weapon_image.get_rect(center=self.rect.center)
        self._special_weapon_offset = pygame.Vector2(20, -10)

    def update(self, keys, terrain, dt, *args, **kwargs):
        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self._weapon_image, self._weapon_rect)

    def get_projectile_origin(self):
        return pygame.math.Vector2(self._weapon_rect.center)

    def get_ability_duration(self):
        return self._time_duration_ability

    def get_ability_time_left(self):
        return self._ability_time_left

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
                self._ability_time_left = self._time_duration_ability
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
