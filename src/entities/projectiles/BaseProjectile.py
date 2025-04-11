import pygame
from abc import ABC, abstractmethod
from config.Constants import Constants


class BaseProjectile(pygame.sprite.Sprite, ABC):
    """
    Classe base abstrata para todos os tipos de projéteis.
    Define a interface comum que todos os projéteis devem implementar.
    """
    
    def __init__(self, position, velocity, image, damage):
        """
        Inicializa um projétil base.

        :param position: Posição inicial do projétil
        :param velocity: Vetor de velocidade do projétil
        :param image: Imagem do projétil
        :param damage: Dano causado pelo projétil
        """
        super().__init__()
        self._position = position
        self._velocity = velocity
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self._damage = damage

    @abstractmethod
    def update(self, dt, terrain=None, player=None):
        """
        Atualiza o estado do projétil.
        Método abstrato que deve ser implementado pelas classes filhas.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (opcional)
        :param player: Sprite do jogador (opcional)
        """
        pass

    def _handle_bounds(self):
        """
        Remove projéteis que saem dos limites da tela.
        """
        if (self.rect.right < 0 or
                self.rect.left > Constants.WIDTH or
                self.rect.bottom < 0 or self.rect.top > Constants.HEIGHT):
            self.kill()

    @abstractmethod
    def draw(self, screen):
        """
        Desenha o projétil na tela.
        Método abstrato que deve ser implementado pelas classes filhas.

        :param screen: Superfície da tela
        """
        pass

    @property
    def damage(self):
        """
        Retorna o dano causado pelo projétil.
        """
        return self._damage 