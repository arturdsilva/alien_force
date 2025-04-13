import pygame

from config.Constants import Constants
from src.entities.Ability import CriticalShot
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
        self.time_projectile_generation = 0

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

    def choose_ability(self):
        return CriticalShot(self)

    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            self.time_projectile_generation += dt
            if self.time_projectile_generation >= 1 / (
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
                self.time_projectile_generation = 0

    # TODO: Implement special ability - Survival Mode (speed and reload buff)

    def to_dict(self):
        """
        Converts the player's state into a dictionary, including Rain-specific attributes.
        """
        data = super().to_dict()
        data["charging_critical"] = self._charging_critical
        data["time_projectile_geration"] = self.time_projectile_generation
        return data

    # TODO: Implement special ability - Survival Mode (speed and reload buff)
    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of Rain from a dictionary.
        """
        instance = cls()
        instance.rect.centerx = data["centerx"]
        instance.rect.bottom = data["bottom"]
        instance._health_points = data["health"]
        instance._is_jumping = data["is_jumping"]
        instance._y_speed = data["y_speed"]
        instance._ready_ability = data["ready_ability"]
        instance._time_cooldown_ability = data["time_cooldown_ability"]
        instance._time_duration_ability = data["time_duration_ability"]
        instance._charging_critical = data.get("charging_critical", 0)
        instance.time_projectile_generation = data.get(
            "time_projectile_geration", 0)
        return instance
