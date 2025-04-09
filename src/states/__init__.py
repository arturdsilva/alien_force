from abc import ABC, abstractmethod
import pygame


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
