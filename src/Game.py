import pygame
import numpy as np
from config.Constants import Constants
from config.AvailableTerrains import AvailableTerrains
from entities.players.AbstractPlayer import AbstractPlayer
from entities.enemies.AbstractEnemy import AbstractEnemy
from entities.Terrain import Terrain


# from states.Menu import Menu


# from entities.players.AbstractPlayer import AbstractPlayer


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.dt = 1 / Constants.FPS
        self.screen = pygame.display.set_mode(
            (Constants.WIDTH, Constants.HEIGHT))
        self.running = True
        self.spawn_timer = 0

        # Sprite Groups
        self.player = pygame.sprite.GroupSingle(AbstractPlayer())
        self.enemies = pygame.sprite.Group()
        map_terrains = AvailableTerrains()
        terrain = map_terrains.get_random_terrain()
        print(terrain[0])
        self.map = Terrain(terrain)


    def run(self):
        while self.running:
            self.clock.tick(Constants.FPS)
            self.handle_events()
            self.update()
            self.draw()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.map, self.dt)
        self.enemies.update(self.dt)

        self.spawn_timer += self.dt
        if self.spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self.spawn_timer = 0


    def draw(self):
        self.screen.fill("purple")
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.map.draw(self.screen)
        pygame.display.flip()


    def spawn_enemy(self):
        self.enemies.add(AbstractEnemy())