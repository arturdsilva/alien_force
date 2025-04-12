import json
import os

import pygame

from config.Constants import Constants
from src.states import GameState


class SaveAndExit(GameState):
    """
    Save and exit menu state used to save progress and exit the game.
    """

    def __init__(self, game, play_state):
        """
        Initializes the save and exit menu.

        :param game: The main game instance.
        :param play_state: The game state that is currently active.
        """
        super().__init__(game)
        self.play_state = play_state  # Store the current play state for later use
        self.next_state = self

        # Font configuration for title and options
        self.font_title = pygame.font.Font(None, 74)
        self.font_options = pygame.font.Font(None, 48)

        # Render the title text (the string remains in Portuguese intentionally)
        self.title = self.font_title.render('Salvar o progresso?', True,
                                            pygame.Color('white'))
        self.title_rect = self.title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))

        # Define the menu options with associated actions
        self.options = [
            {'text': 'Salvar e sair (ENTER)', 'action': self.save_and_exit},
            {'text': 'Sair sem salvar (N)',
             'action': self.exit_without_saving}
        ]

        self.options_surfaces = []
        self.options_rects = []

        # Create surfaces and rectangles for each option to display them centered
        for i, option in enumerate(self.options):
            surface = self.font_options.render(option['text'], True,
                                               pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
            self.options_surfaces.append(surface)
            self.options_rects.append(rect)

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
        # Draw the current game state (displayed in a frozen manner)
        self.play_state.draw(screen)

        # Create a semi-transparent overlay to darken the game screen
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128)  # 50% opacity
        screen.blit(overlay, (0, 0))

        # Draw the save and exit menu title and options on top of the overlay
        screen.blit(self.title, self.title_rect)
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events for the save and exit menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.save_and_exit()
                elif event.key == pygame.K_n:
                    self.exit_without_saving()
            if event.type == pygame.QUIT:
                self.is_running = False

    def save_and_exit(self, file_name="saves/save_game.json"):
        """
        Saves the current play state to a JSON file and exits the game.

        :param file_name: The filename (with path) where the save data will be stored.
        """
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            data = self.play_state.to_dict()

            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

            self.is_running = False

        except (IOError, OSError) as e:
            print("Erro ao salvar o progresso: {}".format(e))
            print("Saindo sem salvar")
            self.exit_without_saving()

    def exit_without_saving(self):
        """
        Exits the game without saving the progress.
        """
        # Simply set the state to not running to exit the game without saving
        self.is_running = False
