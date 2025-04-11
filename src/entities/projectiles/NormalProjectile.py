import pygame
from .BaseProjectile import BaseProjectile


class NormalProjectile(BaseProjectile):
    """
    Projétil normal que se move em linha reta e causa dano ao atingir o alvo.
    """
    
    def __init__(self, position, velocity, image, damage, is_player_projectile=False):
        """
        Inicializa um projétil normal.

        :param position: Posição inicial do projétil
        :param velocity: Vetor de velocidade do projétil
        :param image: Imagem do projétil
        :param damage: Dano causado pelo projétil
        :param is_player_projectile: Indica se é um projétil do jogador
        """
        super().__init__(position, velocity, image, damage)
        self._is_player_projectile = is_player_projectile

    def update(self, dt, terrain=None, player=None):
        """
        Atualiza o estado do projétil.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (opcional)
        :param player: Sprite do jogador (opcional)
        """
        # Atualiza a posição do projétil
        self._position += self._velocity * dt
        self.rect.center = self._position
        
        # Verifica se saiu dos limites da tela
        self._handle_bounds()
        
        # Verifica colisão com o terreno
        if terrain:
            hits = pygame.sprite.spritecollide(self, terrain, False)
            if hits:
                self.kill()
        
        # Verifica colisão com o jogador apenas se não for um projétil do jogador
        if not self._is_player_projectile and player and pygame.sprite.collide_rect(self, player):
            player._health_points -= self._damage
            self.kill()

    def draw(self, screen):
        """
        Desenha o projétil na tela.

        :param screen: Superfície da tela
        """
        screen.blit(self.image, self.rect) 