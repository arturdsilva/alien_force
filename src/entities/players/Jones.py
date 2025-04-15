import pygame
from config.Constants import Constants, Sounds
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.Ability import MissileBarrage
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

        self._projectile_generator = ProjectileGenerator(self,
                                                         projectile_speed,
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

        self.weapon_original = pygame.image.load("assets/sprites/weapons/GrenadeLauncher.png").convert_alpha()
        self.weapon_original = pygame.transform.scale(self.weapon_original, (weapon_width, weapon_height))

        self.missile_weapon_original = pygame.image.load("assets/sprites/weapons/MissileLauncher.png").convert_alpha()
        self.missile_weapon_original = pygame.transform.scale(self.missile_weapon_original, (weapon_width, weapon_height))

        self.current_weapon_original = self.weapon_original.copy()
        self.weapon_image = self.current_weapon_original.copy()  # inicia sem rotação
        self.weapon_rect = self.weapon_image.get_rect(center=self.rect.center)
        self._special_weapon_offset = pygame.Vector2(20, -10)

    def update(self, keys, terrain, dt, *args, **kwargs):

        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def update_weapon(self):
        import math

        if pygame.mouse.get_pressed()[2]:
            self.current_weapon_original = self.missile_weapon_original.copy()

            offset_x = 50 + self._special_weapon_offset.x
            offset_y = 0 + self._special_weapon_offset.y
        else:
            self.current_weapon_original = self.weapon_original.copy()

            offset_x, offset_y = 50, 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        self.weapon_image = pygame.transform.rotate(self.current_weapon_original, angle)
        new_center = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
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

    def get_ready_ability(self):
        return self._ready_ability

    def choose_ability(self):
        return MissileBarrage(self)

    def _compute_cooldown_ability(self, dt):
        if not self._ready_ability:
            self._ability_downtime += dt
            if self._ability_downtime >= self._ability_cooldown:
                self._ready_ability = True

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
        instance._ability_time_spent = data["time_duration_ability"]
        return instance
