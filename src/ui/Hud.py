import pygame

from config.Constants import Constants
from config.Constants import Colors


class Hud:
    """
    Heads-Up Display (HUD) for the game.
    Displays player health and score.
    """

    def __init__(self, player):
        """
        Initializes the HUD.
        
        :param player: The player sprite to track.
        """
        self.__player = player
        self.__score = 0
        self.__font = pygame.font.Font(None, 24)  # Smaller font (24 instead of 36)

        # Health bar dimensions
        self.__health_bar_width = 150  # Narrower bar
        self.__health_bar_height = 15  # Lower bar
        self.__health_bar_x = 20
        self.__health_bar_y = 20

        # Ability bar
        self.__ability_bar_width = 150  # Narrower bar
        self.__ability_bar_height = 15  # Lower bar
        self.__ability_bar_x = 20
        self.__ability_bar_y = 60
        self.__ability_cooldown = player.get_ability_cooldown()

        # Score position
        self.__score_x = Constants.WIDTH - 100  # Adjusted for smaller font
        self.__score_y = 20

        # Colors
        self.__health_bar_bg_color = Colors.DARK_GRAY
        self.__health_bar_color = Colors.GREEN
        self.__health_bar_low_color = Colors.RED
        self.__text_color = Colors.WHITE
        self.__ability_bar_bg_color = Colors.DARK_GRAY
        self.__ability_bar_color = Colors.BLUE
        self.__ability_bar_full_color = Colors.LIGHT_BLUE

    def draw(self, screen):
        """
        Draws the HUD on the screen.
        
        :param screen: The screen surface to draw on.
        """
        # Draw health bar background
        pygame.draw.rect(screen, self.__health_bar_bg_color,
                         (self.__health_bar_x, self.__health_bar_y,
                          self.__health_bar_width, self.__health_bar_height))

        # Calculate health percentage
        health_percentage = self.__player.health_points / self.__player.get_initial_health()
        health_width = int(self.__health_bar_width * health_percentage)

        # Choose color based on health level
        health_color = self.__health_bar_color
        if health_percentage < 0.3:  # Less than 30% health
            health_color = self.__health_bar_low_color

        # Draw health bar
        if health_width > 0:
            pygame.draw.rect(screen, health_color,
                             (self.__health_bar_x, self.__health_bar_y,
                              health_width, self.__health_bar_height))

        # Draw health text
        health_text = self.__font.render(
            f"Health: {self.__player.health_points}/{self.__player.get_initial_health()}",
            True, self.__text_color)
        screen.blit(health_text, (self.__health_bar_x, self.__health_bar_y - 15))

        # Calculate time cooldown percentage
        if self.__player.has_durable_ability:
            ability_duration_percentage = (self.__player.get_ability_time_left()
                                           / self.__player.get_ability_duration())
        else:
            ability_duration_percentage = 1
        ability_duration_width = self.__ability_bar_width * ability_duration_percentage

        ability_cooldown_percentage = (self.__player.get_ability_downtime() /
                                       self.__player.get_ability_cooldown())
        ability_cooldown_width = (self.__ability_bar_width *
                                  ability_cooldown_percentage)

        # Draw time cooldown bar background
        pygame.draw.rect(screen, self.__ability_bar_bg_color,
                         (self.__ability_bar_x, self.__ability_bar_y,
                          self.__ability_bar_width,
                          self.__ability_bar_height))
        # Draw time cooldown bar
        if self.__player.get_ready_ability():
                if ability_duration_percentage >= 1:
                    pygame.draw.rect(screen, self.__ability_bar_full_color,
                                     (self.__ability_bar_x,
                                  self.__ability_bar_y,
                                  self.__ability_bar_width,
                                  self.__ability_bar_height))
                elif self.__player.has_durable_ability:
                    pygame.draw.rect(screen, self.__ability_bar_color,
                                     (self.__ability_bar_x,
                                  self.__ability_bar_y,
                                  ability_duration_width,
                                  self.__ability_bar_height))
        else:
            pygame.draw.rect(screen, self.__ability_bar_color,
                             (self.__ability_bar_x,
                              self.__ability_bar_y,
                              ability_cooldown_width,
                              self.__ability_bar_height))

        # Draw time cooldown text
        if self.__player.get_ready_ability():
            percentage = ability_duration_percentage
        else:
            percentage = ability_cooldown_percentage
        time_cooldown_text = self.__font.render(
            f"Ability: {int(percentage * 100)} %",
            True, self.__text_color)
        screen.blit(time_cooldown_text, (self.__ability_bar_x, self.__ability_bar_y - 15))

        # Draw score
        score_text = self.__font.render(f"Score: {self.__score}", True,
                                        self.__text_color)
        screen.blit(score_text, (self.__score_x, self.__score_y))

    def add_score(self, points):
        """
        Adds points to the player's score.
        
        :param points: Points to add.
        """
        self.__score += points

    @property
    def score(self):
        return self.__score