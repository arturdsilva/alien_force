from abc import ABC, abstractmethod


class AbstractState(ABC):
    """
    Abstract base class for game states.
    """

    def __init__(self, game):
        """
        Initializes a game state.

        :param game: The main game instance.
        """
        self._game = game
        self._next_state = self
        self._is_running = True
        self._load_from_save = False

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

    @property
    def next_state(self):
        """
         Gets the next state to transition to.

         :return: The next GameState instance.
         """
        return self._next_state

    @next_state.setter
    def next_state(self, next_state):
        """
        Sets the next state to transition to.

        :param next_state: The GameState instance to set as the next state.
        """
        self._next_state = next_state

    @property
    def is_running(self):
        """
        Indicates whether the game is still active.

        :return: True if the state is running, False otherwise.
        """
        return self._is_running

    @property
    def load_from_save(self):
        """
        Indicates whether the state should load data from a saved game.

        :return: True if the state should load from a save, False otherwise.
        """
        return self._load_from_save
