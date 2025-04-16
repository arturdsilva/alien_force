import json
import os

import pygame

from config.Constants import Constants, Sounds
from src.states.AbstractState import AbstractState
from src.states.Menu import Menu
from src.utils.AudioManager import AudioManager


class SaveConfirmation(AbstractState):
    """
    Save and exit menu state used to save progress and exit the game.
    """

    def __init__(self, game, play_state, return_to_menu_after_saving):
        """
        Initializes the save and exit menu.

        :param game: The main game instance.
        :param play_state: The game state that is currently active.
        """
        super().__init__(game)
        self.__play_state = play_state
        self.__return_to_menu_after_saving = return_to_menu_after_saving
        self._next_state = self
        self.__audio_manager = AudioManager()

        # Font configuration for title and options
        self.__font_title = pygame.font.Font(None, 74)
        self.__font_options = pygame.font.Font(None, 48)

        # Render the title text
        self.__title = self.__font_title.render('Salvar o progresso?', True,
                                                pygame.Color('white'))
        self.__title_rect = self.__title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))

        # Define the menu options with associated actions
        self.__options = [
            {'text': 'Salvar', 'action': self.__save_and_leave_session},
            {'text': 'Sair sem salvar',
             'action': self.__leave_session}
        ]

        self.__options_surfaces = []
        self.__options_rects = []

        # Create surfaces and rectangles for each option to display them centered
        for i, option in enumerate(self.__options):
            surface = self.__font_options.render(option['text'], True,
                                                 pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
            self.__options_surfaces.append(surface)
            self.__options_rects.append(rect)

    def update(self, dt):
        """
        Updates the save and exit menu state.

        :param dt: Time interval since the last update.
        """
        # TODO: Implement any necessary update logic for the save and exit menu if needed.
        pass

    def draw(self, screen):
        """
        Draws the save and exit menu on the given screen.

        :param screen: The screen surface to draw on.
        """
        self.__play_state.draw(screen)

        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        screen.blit(self.__title, self.__title_rect)
        for surface, rect in zip(self.__options_surfaces,
                                 self.__options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events for the save and exit menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.__save_and_leave_session()
                elif event.key == pygame.K_n:
                    self.__leave_session()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.__options_rects):
                        if rect.collidepoint(event.pos):
                            self.__options[i]['action']()
            if event.type == pygame.QUIT:
                self._is_running = False

    def __save_and_leave_session(self, file_name="saves/save_game.json"):
        """
        Saves the current game progress to a file and leaves the session.

        :param file_name: The path to the save file.
        """
        self.__audio_manager.play_sound(Sounds.CLICK)
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            data = self.__play_state.to_dict()

            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

        except (IOError, OSError) as e:
            print("Erro ao salvar o progresso: {}".format(e))

        self.__leave_session()

    def __leave_session(self):
        """
        Exits the game without saving the progress.
        """
        self.__audio_manager.play_sound(Sounds.CLICK)
        if self.__return_to_menu_after_saving:
            self._next_state = Menu(self._game)
            self.__audio_manager.unpause_music()
        else:
            self._is_running = False
