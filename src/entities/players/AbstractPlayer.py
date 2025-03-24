import pygame
from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator


class AbstractPlayer(pygame.sprite.Sprite):
    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2,
                 color=Constants.PLAYER_DEFAULT_COLOR):
        super().__init__()
        self.image = pygame.Surface(
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.jumping = False
        self.y_speed = 0

        projectile_image = pygame.Surface(
            (Constants.PROJECTILE_DEFAULT_WIDTH, Constants.PROJECTILE_HEIGHT))
        projectile_image.fill(Constants.PROJECTILE_DEFAULT_COLOR)
        self.projectile_generator = ProjectileGenerator(self,
                                                        Constants.PROJECTILE_DEFAULT_SPEED,
                                                        Constants.PROJECTILE_DEFAULT_FREQUENCY,
                                                        projectile_image,
                                                        Constants.PROJECTILE_DEFAULT_DAMAGE)

    def update(self, terrain, keys, dt, projectiles):
        self.handle_input(keys, terrain, dt, projectiles)
        self.limit_bounds()

    def handle_input(self, terrain, keys, dt, projectiles):
        self.compute_vertical_position(terrain, keys, dt)
        self.compute_horizontal_position(terrain, keys, dt)
        if pygame.mouse.get_pressed()[0]:
            target = pygame.math.Vector2(pygame.mouse.get_pos()[0],
                                         pygame.mouse.get_pos()[1])
            self.projectile_generator.generate(target, dt, projectiles)

    def compute_vertical_position(self, terrain, keys, dt):
        if (keys[pygame.K_w] or keys[pygame.K_s]) and not self.jumping:
            self.y_speed = -Constants.JUMP_SPEED
            self.jumping = True

        self.y_speed += + Constants.GRAVITY * dt
        self.rect.y += self.y_speed * dt

        hits = pygame.sprite.spritecollide(self, terrain, False)
        for block in hits:
            self.rect.bottom = block.rect.y
            self.jumping = False
            self.y_speed = 0

    def compute_horizontal_position(self, terrain, keys, dt):
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

    def limit_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
