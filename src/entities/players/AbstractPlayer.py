import pygame
from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator


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

        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH, Constants.PROJECTILE_HEIGHT))
        projectile_image.fill(Constants.PROJECTILE_DEFAULT_COLOR)
        self.projectile_generator = ProjectileGenerator(self,
                                                        Constants.PROJECTILE_DEFAULT_SPEED,
                                                        Constants.PROJECTILE_DEFAULT_FREQUENCY,
                                                        projectile_image,
                                                        Constants.PROJECTILE_DEFAULT_DAMAGE)

    def update(self, terrain, keys, dt, player_projectiles,
               enemies_projectiles):
        """
        Updates the player.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        :param player_projectiles: Player projectiles on screen.
        :param enemies_projectiles: Enemies projectiles on screen.
        """

        self._handle_input(keys, terrain, dt, player_projectiles)
        self._limit_bounds()
        self._compute_damage(enemies_projectiles)

    def _handle_input(self, terrain, keys, dt, projectiles):
        """
        Handles player input.

        :param terrain: The terrain.
        :param keys: Keys being input by the player.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles on screen.
        """

        self._compute_vertical_position(terrain, keys, dt)
        self._compute_horizontal_position(terrain, keys, dt)
        if pygame.mouse.get_pressed()[0]:
            target = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                         pygame.mouse.get_pos()[1])
            self.projectile_generator.generate(target, dt, projectiles)

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
