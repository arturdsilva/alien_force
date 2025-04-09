import pygame
from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator
from src.entities.Abilitiy import MissileBarrage
from src.entities.Abilitiy import LaserBeam
from src.entities.Abilitiy import CriticalShot


class AbstractPlayer(pygame.sprite.Sprite):
    """
    Represents a player.
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
        self.image.fill(Constants.PLAYER_DEFAULT_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self._is_jumping = False
        self._y_speed = 0
        self._health_points = Constants.PLAYER_MAX_HEALTH
        self._ready_ability = True
        self._time_cooldown_ability = 0
        self._time_duration_ability = 0
        self.__CHARACTER_ID = 2
        self._prev_mouse_pressed = False
        self._charging_critical = 0

        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH, Constants.PROJECTILE_HEIGHT))
        ability_image = pygame.Surface(
            (Constants.ABILITY_WIDTH, Constants.ABILITY_HEIGHT)
        )
        projectile_image.fill(Constants.PROJECTILE_DEFAULT_COLOR)
        ability_image.fill(Constants.ABILITY_DEFAULT_COLOR)
        self.projectile_generator = ProjectileGenerator(self,
                                                        Constants.PROJECTILE_DEFAULT_SPEED,
                                                        Constants.PROJECTILE_DEFAULT_FREQUENCY,
                                                        projectile_image,
                                                        Constants.PROJECTILE_DEFAULT_DAMAGE)

        ABILITY_FACTORIES = {
            1: lambda self, image: MissileBarrage(
                self,
                Constants.ABILITY_SPEED,
                image,
                Constants.ABILITY_DAMAGE,
                Constants.MISSILE_SHOT_CAPACITY
            ),
            2: lambda self, image: LaserBeam(
                self,
                Constants.ABILITY_DAMAGE,
                Constants.LASER_DURATION,
                Constants.LASER_WIDTH,
                Constants.COLOR_LASER,
                Constants.LASER_LIFETIME
            ),
            3: lambda self, image: CriticalShot(
                self,
                Constants.ABILITY_SPEED*3,
                image,
                Constants.ABILITY_DAMAGE,
            )
        }
        factory = ABILITY_FACTORIES.get(self.__CHARACTER_ID)
        if factory:
            self.ability_generator = factory(self, ability_image)

    def update(self, terrain, keys, dt, player_projectiles,
               enemies_projectiles, abilities):
        """
        Updates the player.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        :param player_projectiles: Player projectiles on screen.
        :param enemies_projectiles: Enemies projectiles on screen.
        :param abilities: Abilities on screen.
        """

        self._handle_input(keys, terrain, dt, player_projectiles, abilities)
        self._limit_bounds()
        self._compute_damage(enemies_projectiles)

    def _handle_input(self, terrain, keys, dt, projectiles, abilities):
        """
        Handles player input.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles on screen.
        :param abilities: Abilities on screen.
        """

        self._compute_vertical_position(terrain, keys, dt)
        self._compute_horizontal_position(terrain, keys, dt)
        if pygame.mouse.get_pressed()[0]:
            target = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                         pygame.mouse.get_pos()[1])
            self.projectile_generator.generate(target, dt, projectiles)
        self._compute_cooldown_ability(dt)
        if pygame.mouse.get_pressed()[2]:
            target_ability = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                                 pygame.mouse.get_pos()[1])
            if self._ready_ability:
                self.ability_generator.generate(target_ability, dt,
                                                abilities)
        self._compute_duration_ability(dt)

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
        for projectile in enemies_projectiles:
            if pygame.sprite.collide_rect(self, projectile):
                print("got hit")

    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """
        if self.__CHARACTER_ID == 1 or self.__CHARACTER_ID == 2:
            if not self._ready_ability:
                self._time_cooldown_ability += dt
                if self._time_cooldown_ability >= Constants.ABILITY_COOLDOWN:
                    self._ready_ability = True
                    self._time_cooldown_ability = 0
        elif self.__CHARACTER_ID == 3:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] and not self._prev_mouse_pressed:
                self.charging_critical += 1
                if self.charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                    self._ready_ability = True
            self.prev_mouse_pressed = mouse_buttons[0]

    def _compute_duration_ability(self, dt):
        """
        Updates the duration logic for the character's ability based on character type.

        :param dt: The duration of one iteration.
        """

        if self.__CHARACTER_ID == 1:
            if pygame.mouse.get_pressed()[2]:
                self._ready_ability = False
        elif self.__CHARACTER_ID == 2:
            if pygame.mouse.get_pressed()[2]:
                self._time_duration_ability += dt
                if self._time_duration_ability >= Constants.ABILITY_DURATION:
                    self._time_duration_ability = 0
                    self._ready_ability = False
        elif self.__CHARACTER_ID == 3:
            if pygame.mouse.get_pressed()[2]:
                self._ready_ability = False
                if self._charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                    self.charging_critical = 0