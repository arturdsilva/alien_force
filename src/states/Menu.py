import pygame
from src.states import GameState
from src.states.CharacterSelect import CharacterSelect
from config.Constants import Constants


class Menu(GameState):
    """
    Main menu game state.
    """
    def __init__(self, game):
        """
        Initializes the main menu.

        :param game: The main game instance.
        """
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Alien Force', True, pygame.Color('white'))
        self.title_rect = self.title.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/4))
        
        self.font_options = pygame.font.Font(None, 54)
        self.start_text = self.font_options.render('Pressione ESPAÇO para iniciar', True, pygame.Color('white'))
        self.start_rect = self.start_text.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT*3/4))

    def update(self, dt):
        """
        Updates the menu state.

        :param dt: Time interval since last update.
        """
        pass

    def draw(self, screen):
        """
        Draws the menu on screen.

        :param screen: The screen surface to draw on.
        """
        screen.fill(pygame.Color('black'))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.start_text, self.start_rect)

    def handle_events(self, events):
        """
        Processes pygame events in menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = CharacterSelect(self.game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.start_rect.collidepoint(event.pos):
                        self.next_state = CharacterSelect(self.game)
