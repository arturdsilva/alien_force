import random
import pygame
from config.AvailableTerrains import AvailableTerrains
from config.Constants import Constants
from src.entities.Terrain import Terrain
from src.entities.enemies.BouncingEnemy import BouncingEnemy
from src.entities.enemies.LinearEnemy import LinearEnemy
from src.entities.enemies.TankEnemy import TankEnemy
from src.entities.enemies.WavyEnemy import WavyEnemy
from src.states import GameState
from src.states.Pause import Pause
from src.ui.Hud import Hud


class Play(GameState):
    """
    Estado do jogo em andamento.
    """

    def __init__(self, game, player):
        """
        Inicializa o estado de jogo.

        :param game: Instância principal do jogo.
        :param player: Personagem selecionado.
        """
        super().__init__(game)
        self.spawn_timer = 0
        self.__speed_multiplier = 1.0

        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.__terrain = Terrain(random_terrain)

        player.rect.centerx = Constants.WIDTH / 2
        player.rect.bottom = 0

        self.__player = pygame.sprite.GroupSingle(player)
        self.__enemies = pygame.sprite.Group()
        self.__player_projectiles = pygame.sprite.Group()
        self.__enemies_projectiles = pygame.sprite.Group()
        self.__abilities = pygame.sprite.Group()

        self.hud = Hud(player)

        self.bg_image = pygame.image.load("assets/sprites/Background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (Constants.WIDTH, Constants.HEIGHT))

        self._adjust_player_initial_position()

    def _adjust_player_initial_position(self):
        """
        Ajusta a posição inicial do player para ficar sobre o terreno.
        """
        player = self.__player.sprite
        while player.rect.bottom < Constants.HEIGHT:
            player.rect.y += 1
            hits = pygame.sprite.spritecollide(player, self.__terrain, False)
            if hits:
                player.rect.bottom = hits[0].rect.top
                break

    def update(self, dt):
        """
        Atualiza o estado do jogo.

        :param dt: Intervalo de tempo desde a última atualização.
        """
        keys = pygame.key.get_pressed()
        self.__player_projectiles.update(dt)
        self.__enemies_projectiles.update(dt, self.__speed_multiplier)
        self.__abilities.update(dt, self.__speed_multiplier)

        self.__player.update(keys, self.__terrain, dt,
                             self.__player_projectiles,
                             self.__enemies_projectiles, self.__abilities)

        self.__enemies.update(dt, self.__player_projectiles,
                              self.__enemies_projectiles,
                              self.__player, self.__terrain,
                              self.__speed_multiplier)

        self.hud.update(dt)

        for enemy in self.__enemies.sprites():
            if enemy.health <= 0:
                if isinstance(enemy, TankEnemy):
                    self.hud.add_score(100)
                elif isinstance(enemy, WavyEnemy):
                    self.hud.add_score(50)
                elif isinstance(enemy, LinearEnemy):
                    self.hud.add_score(30)
                elif isinstance(enemy, BouncingEnemy):
                    self.hud.add_score(40)
                enemy.kill()

        self.spawn_timer += dt
        if self.spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self.spawn_timer = 0

        if self.__speed_multiplier < Constants.SPEED_MULTIPLIER_LIMIT:
            self.__speed_multiplier += Constants.DIFFICULTY_FACTOR

    def draw(self, screen):
        """
        Desenha o estado do jogo na tela.

        :param screen: A superfície da tela para desenhar.
        """
        screen.blit(self.bg_image, (0, 0))

        self.__terrain.draw(screen)
        for player in self.__player:
            player.draw(screen)
        self.__enemies.draw(screen)
        self.__player_projectiles.draw(screen)
        self.__enemies_projectiles.draw(screen)
        self.__abilities.draw(screen)

        self.hud.draw(screen)

    def handle_events(self, events):
        """
        Processa os eventos do pygame.

        :param events: Lista de eventos para processar.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    self.next_state = Pause(self.game, self)

    def spawn_enemy(self):
        """
        Gera inimigos aleatórios quando apropriado.
        """
        if len(self.__enemies) < Constants.MAX_ENEMIES:
            enemy_types = [
                (WavyEnemy, 30),
                (LinearEnemy, 30),
                (BouncingEnemy, 25),
                (TankEnemy, 15)
            ]
            enemy_class = random.choices(
                [et[0] for et in enemy_types],
                weights=[et[1] for et in enemy_types]
            )[0]
            self.__enemies.add(enemy_class())
