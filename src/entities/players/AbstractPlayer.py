import pygame
from config.Constants import Constants, Colors


class AbstractPlayer(pygame.sprite.Sprite):
    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2,
                 color=Colors.WHITE):
        super().__init__()
        self.image = pygame.Surface(
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.jumping = False
        self.last_vertical_speed = 0


    def update(self, terrain, keys, dt):
        self.handle_input(keys, terrain, dt)
        self._limit_bounds()


    def handle_input(self, terrain, keys, dt):
        self.compute_vertical_position(terrain, keys, dt)
        self.compute_horizontal_position(terrain, keys, dt)


    def compute_vertical_position(self, terrain, keys, dt):
        speed = self.last_vertical_speed
        if (keys[pygame.K_w] or keys[pygame.K_s]) and not self.jumping:
            speed = -Constants.JUMP_SPEED
            self.jumping = True

        speed = speed + Constants.GRAVITY * dt
        print(speed)
        self.rect.y += speed * dt

        hits = pygame.sprite.spritecollide(self, terrain, False)
        for block in hits:
            self.rect.bottom = block.rect.y
            self.jumping = False
            speed = 0

        self.last_vertical_speed = speed


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


    def _limit_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
