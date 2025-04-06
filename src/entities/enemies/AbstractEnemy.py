import pygame
from abc import ABC, abstractmethod
from config.Constants import Constants, Colors
from src.entities.Projectile import Projectile, ProjectileGenerator


class AbstractEnemy(pygame.sprite.Sprite, ABC):
    """
    Represents an enemy.
    """

    def __init__(self, x=0, y=Constants.HEIGHT / 10):
        """
        Initializes an enemy.

        :param x: The initial enemy x coordinate.
        :param y: The initial enemy y coordinate.
        """

        super().__init__()
        self.image = None
        self.rect = None
        self._speed = Constants.ENEMY_SPEED
        self._health_points = None
        self._projectile_generator = None
        self._initialize_sprite(x, y)
        
    @abstractmethod
    def _initialize_sprite(self, x, y):
        """
        Updates the enemy.

        :param dt: The duration of one iteration.
        :param player_projectiles: Player projectiles on screen.
        """
        pass

    def update(self, dt, player_projectiles, terrain=None):
        """
        Atualiza o estado do inimigo.

        :param dt: Tempo desde a última atualização
        :param player_projectiles: Projéteis do jogador na tela
        :param terrain: Grupo de sprites do terreno (opcional)
        """
        self._move(dt, terrain)
        self._limit_bounds()
        self._compute_damage(player_projectiles)
        self._update_behavior(dt, terrain)

    @abstractmethod
    def _move(self, dt, terrain=None):
        """
        Método abstrato para definir o movimento do inimigo.
        Deve ser implementado por cada classe filha.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (opcional)
        """
        pass

    @abstractmethod
    def _update_behavior(self, dt, terrain=None):
        """
        Método abstrato para atualizar comportamentos específicos do inimigo.
        Deve ser implementado por cada classe filha.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (opcional)
        """
        pass

    def _limit_bounds(self):
        """
        Limits enemy position to inside screen boundaries.
        """

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

    def _compute_damage(self, player_projectiles):
        """
        Calcula o dano recebido por projéteis do jogador.
        
        :param player_projectiles: Lista de projéteis do jogador
        :return: True se o inimigo foi destruído
        """
        for projectile in player_projectiles:
            if pygame.sprite.collide_rect(self, projectile):
                self._health_points -= projectile.damage
                projectile.kill()
                if self._health_points <= 0:
                    self.kill()
                    return True
        return False

    @property
    def health(self):
        """
        Retorna a vida atual do inimigo.
        
        :return: Pontos de vida atuais
        """
        return self._health_points
