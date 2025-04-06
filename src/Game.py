import pygame
from config.Constants import Constants
from config.AvailableTerrains import AvailableTerrains
from entities.players.DefaultPlayer import DefaultPlayer
from entities.enemies.AbstractEnemy import AbstractEnemy
from entities.Terrain import Terrain
from src.entities.enemies.WavyEnemy import WavyEnemy
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

    def __handle_events(self):
        """
        Handles pygame events.
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_running = False

    def __update(self):
        """
        Updates the game's entities.
        """

        keys = pygame.key.get_pressed()
        self.__player_projectiles.update(self.__dt)
        self.__player.update(keys, self.__terrain, self.__dt,
                             self.__player_projectiles,
                             self.__enemies_projectiles)
        self.__enemies.update(self.__dt, self.__player_projectiles)

        self.__spawn_timer += self.__dt
        if self.__spawn_timer >= Constants.SPAWN_TIMER:
            self.__spawn_enemy()
            self.__spawn_timer = 0

    def __draw(self):
        """
        Draws game elements on screen.
        """

        self.__screen.fill(Constants.BACKGROUND_COLOR)
        self.__player.draw(self.__screen)
        self.__enemies.draw(self.__screen)
        self.__terrain.draw(self.__screen)
        self.__player_projectiles.draw(self.__screen)
        pygame.display.flip()

    def __spawn_enemy(self):
        """
        Spawns enemies.
        """

        if len(self.__enemies) < Constants.MAX_ENEMIES:
            self.__enemies.add(AbstractEnemy())
            self.__enemies.add(WavyEnemy())
