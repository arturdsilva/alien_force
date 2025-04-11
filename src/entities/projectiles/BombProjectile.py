import pygame
from .BaseProjectile import BaseProjectile


class BombProjectile(BaseProjectile):
    """
    Projétil do tipo bomba que cai verticalmente e explode ao atingir o terreno ou o jogador.
    """
    
    def __init__(self, position, velocity, image, damage, explosion_radius):
        """
        Inicializa uma bomba.

        :param position: Posição inicial da bomba
        :param velocity: Vetor de velocidade da bomba
        :param image: Imagem da bomba
        :param damage: Dano causado pela bomba
        :param explosion_radius: Raio da explosão
        """
        super().__init__(position, velocity, image, damage)
        self._explosion_radius = explosion_radius
        self._exploded = False
        self._explosion_time = 0
        self._explosion_duration = 1.0  # 1 segundo de duração
        self._explosion_surface = None
        self._explosion_rect = None

    def update(self, dt, terrain=None, player=None):
        """
        Atualiza o estado da bomba.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno (opcional)
        :param player: Sprite do jogador (opcional)
        """
        if not self._exploded:
            self._position += self._velocity * dt
            self.rect.center = self._position
            
            # Verifica colisão com o jogador primeiro
            if player and pygame.sprite.collide_rect(self, player):
                self._explode(terrain, player)
            # Depois verifica colisão com o terreno
            elif terrain:
                hits = pygame.sprite.spritecollide(self, terrain, False)
                if hits:
                    self.rect.bottom = hits[0].rect.top
                    self._explode(terrain, player)
        else:
            # Atualiza o tempo da explosão
            self._explosion_time += dt
            if self._explosion_time >= self._explosion_duration:
                self.kill()

    def _explode(self, terrain, player):
        """
        Dispara a explosão da bomba e aplica dano na área.

        :param terrain: Grupo de sprites do terreno
        :param player: Sprite do jogador
        """
        self._exploded = True
        
        # Cria área da explosão
        self._explosion_rect = pygame.Rect(0, 0, self._explosion_radius * 2, self._explosion_radius * 2)
        self._explosion_rect.center = self.rect.center
        
        # Cria superfície da explosão
        self._explosion_surface = pygame.Surface((self._explosion_radius * 2, self._explosion_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self._explosion_surface, (128, 0, 128, 128), 
                         (self._explosion_radius, self._explosion_radius), 
                         self._explosion_radius)
        
        # Aplica dano ao jogador se estiver no raio da explosão
        if player and self._explosion_rect.colliderect(player.rect):
            player._health_points -= self._damage

    def draw(self, screen):
        """
        Desenha a bomba ou explosão na tela.

        :param screen: Superfície da tela
        """
        if self._exploded and self._explosion_surface:
            # Calcula alpha baseado no tempo restante
            alpha = int(255 * (1 - self._explosion_time / self._explosion_duration))
            self._explosion_surface.set_alpha(alpha)
            screen.blit(self._explosion_surface, self._explosion_rect)
        else:
            screen.blit(self.image, self.rect)

    @property
    def explosion_radius(self):
        """
        Retorna o raio da explosão.
        """
        return self._explosion_radius

    @property
    def exploded(self):
        """
        Retorna se a bomba explodiu.
        """
        return self._exploded 