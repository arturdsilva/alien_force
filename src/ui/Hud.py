import pygame
from config.Constants import Constants


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
        self.font = pygame.font.Font(None, 24)  # Fonte menor (24 em vez de 36)
        
        # Health bar dimensions
        self.health_bar_width = 150  # Barra mais estreita
        self.health_bar_height = 15  # Barra mais baixa
        self.health_bar_x = 20
        self.health_bar_y = 20
        
        # Score position
        self.score_x = Constants.WIDTH - 100  # Ajustado para a fonte menor
        self.score_y = 20
        
        # Colors
        self.health_bar_bg_color = pygame.Color(50, 50, 50)
        self.health_bar_color = pygame.Color(0, 255, 0)  # Green
        self.health_bar_low_color = pygame.Color(255, 0, 0)  # Red
        self.text_color = pygame.Color(255, 255, 255)  # White
    
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
        health_text = self.font.render(f"Health: {self.player._health_points}/{self.player.get_initial_health()}", 
                                      True, self.text_color)
        screen.blit(health_text, (self.health_bar_x, self.health_bar_y - 15))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        screen.blit(score_text, (self.score_x, self.score_y))
    
    def add_score(self, points):
        """
        Adds points to the player's score.
        
        :param points: Points to add.
        """
        self.score += points
