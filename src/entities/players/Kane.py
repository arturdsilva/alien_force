import pygame
from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer


class Kane(AbstractPlayer):
    """
    Captain "Cyborg" Kane - Assault weapons and plasma specialist
    Basic attack: Assault rifle with fast reload
    Special ability: Plasma accelerator cannon
    """

    def get_player_color(self):
        return pygame.Color('steelblue')

    def get_initial_health(self):
        return Constants.PLAYER_MAX_HEALTH 

    def get_projectile_color(self):
        return pygame.Color('yellow') 

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED * 1.5 

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY * 1.5 

    def get_projectile_damage(self):
        return int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.2) 

    # TODO: Implement special ability - Plasma accelerator cannon