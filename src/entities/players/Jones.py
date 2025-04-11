import pygame

from config.Constants import Constants
from src.entities.Ability import MissileBarrage
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

    def choose_ability_generator(self, ability_image):
        return MissileBarrage(
            self,
            Constants.ABILITY_SPEED,
            ability_image,
            Constants.ABILITY_DAMAGE,
            Constants.MISSILE_SHOT_CAPACITY
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
            self._ready_ability = False

    # TODO: Implement area damage for grenades
