import pygame
from abc import ABC, abstractmethod
from config.Constants import Constants


class AbstractAbility(pygame.sprite.Sprite, ABC):
    """
    Represents a generic skill
    """

    def __init__(self, agent):
        """
        Initializes a skill

        :param agent: The ability user.
        """
        super().__init__()
        self._agent = agent
        self._speed = Constants.ABILITY_DEFAULT_SPEED
        self._image = None
        self._damage = Constants.ABILITY_DEFAULT_DAMAGE
        self._lifetime = None

    @property
    def damage(self):
        """
        Returns the damage value of the ability.

        :return: The damage value
        """
        return self._damage

    @abstractmethod
    def generate(self, target, dt, abilities_group):
        pass