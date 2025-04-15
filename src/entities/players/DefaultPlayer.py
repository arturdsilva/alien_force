from config.Constants import Constants
from src.entities.players.AbstractPlayer import AbstractPlayer


class DefaultPlayer(AbstractPlayer):
    """
    Default implementation of AbstractPlayer.
    """

    def get_player_color(self):
        return Constants.PLAYER_DEFAULT_COLOR

    def get_initial_health(self):
        return Constants.PLAYER_MAX_HEALTH

    def get_projectile_color(self):
        return Constants.PROJECTILE_DEFAULT_COLOR

    def get_projectile_speed(self):
        return Constants.PROJECTILE_DEFAULT_SPEED

    def get_projectile_frequency(self):
        return Constants.PROJECTILE_DEFAULT_FREQUENCY

    def get_projectile_damage(self):
        return Constants.PROJECTILE_DEFAULT_DAMAGE

    def get_ability_time_left(self):
        return int(self.time_cooldown_ability)
