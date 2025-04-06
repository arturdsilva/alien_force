from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
import pygame


class LinearEnemy(AbstractEnemy):
    """
    Inimigo que se move em linha reta.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.HEIGHT / 2):
        """
        Inicializa um inimigo com movimento linear.

        :param x: Coordenada x inicial do inimigo
        :param y: Coordenada y inicial do inimigo
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.LINEAR_ENEMY_MAX_HEALTH
        self._speed = Constants.LINEAR_ENEMY_SPEED

    def _initialize_sprite(self, x, y):
        """
        Inicializa o sprite do inimigo linear.

        :param x: Coordenada x inicial
        :param y: Coordenada y inicial
        """
        self.image = pygame.Surface((Constants.LINEAR_ENEMY_WIDTH,
                                   Constants.LINEAR_ENEMY_HEIGHT))
        self.image.fill(Colors.RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def _move(self, dt):
        """
        Atualiza a posição do inimigo com movimento linear.

        :param dt: Tempo desde a última atualização
        """
        self.rect.x += self._speed * dt
        
        if self._limit_bounds():
            self._speed = -self._speed

    def _update_behavior(self, dt):
        """
        Atualiza comportamentos específicos do inimigo linear.
        Neste caso, não há comportamentos adicionais para atualizar.

        :param dt: Tempo desde a última atualização
        """
        pass 