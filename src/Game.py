import pygame
from config.Constants import Constants, Sounds
from src.states.Menu import Menu
from src.utils.AudioManager import AudioManager
from config.AvailableTerrains import AvailableTerrains
from entities.players.AbstractPlayer import AbstractPlayer
from entities.Terrain import Terrain
from src.entities.enemies.WavyEnemy import WavyEnemy


class Game:
    """
    Represents the game.
    """

    def __init__(self):
        """
        Initializes the game.
        """
        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__dt = 1 / Constants.FPS
        self.__screen = pygame.display.set_mode(
            (Constants.WIDTH, Constants.HEIGHT))
        self.__is_running = True
        self.__current_state = Menu(self)
        self.__next_state = None
        self.__audio_manager = AudioManager()
        self.__audio_manager.play_music(Sounds.PLAY)

    def run(self):
        """
        Runs the game.
        """
        while self.__is_running:
            self.__clock.tick(Constants.FPS)
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.__is_running = False

            self.__current_state.handle_events(events)
            self.__current_state.update(self.__dt)
            self.__current_state.draw(self.__screen)

            # Check if state change is needed
            if self.__current_state.next_state != self.__current_state:
                self.__next_state = self.__current_state.next_state
                self.__current_state.next_state = self.__current_state
                self.__current_state = self.__next_state
                self.__next_state = None

            pygame.display.flip()
