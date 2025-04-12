import pygame

from config.Constants import Constants
from src.entities.AbstractAbility import CriticalShot
from src.entities.players.AbstractPlayer import AbstractPlayer


class Rain(AbstractPlayer):
    """
    Lieutenant Rain - Precision and survival specialist
    Basic attack: Precision rifle with very slow reload
    Special ability: Survival Mode (speed and reload buff)
    """

    def __init__(self):
        super(Rain, self).__init__()
        self._charging_critical = 0
        self.time_projectile_geration = 0

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

    def choose_ability(self, ability_image):
        return CriticalShot(
            self,
            Constants.ABILITY_SPEED * 3,
            ability_image,
            Constants.ABILITY_DAMAGE
        )

    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.time_projectile_geration += dt
            if self.time_projectile_geration >= 1 / (
                    Constants.PROJECTILE_DEFAULT_FREQUENCY * 0.1):
                self._charging_critical += 1
            if self._charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                self._ready_ability = True

    def _compute_duration_ability(self, dt):
        """
        Updates the duration logic for the character's ability based on character type.

        :param dt: The duration of one iteration.
        """

        if pygame.mouse.get_pressed()[2]:
            self._ready_ability = False
            if self._charging_critical >= Constants.NORMAL_SHOTS_REQUIRED:
                self._charging_critical = 0
                self.time_projectile_geration = 0

    # TODO: Implement special ability - Survival Mode (speed and reload buff)
