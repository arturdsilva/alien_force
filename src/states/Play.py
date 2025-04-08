import pygame
import random
from src.states import GameState
from config.Constants import Constants
from config.AvailableTerrains import AvailableTerrains
from entities.Terrain import Terrain
from src.entities.enemies.WavyEnemy import WavyEnemy
from src.entities.enemies.LinearEnemy import LinearEnemy
from src.entities.enemies.BouncingEnemy import BouncingEnemy
from src.entities.enemies.TankEnemy import TankEnemy
from src.states.Pause import Pause
from src.ui.Hud import Hud


class Play(GameState):
    """
    Estado do jogo em andamento.
    """
    def __init__(self, game, player):
        """
        Inicializa o estado de jogo.

        :param game: A instância principal do jogo.
        :param player: O personagem selecionado pelo jogador.
        """
        super().__init__(game)
        self.spawn_timer = 0

        # Terrain
        terrains = AvailableTerrains()
        random_terrain = terrains.get_random_terrain()
        self.terrain = Terrain(random_terrain)

        # Posiciona o player no centro-x e acima do terreno
        player.rect.centerx = Constants.WIDTH / 2
        player.rect.bottom = 0  # Começa no topo
        
        # Sprite Groups
        self.player = pygame.sprite.GroupSingle(player)
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.enemies_projectiles = pygame.sprite.Group()

        # Initialize HUD
        self.hud = Hud(player)

        # Ajusta a posição inicial do player para ficar sobre o terreno
        self._adjust_player_initial_position()

    def _adjust_player_initial_position(self):
        """
        Ajusta a posição inicial do player para ficar sobre o terreno.
        """
        player = self.player.sprite
        # Move o player para baixo até encontrar o terreno
        while player.rect.bottom < Constants.HEIGHT:
            player.rect.y += 1
            hits = pygame.sprite.spritecollide(player, self.terrain, False)
            if hits:
                player.rect.bottom = hits[0].rect.top
                break

    def update(self, dt):
        """
        Atualiza o estado do jogo.

        :param dt: O intervalo de tempo desde a última atualização.
        """
        keys = pygame.key.get_pressed()
        self.player_projectiles.update(dt)
        self.player.update(keys, self.terrain, dt,
                          self.player_projectiles,
                          self.enemies_projectiles)
        self.enemies.update(dt, self.player_projectiles, self.terrain)
        
        # Update HUD
        self.hud.update(dt)
        
        # Check for enemy destruction to update score
        for enemy in self.enemies.sprites():
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

        self.spawn_timer += dt
        if self.spawn_timer >= Constants.SPAWN_TIMER:
            self.spawn_enemy()
            self.spawn_timer = 0

    def draw(self, screen):
        """
        Desenha o estado do jogo.

        :param screen: A superfície da tela onde desenhar.
        """
        screen.fill(Constants.BACKGROUND_COLOR)
        self.terrain.draw(screen)
        self.player.draw(screen)
        self.enemies.draw(screen)
        self.player_projectiles.draw(screen)
        
        # Draw HUD on top of everything
        self.hud.draw(screen)

    def handle_events(self, events):
        """
        Processa eventos do pygame durante o jogo.

        :param events: Lista de eventos do pygame para processar.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    self.next_state = Pause(self.game, self)

    def spawn_enemy(self):
        """
        Gera inimigos aleatórios no jogo quando apropriado.
        Os inimigos são escolhidos aleatoriamente entre os tipos disponíveis,
        com diferentes probabilidades baseadas na dificuldade.
        """
        if len(self.enemies) < Constants.MAX_ENEMIES:
            # Lista de tipos de inimigos com seus pesos (probabilidades)
            enemy_types = [
                (WavyEnemy, 30),      # 30% de chance
                (LinearEnemy, 30),     # 30% de chance
                (BouncingEnemy, 25),   # 25% de chance
                (TankEnemy, 15)        # 15% de chance
            ]
            
            # Escolhe um inimigo baseado nos pesos
            enemy_class = random.choices(
                [enemy[0] for enemy in enemy_types],
                weights=[enemy[1] for enemy in enemy_types]
            )[0]
            
            # Cria e adiciona o inimigo ao grupo
            self.enemies.add(enemy_class())
