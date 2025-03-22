import pygame
from config.Constants import Constants


class AbstractPlayer(pygame.sprite.Sprite):
    def __init__(self, x=Constants.WIDTH / 2, y=Constants.HEIGHT / 2):
        super().__init__()
        self.image = pygame.Surface(
            (Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT))
        self.image.fill(Constants.WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = Constants.PLAYER_SPEED


    def handle_input(self, keys, dt):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.rect.x += self.speed * dt


    def update(self, keys, dt):
        self.handle_input(keys, dt)
        self._limit_bounds()


    def _limit_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
