import pygame

from config.Constants import Constants
from config.Constants import Colors
from .AbstractProjectile import AbstractProjectile
from config.Constants import Sounds
from src.utils.AudioManager import AudioManager


class BombProjectile(AbstractProjectile):
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
        self.__exploded = False
        self._explosion_time = 0
        self._explosion_duration = 1.0
        self._explosion_surface = None
        self._explosion_rect = None
        self.__audio_manager = AudioManager()

    def update(self, dt, terrain=None, player=None):
        """
        Updates the bomb state.

        :param dt: Time since last update
        :param terrain: Terrain sprite group (optional)
        :param player: Player sprite (optional)
        """
        if not self.__exploded:
            self._position += self._velocity * dt
            self.rect.center = self._position

            # Check terrain collision
            if terrain:
                hits = pygame.sprite.spritecollide(self, terrain, False)
                if hits:
                    self.rect.bottom = hits[0].rect.top
                    self.__trigger_explosion(player)
        else:
            self._explosion_time += dt
            if self._explosion_time >= self._explosion_duration:
                self.kill()

    def __trigger_explosion(self, player):
        """
        Triggers the bomb explosion and applies damage in the area.

        :param player: Player sprite
        """
        self.__exploded = True
        self.__audio_manager.play_sound(Sounds.BOOM)

        # Create explosion area
        self._explosion_rect = pygame.Rect(0, 0, self._explosion_radius * 2, self._explosion_radius * 2)
        self._explosion_rect.center = self.rect.center
        # Create explosion surface
        color = Constants.TANK_BOMB_EXPLOSION_COLOR
        self._explosion_surface = pygame.Surface((self._explosion_radius * 2, self._explosion_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self._explosion_surface,
                           (color[0], color[1], color[2], 80),
                           (self._explosion_radius, self._explosion_radius), self._explosion_radius)
        pygame.draw.circle(self._explosion_surface, Constants.TANK_BOMB_EXPLOSION_COLOR,

                           (self._explosion_radius, self._explosion_radius), self._explosion_radius * 0.7)
        pygame.draw.circle(self._explosion_surface, Colors.GLOW_WHITE,
                           (self._explosion_radius, self._explosion_radius), self._explosion_radius * 0.3)

        # Applies damage to the player if inside explosion radius
        if player and self._explosion_rect.colliderect(player.rect):
            player.inflict_damage(self.damage)

    def compute_collision(self, player):
        if not self.__exploded and pygame.sprite.collide_rect(self, player):
            self.__trigger_explosion(player)

    def draw(self, screen):
        """
        Draws the bomb or explosion on screen.

        :param screen: Screen surface
        """
        if self.__exploded and self._explosion_surface:
            # Updates alpha according to remaining explosion time
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
        return self.__exploded