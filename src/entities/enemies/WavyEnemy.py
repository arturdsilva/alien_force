from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
import numpy as np
import pygame


class WavyEnemy(AbstractEnemy):
    """
    Inimigo que se move em um padrão sinusoidal.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 3):
        """
        Inicializa um inimigo com movimento ondular.

        :param x: Coordenada x inicial do inimigo
        :param y: Coordenada y inicial do inimigo
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.WAVY_ENEMY_MAX_HEALTH
        self._speed = 1.5 * Constants.ENEMY_SPEED
        self.__timer = 0
        self.__amplitude = Constants.WAVY_ENEMY_AMPLITUDE
        self.__angular_frequency = Constants.WAVY_ENEMY_ANGULAR_FREQUENCY
        self.__base_y = y

    def _initialize_sprite(self, x, y):
        """
        Inicializa o sprite do inimigo ondular.

        :param x: Coordenada x inicial
        :param y: Coordenada y inicial
        """
        self.image = pygame.Surface((Constants.WAVY_ENEMY_WIDTH,
                                   Constants.WAVY_ENEMY_HEIGHT))
        self.image.fill(Colors.BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def _move(self, dt):
        """
        Atualiza a posição do inimigo com movimento ondular.

        :param dt: Tempo desde a última atualização
        """
        self.rect.x += self._speed * dt
        self.rect.y = self.__base_y + self.__amplitude * np.sin(
            self.__angular_frequency * self.__timer)
        
        if self._limit_bounds():
            self._speed = -self._speed

    def _update_behavior(self, dt):
        """
        Atualiza o timer para o movimento ondular.

        :param dt: Tempo desde a última atualização
        """
        self.__timer = (self.__timer + dt) % (
                2 * np.pi / self.__angular_frequency)
