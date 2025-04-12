from abc import ABC, abstractmethod
import json
import os


class GameState(ABC):
    """
    Abstract base class for game states.
    """

    def __init__(self, game):
        """
        Initializes a game state.

        :param game: The main game instance.
        """
        self.game = game
        self.next_state = self
        self.is_running = True
        self.load_from_save = False

    def save(self, play_state, file_name="saves/save_game.json"):
        """
        Saves the current game progress to a file.

        :param play_state: The current play state to be saved.
        :param file_name: The path to the save file.
        :return: True if the save was successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(file_name), exist_ok=True)

            data = play_state.to_dict()

            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

            return True

        except (IOError, OSError) as e:
            print("Erro ao salvar o progresso: {}".format(e))
            return False

    @abstractmethod
    def update(self, dt):
        """
        Updates the state.

        :param dt: Time interval since last update.
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Draws the state on screen.

        :param screen: The screen surface to draw on.
        """
        pass

    @abstractmethod
    def handle_events(self, events):
        """
        Processes pygame events.

        :param events: List of pygame events to process.
        """
        pass
