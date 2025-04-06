import pygame
from src.states import GameState
from config.Constants import Constants
from config.AvailableTerrains import AvailableTerrains
from entities.enemies.AbstractEnemy import AbstractEnemy
from entities.Terrain import Terrain
from src.entities.enemies.WavyEnemy import WavyEnemy


class Play(GameState):
    """
    Estado do jogo em andamento.
    """
    def __init__(self, game, player):
        super().__init__(game)
        self.spawn_timer = 0

        # Terrain
        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.terrain = Terrain(random_terrain)

        # Posiciona o player no centro-x e na parte inferior da tela
        player.rect.centerx = Constants.WIDTH / 2
        player.rect.bottom = Constants.HEIGHT

        # Sprite Groups
        self.player = pygame.sprite.GroupSingle(player)
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemies_projectiles = pygame.sprite.Group()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player_projectiles.update(dt)
        self.player.update(keys, self.terrain, dt,
                          self.player_projectiles,
                          self.enemies_projectiles)
        self.enemies.update(dt, self.player_projectiles)

        self.spawn_timer += dt
        if self.spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self.spawn_timer = 0

    def draw(self, screen):
        screen.fill(Constants.BACKGROUND_COLOR)
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.terrain.draw(screen)
        self.player_projectiles.draw(screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.states.Pause import Pause
                    self.next_state = Pause(self.game, self)

    def spawn_enemy(self):
        """
        Spawns enemies.
        """
        if len(self.enemies) < Constants.MAX_ENEMIES:
            self.enemies.add(AbstractEnemy())
            self.enemies.add(WavyEnemy())
