import pygame
from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer
from src.entities.Ability import MissileBarrage

class Jones(AbstractPlayer):
    """
    Sergeant Jones - Explosives and area damage specialist
    Basic attack: Grenade launcher with slow reload
    Special ability: Missile Barrage
    """

    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):

        super().__init__(x, y)
        old_center = self.rect.center

        self.sprite_idle = pygame.image.load("assets/sprites/players/JonesIdle.png").convert_alpha()
        self.sprite_idle = pygame.transform.scale(
            self.sprite_idle, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        walk_sheet = pygame.image.load("assets/sprites/players/JonesWalk.png").convert_alpha()
        walk_sheet = pygame.transform.scale(
            walk_sheet, (Constants.PLAYER_WIDTH * 2, Constants.PLAYER_HEIGHT)
        )
        frame1 = walk_sheet.subsurface((0, 0, Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)).copy()
        frame2 = walk_sheet.subsurface((Constants.PLAYER_WIDTH, 0, Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)).copy()
        self.sprite_walk_frames = [frame1, frame2]

        self.sprite_jump = pygame.image.load("assets/sprites/players/JonesJump.png").convert_alpha()
        self.sprite_jump = pygame.transform.scale(
            self.sprite_jump, (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT)
        )

        self.image = self.sprite_idle
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        weapon_width = 100
        weapon_height = 100

        self.weapon_original = pygame.image.load("assets/sprites/weapons/GrenadeLauncher.png").convert_alpha()
        self.weapon_original = pygame.transform.scale(self.weapon_original, (weapon_width, weapon_height))

        self.missile_weapon_original = pygame.image.load("assets/sprites/weapons/MissileLauncher.png").convert_alpha()
        self.missile_weapon_original = pygame.transform.scale(self.missile_weapon_original, (weapon_width, weapon_height))

        self.current_weapon_original = self.weapon_original.copy()
        self.weapon_image = self.current_weapon_original.copy()  # inicia sem rotação
        self.weapon_rect = self.weapon_image.get_rect(center=self.rect.center)

    def update(self, keys, terrain, dt, *args, **kwargs):

        self.update_weapon()
        super().update(keys, terrain, dt, *args, **kwargs)

    def update_weapon(self):
        import math

        if pygame.mouse.get_pressed()[2]:
            self.current_weapon_original = self.missile_weapon_original.copy()

            offset_x, offset_y = 70, -10
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

    def get_player_color(self):
        return pygame.Color('olive')

    def get_initial_health(self):
        return int(Constants.PLAYER_MAX_HEALTH * 1.2)

    def get_projectile_color(self):
        return pygame.Color('orange')

    def get_projectile_image(self):
        image = pygame.image.load("assets/sprites/projectiles/GrenadeLauncherProjectile.png").convert_alpha()
        return pygame.transform.scale(image, (15, 15))

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED * 0.7

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5

    def get_projectile_damage(self):
        return int(Constants.PROJECTILE_DEFAULT_DAMAGE * 2)

    def choose_ability(self):
        return MissileBarrage(self)

    def _compute_cooldown_ability(self, dt):
        if not self._ready_ability:
            self._time_cooldown_ability += dt
            if self._time_cooldown_ability >= Constants.ABILITY_COOLDOWN:
                self._ready_ability = True
                self._time_cooldown_ability = 0

    def _compute_duration_ability(self, dt):
        if pygame.mouse.get_pressed()[2]:
            self._ready_ability = False

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
        instance._time_cooldown_ability = data["time_cooldown_ability"]
        instance._time_duration_ability = data["time_duration_ability"]
        return instance
