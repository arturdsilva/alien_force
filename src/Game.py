import pygame
from config.Constants import Constants
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
        self.__spawn_timer = 0

        # Terrain
        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.__terrain = Terrain(random_terrain)

        # Sprite Groups
        self.__player = pygame.sprite.GroupSingle(
            AbstractPlayer())  # TODO: create logic to select player
        self.__enemies = pygame.sprite.Group()
        self.__player_projectiles = pygame.sprite.Group()
        self.__enemies_projectiles = pygame.sprite.Group()

    def run(self):
        """
        Runs the game.
        """

        while self.__is_running:
            self.__clock.tick(Constants.FPS)
            self.__handle_events()
            self.__update()
            self.__draw()

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
        self.__enemies_projectiles.update(self.__dt)

        self.__player.update(keys, self.__terrain, self.__dt,
                             self.__player_projectiles,
                             self.__enemies_projectiles)
        self.__enemies.update(self.__dt, self.__player_projectiles,
                              self.__enemies_projectiles,
                              self.__player)

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
        self.__enemies_projectiles.draw(self.__screen)
        pygame.display.flip()

    def __spawn_enemy(self):
        """
        Spawns enemies.
        """

        if len(self.__enemies) < Constants.MAX_ENEMIES:
            self.__enemies.add(WavyEnemy())

    def __game_over(self):
        """
        Ends the game.
        """

        self.__is_running = False
        print("Game Over")
