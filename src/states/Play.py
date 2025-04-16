import random

import pygame

from config.AvailableTerrains import AvailableTerrains
from config.Constants import Constants, Sounds
from src.entities.Terrain import Terrain
from src.entities.enemies.BouncingEnemy import BouncingEnemy
from src.entities.enemies.EnemyClassMap import EnemyClassMap
from src.entities.enemies.LinearEnemy import LinearEnemy
from src.entities.enemies.TankEnemy import TankEnemy
from src.entities.enemies.WavyEnemy import WavyEnemy
from src.entities.players.PlayerClassMap import PlayerClassMap
from src.states.AbstractState import AbstractState
from src.states.Pause import Pause
from src.ui.Hud import Hud
from src.utils.AudioManager import AudioManager


class Play(AbstractState):
    """
    Game in progress state.
    """

    def __init__(self, game, player_name):
        """
        Initializes the game state.

        :param game: The main game instance.
        :param player_name: The character selected by the player.
        """
        super().__init__(game)
        self.__spawn_timer = 0
        self.__audio_manager = AudioManager()
        self.__speed_multiplier = 1.0

        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.__terrain = Terrain(random_terrain)

        self.__player_name = player_name
        player = PlayerClassMap[self.__player_name]()
        player.rect.centerx = Constants.WIDTH / 2
        player.rect.bottom = 0

        self.__player = pygame.sprite.GroupSingle(player)
        self.__enemies = pygame.sprite.Group()
        self.__player_projectiles = pygame.sprite.Group()
        self.__enemies_projectiles = pygame.sprite.Group()
        self.__abilities = pygame.sprite.Group()

        self.__hud = Hud(player)

        self.__bg_image = pygame.image.load(
            "assets/sprites/Background.png").convert()
        self.__bg_image = pygame.transform.scale(self.__bg_image, (
            Constants.WIDTH, Constants.HEIGHT))

        self.__adjust_player_initial_position()

    def __adjust_player_initial_position(self):
        """
        Adjusts the initial player position to be on terrain.
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
        Updates the game state.

        :param dt: Time since last update.
        """
        keys = pygame.key.get_pressed()

        player = self.__player.sprite
        self.__player_projectiles.update(dt, self.__terrain, player)
        self.__enemies_projectiles.update(dt, self.__terrain, player)
        self.__abilities.update(dt, self.__speed_multiplier)

        self.__player.update(keys, self.__terrain, dt,
                             self.__player_projectiles,
                             self.__enemies_projectiles, self.__abilities)

        self.__enemies.update(dt, self.__player_projectiles, self.__abilities,
                              self.__enemies_projectiles,
                              self.__player, self.__terrain,
                              self.__speed_multiplier)

        for enemy in self.__enemies.sprites():
            if enemy.health <= 0:
                if isinstance(enemy, TankEnemy):
                    self.__hud.add_score(100)
                elif isinstance(enemy, WavyEnemy):
                    self.__hud.add_score(50)
                elif isinstance(enemy, LinearEnemy):
                    self.__hud.add_score(30)
                elif isinstance(enemy, BouncingEnemy):
                    self.__hud.add_score(40)
                enemy.kill()
                self.__audio_manager.play_sound(Sounds.DEATH)

        if player.health_points <= 0:
            from src.states.GameOver import GameOver
            self._next_state = GameOver(self._game, self.__hud.score,
                                        self.__player_name)
            self.__audio_manager.pause_music()
            self.__audio_manager.play_sound(Sounds.GAME_OVER)

        self.__spawn_timer += dt
        if self.__spawn_timer >= Constants.SPAWN_TIMER:
            self.__spawn_enemy()
            self.__spawn_timer = 0

        if self.__speed_multiplier < Constants.SPEED_MULTIPLIER_LIMIT:
            self.__speed_multiplier += Constants.DIFFICULTY_FACTOR

    def draw(self, screen):
        """
        Draws the game state.

        :param screen: The screen surface to draw on.
        """
        screen.blit(self.__bg_image, (0, 0))

        self.__terrain.draw(screen)

        for projectile in self.__player_projectiles:
            projectile.draw(screen)
        for player in self.__player:
            player.draw(screen)
        self.__enemies.draw(screen)
        for projectile in self.__enemies_projectiles:
            projectile.draw(screen)

        self.__abilities.draw(screen)

        self.__hud.draw(screen)

    def handle_events(self, events):
        """
        Processes pygame events during the game.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    self._next_state = Pause(self._game, self)
                    self.__audio_manager.pause_music()
                    self.__audio_manager.play_sound(Sounds.CLICK)
            if event.type == pygame.QUIT:
                self.__audio_manager.pause_music()
                self.__audio_manager.play_sound(Sounds.CLICK)
                if self.__player.sprite is not None:
                    from src.states.SaveConfirmation import SaveConfirmation
                    self._next_state = SaveConfirmation(self._game, self,
                                                        False)
                else:
                    self._is_running = False

    def __spawn_enemy(self):
        """
        Spawns random enemies in the game when appropriate.
        Enemies are chosen randomly from available types,
        with different probabilities based on difficulty.
        """
        if len(self.__enemies) < Constants.MAX_ENEMIES:
            enemy_types = [
                (WavyEnemy, Constants.WAVY_ENEMY_SPAWN_CHANCE),
                (LinearEnemy, Constants.LINEAR_ENEMY_SPAWN_CHANCE),
                (BouncingEnemy, Constants.BOUNCING_ENEMY_SPAWN_CHANCE),
                (TankEnemy, Constants.TANK_ENEMY_SPAWN_CHANCE)
            ]
            enemy_class = random.choices(
                [et[0] for et in enemy_types],
                weights=[et[1] for et in enemy_types]
            )[0]

            spawn_positions = [0, Constants.WIDTH]
            spawn_x = random.choice(spawn_positions)

            self.__enemies.add(enemy_class(spawn_x))

    def to_dict(self):
        """
        Converts the current Play state into a dictionary.
        """
        state = {
            "spawn_timer": self.__spawn_timer,
            "speed_multiplier": self.__speed_multiplier,
            "terrain": self.__terrain.to_dict(),
            "player": None if self.__player.sprite is None else self.__player.sprite.to_dict(),
            "enemies": [enemy.to_dict() for enemy in
                        self.__enemies.sprites()],
        }
        return state

    @classmethod
    def from_dict(cls, data, game, player_name):
        """
        Creates an instance of Play from a dictionary.

        :param player_name: name of the player's type.
        :param data: The dictionary containing the state.
        :param game: The main game instance.
        :return: A restored instance of Play.
        """
        # Create the Play state instance using the provided game and player
        instance = cls(game, player_name)
        instance.__spawn_timer = data.get("spawn_timer", 0)
        instance.__speed_multiplier = data.get("speed_multiplier", 1.0)

        # Restore Terrain
        instance.__terrain = Terrain.from_dict(data["terrain"])

        # Restore Player state
        player_data = data.get("player")
        if data.get("player") is not None:
            player_type = player_data.get("type")
            instance.__player_name = player_type
            restored_player = PlayerClassMap[player_type].from_dict(
                player_data)
            instance.__player = pygame.sprite.GroupSingle(restored_player)
        else:
            print("player not found")

        # Restore Enemies
        restored_enemies = []
        for enemy_data in data.get("enemies", []):
            enemy_type = enemy_data.get("type")
            if enemy_type in EnemyClassMap:
                enemy = EnemyClassMap[enemy_type].from_dict(enemy_data)
                restored_enemies.append(enemy)
        instance.__enemies = pygame.sprite.Group(restored_enemies)

        instance.__player_projectiles = pygame.sprite.Group()
        instance.__enemies_projectiles = pygame.sprite.Group()
        instance.__abilities = pygame.sprite.Group()
        instance.__hud = Hud(instance.__player.sprite)

        return instance
