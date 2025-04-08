import pygame
from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer


class Jones(AbstractPlayer):
    """
    Sergeant Jones - Explosives and area damage specialist
    Basic attack: Grenade launcher with slow reload
    Special ability: Missile Barrage
    """

    def get_player_color(self):
        return pygame.Color('olive')

    def get_initial_health(self):
        return int(Constants.PLAYER_MAX_HEALTH * 1.2)  

    def get_projectile_color(self):
        return pygame.Color('orange') 

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED * 0.7 

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5 

    def get_projectile_damage(self):
        return int(Constants.PROJECTILE_DEFAULT_DAMAGE * 2) 

    # TODO: Implement area damage for grenades
    # TODO: Implement special ability - Missile Barrage (multiple simultaneous projectiles)