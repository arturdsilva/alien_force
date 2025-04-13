import pygame
from .BaseProjectile import BaseProjectile


class NormalProjectile(BaseProjectile):
    """
    Normal projectile that moves in a straight line and causes damage upon hitting the target.
    """
    
    def __init__(self, position, velocity, image, damage, is_player_projectile=False):
        """
        Initializes a normal projectile.

        :param position: Initial position of the projectile
        :param velocity: Velocity vector of the projectile
        :param image: Projectile image
        :param damage: Damage caused by the projectile
        :param is_player_projectile: Indicates if it's a player projectile
        """
        super().__init__(position, velocity, image, damage)
        self._is_player_projectile = is_player_projectile

    def update(self, dt, terrain=None, player=None):
        """
        Updates the projectile state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        :param player: Player sprite (optional)
        """
        # Update projectile position
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
        Draws the projectile on screen.

        :param screen: Screen surface
        """
        screen.blit(self.image, self.rect)