import pygame
from config.Constants import Constants
from config.AvailableTerrains import AvailableTerrains
from entities.players.AbstractPlayer import AbstractPlayer
from entities.enemies.AbstractEnemy import AbstractEnemy
from entities.Terrain import Terrain
from src.entities.enemies.WavyEnemy import WavyEnemy


class Game:
    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._dt = 1 / Constants.FPS
        self.screen = pygame.display.set_mode(
            (Constants.WIDTH, Constants.HEIGHT))
        self._is_running = True
        self._spawn_timer = 0

        # Sprite Groups
        self._player = pygame.sprite.GroupSingle(AbstractPlayer())
        self._enemies = pygame.sprite.Group()
        self._projectiles = pygame.sprite.Group()
        terrains = AvailableTerrains()
        terrain = terrains.get_random_terrain()
        self._terrain = Terrain(terrain)

    def run(self):
        while self._is_running:
            self._clock.tick(Constants.FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self._player.update(keys, self._terrain, self._dt, self._projectiles)
        self._enemies.update(self._dt)
        self._projectiles.update(self._dt)

        self._spawn_timer += self._dt
        if self._spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self._spawn_timer = 0

    def draw(self):
        self.screen.fill(Constants.BACKGROUND_COLOR)
        self._player.draw(self.screen)
        self._enemies.draw(self.screen)
        self._terrain.draw(self.screen)
        self._projectiles.draw(self.screen)
        pygame.display.flip()

    def spawn_enemy(self):
        if len(self._enemies) < Constants.MAX_ENEMIES:
            self._enemies.add(AbstractEnemy())
            self._enemies.add(WavyEnemy())
