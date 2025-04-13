import pygame

from config.Constants import Constants, Sounds
from src.utils.AudioManager import AudioManager
from src.states.GameState import GameState


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
        self.__audio_manager = AudioManager()

        # Font configuration
        self.font_title = pygame.font.Font(None, 74)
        self.font_options = pygame.font.Font(None, 48)

        # Título
        self.title = self.font_title.render('PAUSADO', True,
                                            pygame.Color('white'))
        self.title_rect = self.title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))

        # Options
        self.options = [
            {'text': 'Continuar (ESC)', 'action': self.resume_game},
            {'text': 'Menu Principal (M)', 'action': self.return_to_menu}
        ]

        self.options_surfaces = []
        self.options_rects = []

        for i, option in enumerate(self.options):
            surface = self.font_options.render(option['text'], True,
                                               pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
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
            if event.type == pygame.QUIT:
                from src.states.SaveConfirmation import SaveConfirmation
                self.next_state = SaveConfirmation(self.game, self.play_state,
                                                   False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.resume_game()
                    self.__audio_manager.unpause_music()
                    self.__audio_manager.play_sound(Sounds.CLICK)
                elif event.key == pygame.K_m:
                    self.return_to_menu()
                    self.__audio_manager.unpause_music()
                    self.__audio_manager.play_sound(Sounds.CLICK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    for i, rect in enumerate(self.options_rects):
                        if rect.collidepoint(mouse_pos):
                            self.options[i]['action']()

    def resume_game(self):
        """
        Returns to the paused game.
        """
        self.next_state = self.play_state

    def return_to_menu(self):
        """
        Returns to the main menu.
        """
        from src.states.SaveConfirmation import SaveConfirmation
        self.next_state = SaveConfirmation(self.game, self.play_state, True)
