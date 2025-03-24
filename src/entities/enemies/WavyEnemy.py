from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
import numpy as np


class WavyEnemy(AbstractEnemy):
    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 3,
                 speed_factor=1.5,
                 color=Colors.BLUE):
        super().__init__(x=x, y=y, speed_factor=speed_factor,
                         width=Constants.WAVY_ENEMY_WIDTH,
                         height=Constants.WAVY_ENEMY_HEIGHT, color=color)
        self.timer = 0
        self.amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self.angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY
        self.height = Constants.WAVY_ENEMY_Y

    def move(self, dt):
        self.rect.x += self.speed * dt
        self.rect.y = self.height + self.amplitude * np.sin(
            self.angular_frequency * self.timer)
        self.timer += dt

        if self.limit_bounds():
            self.speed = -self.speed
