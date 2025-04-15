import pygame
from config.Constants import Constants, Sounds
from src.entities.Ability import CriticalShot
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator


class Rain(AbstractPlayer):
    """
    Lieutenant Rain - Precision and survival specialist
    Basic attack: Precision rifle with very slow reload
    Special ability: Survival Mode (speed and reload buff)
    """

    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):
        super().__init__(x, y)
        self._initial_health = int(Constants.PLAYER_MAX_HEALTH * 0.9)
        self._health_points = self._initial_health
        self._ability_cooldown = Constants.CRITICAL_SHOT_COOLDOWN

        projectile_image = pygame.image.load(
            "assets/sprites/projectiles/PrecisionRifleProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (15, 15))
        projectile_speed = Constants.PROJECTILE_DEFAULT_SPEED * 2.0
        projectile_frequency = Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5
        projectile_damage = int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.8)
        projectile_sound = Sounds.GUN_SHOT

        self._projectile_generator = ProjectileGenerator(self,
                                                         projectile_speed,
                                                         projectile_frequency,
                                                         projectile_image,
                                                         projectile_damage,
                                                         projectile_sound,
                                                         is_player_projectile=True
                                                         )
        self.time_projectile_generation = 0

        self._sprite_idle = pygame.image.load(
            "assets/sprites/players/RainIdle.png").convert_alpha()
        self._sprite_idle = pygame.transform.scale(
            self._sprite_idle,
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
        self._sprite_walk_frames = [frame1, frame2]

        self._sprite_jump = pygame.image.load(
            "assets/sprites/players/RainJump.png").convert_alpha()
        self._sprite_jump = pygame.transform.scale(
            self._sprite_jump,
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        self.image = self._sprite_idle
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._charged_shots = Constants.NORMAL_SHOTS_REQUIRED
        self._charging_critical = Constants.NORMAL_SHOTS_REQUIRED

        weapon_width = 70
        weapon_height = 70

        self._weapon_original_image = pygame.image.load(
            "assets/sprites/weapons/PrecisionRifle.png").convert_alpha()
        self._weapon_original_image = pygame.transform.scale(self._weapon_original_image, (
        weapon_width, weapon_height))

        self._special_weapon_original_image = pygame.image.load(
            "assets/sprites/weapons/SpecialPrecisionRifle.png").convert_alpha()
        self._special_weapon_original_image = pygame.transform.scale(
            self._special_weapon_original_image, (weapon_width, weapon_height))

        self._current_weapon_original_image = self._weapon_original_image.copy()
        self._weapon_image = self._current_weapon_original_image.copy()  # inicia sem rotação
        self._weapon_rect = self._weapon_image.get_rect(center=self.rect.center)

    def update(self, keys, terrain, dt, *args, **kwargs):
        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self._weapon_image, self._weapon_rect)

    def get_projectile_origin(self):
        return pygame.math.Vector2(self._weapon_rect.center)

    def choose_ability(self):
        return CriticalShot(self)

    def _compute_cooldown_ability(self, dt):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and not self._ready_ability:

            self.time_projectile_generation += dt
            if self.time_projectile_generation >= 1 / (
                    Constants.PROJECTILE_DEFAULT_FREQUENCY):
                self._charged_shots += 1
                self.time_projectile_generation = 0
                if self._charged_shots <= Constants.NORMAL_SHOTS_REQUIRED:
                    self._ability_downtime = (self._charged_shots *
                                              self._ability_cooldown /
                                              Constants.NORMAL_SHOTS_REQUIRED)

            if self._charged_shots >= Constants.NORMAL_SHOTS_REQUIRED:
                self._ready_ability = True

    def _compute_duration_ability(self, dt):
        if pygame.mouse.get_pressed()[2]:
            self._ready_ability = False
            if self._charged_shots >= Constants.NORMAL_SHOTS_REQUIRED:
                self._charged_shots = 0
                self.time_projectile_generation = 0
                self._ability_downtime = 0


    # TODO: Implement special ability - Survival Mode (speed and reload buff)

    def to_dict(self):
        """
        Converts the player's state into a dictionary, including Rain-specific attributes.
        """
        data = super().to_dict()
        data["charging_critical"] = self._charged_shots
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
        instance._charged_shots = data.get("charging_critical", 0)
        instance.time_projectile_generation = data.get(
            "time_projectile_geration", 0)
        return instance
