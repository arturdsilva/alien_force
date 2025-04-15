import pygame
from config.Constants import Constants, Sounds
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.abilities.MissileBarrage import MissileBarrage
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator

class Jones(AbstractPlayer):
    """
    Sergeant Jones - Explosives and area damage specialist
    Basic attack: Grenade launcher with slow reload
    Special ability: Missile Barrage
    """

    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):

        super().__init__(x, y)
        self._initial_health = int(Constants.PLAYER_MAX_HEALTH * 1.2)
        self._health_points = self._initial_health
        self._ability_cooldown = Constants.MISSILE_COOLDOWN

        projectile_image = pygame.image.load(
            "assets/sprites/projectiles/GrenadeLauncherProjectile.png").convert_alpha()
        projectile_image = pygame.transform.scale(projectile_image, (15, 15))
        projectile_speed = Constants.PROJECTILE_DEFAULT_SPEED * 0.7
        projectile_frequency = Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5
        projectile_damage = int(Constants.PROJECTILE_DEFAULT_DAMAGE * 2)
        projectile_sound = Sounds.GUN_SHOT

        self._projectile_generator = ProjectileGenerator(projectile_speed,
                                                         projectile_frequency,
                                                         projectile_image,
                                                         projectile_damage,
                                                         projectile_sound,
                                                         is_player_projectile=True
                                                         )

        self._sprite_idle = pygame.image.load("assets/sprites/players/JonesIdle.png").convert_alpha()
        self._sprite_idle = pygame.transform.scale(
            self._sprite_idle, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        walk_sheet = pygame.image.load("assets/sprites/players/JonesWalk.png").convert_alpha()
        walk_sheet = pygame.transform.scale(
            walk_sheet, (Constants.PLAYER_WIDTH * 2, Constants.PLAYER_HEIGHT)
        )
        frame1 = walk_sheet.subsurface((0, 0, Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)).copy()
        frame2 = walk_sheet.subsurface((Constants.PLAYER_WIDTH, 0, Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)).copy()
        self._sprite_walk_frames = [frame1, frame2]

        self._sprite_jump = pygame.image.load("assets/sprites/players/JonesJump.png").convert_alpha()
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
            "assets/sprites/weapons/GrenadeLauncher.png").convert_alpha()
        self._weapon_original_image = pygame.transform.scale(self._weapon_original_image, (
        weapon_width, weapon_height))

        self._special_weapon_original_image = pygame.image.load(
            "assets/sprites/weapons/MissileLauncher.png").convert_alpha()
        self._special_weapon_original_image = pygame.transform.scale(
            self._special_weapon_original_image, (weapon_width, weapon_height))

        self._current_weapon_original_image = self._weapon_original_image.copy()
        self._weapon_image = self._current_weapon_original_image.copy()  # inicia sem rotação
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

    def choose_ability(self):
        return MissileBarrage(self)

    def _compute_cooldown_ability(self, dt):
        if not self._ready_ability:
            self._ability_downtime += dt
            if self._ability_downtime >= self._ability_cooldown:
                self._ready_ability = True
                self._audio_manager.play_sound(Sounds.RECHARGED)

    def _compute_duration_ability(self, dt):
        if pygame.mouse.get_pressed()[2] and self._ready_ability:
            self._ready_ability = False
            self._ability_downtime = 0

    # TODO: Implement area damage for grenades

    def to_dict(self):
        """
        Converts the player's state into a dictionary.
        """
        return super().to_dict()

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of Jones from a dictionary.
        """
        instance = cls()
        instance.rect.centerx = data["centerx"]
        instance.rect.bottom = data["bottom"]
        instance._health_points = data["health"]
        instance._is_jumping = data["is_jumping"]
        instance._y_speed = data["y_speed"]
        instance._ready_ability = data["ready_ability"]
        instance.time_cooldown_ability = data["time_cooldown_ability"]
        return instance
