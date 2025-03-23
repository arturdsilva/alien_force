import pygame
from config.Constants import Constants, Colors


class AbstractEnemy(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = Constants.HEIGHT / 10,
                 speed_factor = 1,
                 width = 50,
                 height = 50,
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
        self.limit_bounds()


    def move(self, dt):
        self.rect.x += self.speed * dt
        if self.limit_bounds():
            self.speed = -self.speed


    def limit_bounds(self):
        out_of_bounds = False
        if self.rect.left < 0:
            self.rect.left = 0
            out_of_bounds = True
        if self.rect.right > Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            out_of_bounds = True
        if self.rect.top < 0:
            self.rect.top = 0
            out_of_bounds = True
        if self.rect.bottom > Constants.HEIGHT:
            self.rect.bottom = Constants.HEIGHT
            out_of_bounds = True

        return out_of_bounds
