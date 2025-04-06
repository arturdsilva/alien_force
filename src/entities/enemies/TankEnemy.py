from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
import pygame


class TankEnemy(AbstractEnemy):
    """
    Inimigo grande e resistente que se move lentamente no topo da tela.
    """

    def __init__(self, x=Constants.WIDTH, y=Constants.TANK_ENEMY_Y):
        """
        Inicializa um inimigo tanque.

        :param x: Coordenada x inicial do inimigo
        :param y: Coordenada y inicial do inimigo (fixo no topo)
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.TANK_ENEMY_MAX_HEALTH
        self._speed = Constants.TANK_ENEMY_SPEED

    def _initialize_sprite(self, x, y):
        """
        Inicializa o sprite do inimigo tanque.

        :param x: Coordenada x inicial
        :param y: Coordenada y inicial
        """
        self.image = pygame.Surface((Constants.TANK_ENEMY_WIDTH,
                                   Constants.TANK_ENEMY_HEIGHT))
        self.image.fill(Colors.PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def _move(self, dt, terrain=None):
        """
        Atualiza a posição do inimigo tanque.
        Move-se apenas horizontalmente no topo da tela.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (não utilizado por este inimigo)
        """
        self.rect.x += self._speed * dt
        
        # Mantém o Y fixo no topo
        self.rect.centery = Constants.TANK_ENEMY_Y
        
        # Inverte direção nas bordas
        if self.rect.left <= 0:
            self.rect.left = 0
            self._speed = abs(self._speed)
        elif self.rect.right >= Constants.WIDTH:
            self.rect.right = Constants.WIDTH
            self._speed = -abs(self._speed)

    def _update_behavior(self, dt, terrain=None):
        """
        Atualiza comportamentos específicos do inimigo tanque.
        Neste caso, não há comportamentos adicionais para atualizar.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (não utilizado por este inimigo)
        """
        pass 