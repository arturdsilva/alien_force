import pygame

from config.Constants import Constants, Sounds
from src.utils.AudioManager import AudioManager
from src.states.AbstractState import AbstractState


class Pause(AbstractState):
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
        self.__play_state = play_state  # Stores the game state to return to
        self._next_state = self
        self.__audio_manager = AudioManager()

        # Font configuration
        self.__font_title = pygame.font.Font(None, 74)
        self.__font_options = pygame.font.Font(None, 48)

        # Title
        self.__title = self.__font_title.render('PAUSADO', True,
                                                pygame.Color('white'))
        self.__title_rect = self.__title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))

        # Options
        self.__options = [
            {'text': 'Continuar', 'action': self.__resume_game},
            {'text': 'Menu Principal', 'action': self.__return_to_menu}
        ]

        self.__options_surfaces = []
        self.__options_rects = []

        for i, option in enumerate(self.__options):
            surface = self.__font_options.render(option['text'], True,
                                                 pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
            self.__options_surfaces.append(surface)
            self.__options_rects.append(rect)

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
        self.__play_state.draw(screen)

        # Create semi-transparent surface to darken the game
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128)  # 128 is 50% opacity
        screen.blit(overlay, (0, 0))

        # Draw pause menu
        screen.blit(self.__title, self.__title_rect)
        for surface, rect in zip(self.__options_surfaces, self.__options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events in pause menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                from src.states.SaveConfirmation import SaveConfirmation
                self._next_state = SaveConfirmation(self._game, self.__play_state,
                                                    False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__resume_game()
                elif event.key == pygame.K_m:
                    self.__return_to_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    for i, rect in enumerate(self.__options_rects):
                        if rect.collidepoint(mouse_pos):
                            self.__options[i]['action']()

    def __resume_game(self):
        """
        Returns to the paused game.
        """
        self._next_state = self.__play_state

        self.__audio_manager.unpause_music()
        self.__audio_manager.play_sound(Sounds.CLICK)

    def __return_to_menu(self):
        """
        Returns to the main menu.
        """
        from src.states.SaveConfirmation import SaveConfirmation
        self._next_state = SaveConfirmation(self._game, self.__play_state, True)
        self.__audio_manager.play_sound(Sounds.CLICK)
