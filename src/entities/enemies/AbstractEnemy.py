import pygame
from config.Constants import Constants, Colors


class AbstractEnemy(pygame.sprite.Sprite):
    def __init__(self, x = Constants.WIDTH / 2, y = 0,
                 speed_factor = 1,
                 width = Constants.PLAYER_WIDTH,
                 height = Constants.PLAYER_HEIGHT,
                 color = Colors.RED):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed_factor * Constants.ENEMY_SPEED


    def update(self, dt):
        self.move(dt)
        self._limit_bounds()


    def move(self, dt):
        self.rect.y += self.speed * dt


    def _limit_bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
