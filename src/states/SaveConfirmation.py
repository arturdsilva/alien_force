import pygame
import json
import os

from config.Constants import Constants, Sounds
from src.states.GameState import GameState
from src.states.Menu import Menu
from src.utils.AudioManager import AudioManager


class SaveConfirmation(GameState):
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
        self.play_state = play_state
        self.return_to_menu_after_saving = return_to_menu_after_saving
        self.next_state = self
        self.__audio_manager = AudioManager()

        # Font configuration for title and options
        self.font_title = pygame.font.Font(None, 74)
        self.font_options = pygame.font.Font(None, 48)

        # Render the title text
        self.title = self.font_title.render('Salvar o progresso?', True,
                                            pygame.Color('white'))
        self.title_rect = self.title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))

        # Define the menu options with associated actions
        self.options = [
            {'text': 'Salvar', 'action': self.save_and_leave_session},
            {'text': 'Sair sem salvar',
             'action': self.leave_session}
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
                    self.save_and_leave_session()
                elif event.key == pygame.K_n:
                    self.leave_session()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.options_rects):
                        if rect.collidepoint(event.pos):
                            self.options[i]['action']()
            if event.type == pygame.QUIT:
                self.is_running = False

    def save_and_leave_session(self, file_name="saves/save_game.json"):
        """
        Saves the current game progress to a file and leaves the session.

        :param file_name: The path to the save file.
        """
        self.__audio_manager.play_sound(Sounds.CLICK)
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            data = self.play_state.to_dict()

            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

        except (IOError, OSError) as e:
            print("Erro ao salvar o progresso: {}".format(e))

        self.leave_session()

    def leave_session(self):
        """
        Exits the game without saving the progress.
        """
        self.__audio_manager.play_sound(Sounds.CLICK)
        if self.return_to_menu_after_saving:
            self.next_state = Menu(self.game)
            self.__audio_manager.unpause_music()
        else:
            self.is_running = False
