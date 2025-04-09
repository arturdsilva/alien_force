import pygame
from src.states import GameState
from config.Constants import Constants


class Pause(GameState):
    """
    Game pause state.
    """
    def __init__(self, game, play_state):
        """
        Initializes the pause menu.

        :param game: The main game instance.
        :param play_state: The game state that was paused.
        """
        super().__init__(game)
        self.play_state = play_state  # Stores the game state to return to
        self.next_state = self 
        
        # Font configuration
        self.font_title = pygame.font.Font(None, 74)
        self.font_options = pygame.font.Font(None, 48)
        
        # Título
        self.title = self.font_title.render('PAUSADO', True, pygame.Color('white'))
        self.title_rect = self.title.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/3))
        
        # Options
        self.options = [
            {'text': 'Continuar (P)', 'action': self.resume_game},
            {'text': 'Menu Principal (ESC)', 'action': self.return_to_menu}
        ]
        
        self.options_surfaces = []
        self.options_rects = []
        
        for i, option in enumerate(self.options):
            surface = self.font_options.render(option['text'], True, pygame.Color('white'))
            rect = surface.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2 + i * 60))
            self.options_surfaces.append(surface)
            self.options_rects.append(rect)

    def update(self, dt):
        """
        Updates the pause menu state.

        :param dt: Time interval since last update.
        """
        pass

    def draw(self, screen):
        """
        Draws the pause menu.

        :param screen: The screen surface to draw on.
        """
        # Draw current game state (frozen)
        self.play_state.draw(screen)
        
        # Create semi-transparent surface to darken the game
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128)  # 128 is 50% opacity
        screen.blit(overlay, (0, 0))
        
        # Draw pause menu
        screen.blit(self.title, self.title_rect)
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events in pause menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.resume_game()
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu()

    def resume_game(self):
        """
        Returns to the paused game.
        """
        self.next_state = self.play_state

    def return_to_menu(self):
        """
        Returns to the main menu.
        """
        from src.states.Menu import Menu
        self.next_state = Menu(self.game)
