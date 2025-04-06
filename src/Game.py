import pygame
from config.Constants import Constants
from src.states.Menu import Menu


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
            
            # Verifica se precisa mudar de estado
            if self.__current_state.next_state != self.__current_state:
                self.__next_state = self.__current_state.next_state
                self.__current_state.next_state = self.__current_state  # Reseta o next_state
                self.__current_state = self.__next_state
                self.__next_state = None
            
            pygame.display.flip()
