import random

import pygame

from config.AvailableTerrains import AvailableTerrains
from config.Constants import Constants
from src.entities.Terrain import Terrain
from src.entities.enemies.BouncingEnemy import BouncingEnemy
from src.entities.enemies.EnemyClassMap import EnemyClassMap
from src.entities.enemies.LinearEnemy import LinearEnemy
from src.entities.enemies.TankEnemy import TankEnemy
from src.entities.enemies.WavyEnemy import WavyEnemy
from src.entities.players.PlayerClassMap import PlayerClassMap
from src.states import GameState
from src.states.Pause import Pause
from src.states.Hud import Hud


class Play(GameState):
    """
    Game in progress state.
    """

    def __init__(self, game, player_name):
        """
        Initializes the game state.

        :param game: The main game instance.
        :param player: The character selected by the player.
        """
        super().__init__(game)
        self.spawn_timer = 0
        self.__speed_multiplier = 1.0

        # Terrain
        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.__terrain = Terrain(random_terrain)

        player = PlayerClassMap[player_name]()

        # Posiciona o player no centro-x e acima do terreno
        player.rect.centerx = Constants.WIDTH / 2
        player.rect.bottom = 0  # Começa no topo

        # Sprite Groups
        self.__player = pygame.sprite.GroupSingle(player)
        self.__enemies = pygame.sprite.Group()
        self.__player_projectiles = pygame.sprite.Group()
        self.__enemies_projectiles = pygame.sprite.Group()
        self.__abilities = pygame.sprite.Group()

        # Initialize HUD
        self.hud = Hud(player)

        # Ajusta a posição inicial do player para ficar sobre o terreno
        self._adjust_player_initial_position()

    def _adjust_player_initial_position(self):
        """
        Adjusts the initial player position to be on terrain.
        """
        player = self.__player.sprite
        # Move o player para baixo até encontrar o terreno
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

        # Update HUD
        self.hud.update(dt)

        # Check for enemy destruction to update score
        for enemy in self.__enemies.sprites():
            if enemy.health <= 0:
                # Add points based on enemy type
                if isinstance(enemy, TankEnemy):
                    self.hud.add_score(100)
                elif isinstance(enemy, WavyEnemy):
                    self.hud.add_score(50)
                elif isinstance(enemy, LinearEnemy):
                    self.hud.add_score(30)
                elif isinstance(enemy, BouncingEnemy):
                    self.hud.add_score(40)
                # Mata o inimigo após atualizar a pontuação
                enemy.kill()

        # Verifica se o jogador morreu
        if player._health_points <= 0:
            from src.states.GameOver import GameOver
            self.next_state = GameOver(self.game, self.hud.score)

        self.spawn_timer += dt
        if self.spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self.spawn_timer = 0

        if self.__speed_multiplier < Constants.SPEED_MULTIPLIER_LIMIT:
            self.__speed_multiplier += Constants.DIFFICULTY_FACTOR

    def draw(self, screen):
        """
        Draws the game state.

        :param screen: The screen surface to draw on.
        """
        screen.fill(Constants.BACKGROUND_COLOR)
        self.__terrain.draw(screen)
        self.__player.draw(screen)
        self.__enemies.draw(screen)
        
        # Desenha os projéteis do jogador
        for projectile in self.__player_projectiles:
            projectile.draw(screen)
            
        # Desenha os projéteis dos inimigos
        for projectile in self.__enemies_projectiles:
            projectile.draw(screen)
            
        self.__abilities.draw(screen)

        # Draw HUD on top of everything
        self.hud.draw(screen)

    def handle_events(self, events):
        """
        Processes pygame events during the game.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    self.next_state = Pause(self.game, self)
            if event.type == pygame.QUIT:
                if self.__player.sprite is not None:
                    from src.states.SaveConfirmation import SaveConfirmation
                    self.next_state = SaveConfirmation(self.game, self, False)
                else:
                    self.is_running = False

    def spawn_enemy(self):
        """
        Spawns random enemies in the game when appropriate.
        Enemies are chosen randomly from available types,
        with different probabilities based on difficulty.
        """
        if len(self.__enemies) < Constants.MAX_ENEMIES:
            # Lista de tipos de inimigos com seus pesos (probabilidades)
            enemy_types = [
                (WavyEnemy, 30),  # 30% de chance
                (LinearEnemy, 30),  # 30% de chance
                (BouncingEnemy, 25),  # 25% de chance
                (TankEnemy, 15)  # 15% de chance
            ]

            # Escolhe um inimigo baseado nos pesos
            enemy_class = random.choices(
                [enemy[0] for enemy in enemy_types],
                weights=[enemy[1] for enemy in enemy_types]
            )[0]

            # Cria e adiciona o inimigo ao grupo
            self.__enemies.add(enemy_class())

    def to_dict(self):
        """
        Converts the current Play state into a dictionary.
        """
        state = {
            "spawn_timer": self.spawn_timer,
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
        instance.spawn_timer = data.get("spawn_timer", 0)
        instance.__speed_multiplier = data.get("speed_multiplier", 1.0)

        # Restore Terrain
        instance.__terrain = Terrain.from_dict(data["terrain"])

        # Restore Player state
        player_data = data.get("player")
        if data.get("player") is not None:
            player_type = player_data.get("type")
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
        instance.hud = Hud(instance.__player.sprite)

        return instance
