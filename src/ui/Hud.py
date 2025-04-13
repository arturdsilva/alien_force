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
        self.player = player
        self.score = 0
        self.font = pygame.font.Font(None, 24)  # Smaller font (24 instead of 36)

        # No loop principal do jogo:


        # Health bar dimensions
        self.health_bar_width = 150  # Narrower bar
        self.health_bar_height = 15  # Lower bar
        self.health_bar_x = 20
        self.health_bar_y = 20

        # Cooldown ability bar dimensions
        self.time_cooldown_bar_width = 150  # Narrower bar
        self.time_cooldown_bar_height = 15  # Lower bar
        self.time_cooldown_bar_x = 20
        self.time_cooldown_bar_y = 60

        # Score position
        self.score_x = Constants.WIDTH - 100  # Adjusted for smaller font
        self.score_y = 20

        # Colors
        self.health_bar_bg_color = Colors.DARK_GRAY
        self.health_bar_color = Colors.GREEN
        self.health_bar_low_color = Colors.RED
        self.text_color = Colors.WHITE
        self.time_cooldown_bar_bg_color = Colors.DARK_GRAY
        self.time_cooldown_bar_color = Colors.BLUE
        self.time_cooldown_bar_ready_color = Colors.LIGHT_BLUE

    def update(self, dt):
        """
        Updates the HUD state.
        
        :param dt: Time since last update.
        """
        # Update score based on player actions or game events
        # This could be expanded based on game mechanics
        pass

    def draw(self, screen):
        """
        Draws the HUD on the screen.
        
        :param screen: The screen surface to draw on.
        """
        # Draw health bar background
        pygame.draw.rect(screen, self.health_bar_bg_color,
                         (self.health_bar_x, self.health_bar_y,
                          self.health_bar_width, self.health_bar_height))

        # Calculate health percentage
        health_percentage = self.player._health_points / self.player.get_initial_health()
        health_width = int(self.health_bar_width * health_percentage)

        # Choose color based on health level
        health_color = self.health_bar_color
        if health_percentage < 0.3:  # Less than 30% health
            health_color = self.health_bar_low_color

        # Draw health bar
        if health_width > 0:
            pygame.draw.rect(screen, health_color,
                             (self.health_bar_x, self.health_bar_y,
                              health_width, self.health_bar_height))

        # Draw health text
        health_text = self.font.render(
            f"Health: {self.player._health_points}/{self.player.get_initial_health()}",
            True, self.text_color)
        screen.blit(health_text, (self.health_bar_x, self.health_bar_y - 15))

        # Calculate time cooldown percentage
        time_cooldown_percentage = self.player.get_time_cooldown_ability() / Constants.ABILITY_COOLDOWN
        time_cooldown_width = self.time_cooldown_bar_width * time_cooldown_percentage

        # Draw time cooldown bar background
        pygame.draw.rect(screen, self.time_cooldown_bar_bg_color,
                         (self.time_cooldown_bar_x, self.time_cooldown_bar_y,
                          self.time_cooldown_bar_width,
                          self.time_cooldown_bar_height))
        if self.player.get_ready_ability() and self.player.get_time_cooldown_ability() >= Constants.ABILITY_COOLDOWN:
            pygame.draw.rect(screen, self.time_cooldown_bar_ready_color,
                             (self.time_cooldown_bar_x, self.time_cooldown_bar_y,
                              self.time_cooldown_bar_width, self.time_cooldown_bar_height))
        else:
            # Choose color based on time cooldown level
            time_cooldown_color = self.time_cooldown_bar_color

            # Draw time cooldown bar
            if time_cooldown_width >= 0:
                pygame.draw.rect(screen, time_cooldown_color,
                                 (self.time_cooldown_bar_x, self.time_cooldown_bar_y,
                                  time_cooldown_width, self.time_cooldown_bar_height))

        # Draw time cooldown text
        time_cooldown_text = self.font.render(
            f"Ability: {int(time_cooldown_percentage * 100)} %",
            True, self.text_color)
        screen.blit(time_cooldown_text, (self.time_cooldown_bar_x, self.time_cooldown_bar_y - 15))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True,
                                      self.text_color)
        screen.blit(score_text, (self.score_x, self.score_y))

    def add_score(self, points):
        """
        Adds points to the player's score.
        
        :param points: Points to add.
        """
        self.score += points 