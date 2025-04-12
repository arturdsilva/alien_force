import pygame

from config.Constants import Constants
from src.entities.Ability import LaserBeam
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

    def choose_ability(self, ability_image):
        return LaserBeam(
            self,
            Constants.ABILITY_DAMAGE,
            Constants.LASER_DURATION,
            Constants.LASER_WIDTH,
            Constants.COLOR_LASER,
            Constants.LASER_LIFETIME
        )

    def _compute_cooldown_ability(self, dt):
        """
        Updates the cooldown timer for the character's special ability.

        :param dt: The duration of one iteration.
        """
        if not self._ready_ability:
            self._time_cooldown_ability += dt
            if self._time_cooldown_ability >= Constants.ABILITY_COOLDOWN:
                self._ready_ability = True
                self._time_cooldown_ability = 0

    def _compute_duration_ability(self, dt):
        """
        Updates the duration logic for the character's ability based on character type.

        :param dt: The duration of one iteration.
        """

        if pygame.mouse.get_pressed()[2]:
            self._time_duration_ability += dt
            if self._time_duration_ability >= Constants.ABILITY_DURATION:
                self._time_duration_ability = 0
                self._ready_ability = False
