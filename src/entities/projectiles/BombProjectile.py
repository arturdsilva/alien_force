import pygame
from .BaseProjectile import BaseProjectile


class BombProjectile(BaseProjectile):
    """
    Bomb-type projectile that falls vertically and explodes upon hitting terrain or player.
    """
    
    def __init__(self, position, velocity, image, damage, explosion_radius):
        """
        Initializes a bomb.

        :param position: Initial position of the bomb
        :param velocity: Velocity vector of the bomb
        :param image: Bomb image
        :param damage: Damage caused by the bomb
        :param explosion_radius: Explosion radius
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
        Updates the bomb state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        :param player: Player sprite (optional)
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
        Triggers the bomb explosion and applies damage in the area.

        :param terrain: Terrain sprite group
        :param player: Player sprite
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
        # if player and self._explosion_rect.colliderect(player.rect):
        #     player._health_points -= self._damage

    def draw(self, screen):
        """
        Draws the bomb or explosion on screen.

        :param screen: Screen surface
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
        Returns the explosion radius.
        """
        return self._explosion_radius

    @property
    def exploded(self):
        """
        Returns whether the bomb has exploded.
        """
        return self._exploded 