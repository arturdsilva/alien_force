import pygame
from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer


class Rain(AbstractPlayer):
    """
    Lieutenant Rain - Precision and survival specialist
    Basic attack: Precision rifle with very slow reload
    Special ability: Survival Mode (speed and reload buff)
    """

    def get_player_color(self):
        return pygame.Color('darkgreen')
    def get_initial_health(self):
        return int(Constants.PLAYER_MAX_HEALTH * 0.9) 

    def get_projectile_color(self):
        return pygame.Color('lime')  

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED * 2.0  

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.5 

    def get_projectile_damage(self):
        return int(Constants.PROJECTILE_DEFAULT_DAMAGE * 1.8)  

    # TODO: Implement special ability - Survival Mode (speed and reload buff)