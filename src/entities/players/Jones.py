import pygame
from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer


class Jones(AbstractPlayer):
    """
    Sargento Jones - Especialista em explosivos e dano em área
    Ataque básico: Lançador de granadas com recarga lenta
    Habilidade especial: Barragem de Mísseis
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

    # TODO: Implementar dano em área para as granadas
    # TODO: Implementar habilidade especial - Barragem de Mísseis (múltiplos projéteis simultâneos)