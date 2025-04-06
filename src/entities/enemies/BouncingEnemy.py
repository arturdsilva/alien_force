from src.entities.enemies.AbstractEnemy import AbstractEnemy
from config.Constants import Constants, Colors
import pygame
import random


class BouncingEnemy(AbstractEnemy):
    """
    Inimigo que se move horizontalmente e ocasionalmente cai rapidamente,
    subindo lentamente depois.
    """

    # Estados do inimigo
    MOVING = 'moving'      # Movendo horizontalmente
    PREPARING = 'preparing'  # Preparando para cair
    FALLING = 'falling'    # Caindo
    WAITING = 'waiting'    # Esperando após cair/subir
    RISING = 'rising'      # Subindo

    def __init__(self, x=Constants.WIDTH, y=Constants.BOUNCING_ENEMY_BASE_HEIGHT):
        """
        Inicializa um inimigo que alterna entre movimento horizontal e vertical.

        :param x: Coordenada x inicial do inimigo
        :param y: Coordenada y inicial do inimigo
        """
        super().__init__(x=x, y=y)
        self._health_points = Constants.BOUNCING_ENEMY_MAX_HEALTH
        self._velocity_x = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED  # Começa indo para a esquerda
        self._state = self.MOVING
        self._timer = 0
        self._wait_timer = 0
        self._fall_time = random.uniform(
            Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
            Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
        )
        self._original_y = y

    def _initialize_sprite(self, x, y):
        """
        Inicializa o sprite do inimigo.

        :param x: Coordenada x inicial
        :param y: Coordenada y inicial
        """
        self.image = pygame.Surface((Constants.BOUNCING_ENEMY_WIDTH,
                                   Constants.BOUNCING_ENEMY_HEIGHT))
        self.image.fill(Colors.ORANGE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def _move(self, dt, terrain=None):
        """
        Atualiza a posição do inimigo baseado no estado atual.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno
        """
        if self._state == self.MOVING:
            # Movimento horizontal com velocidade constante
            self.rect.x += self._velocity_x * dt
            
            # Inverte direção nas bordas
            if self.rect.left <= 0:
                self.rect.left = 0
                self._velocity_x = Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED
            elif self.rect.right >= Constants.WIDTH:
                self.rect.right = Constants.WIDTH
                self._velocity_x = -Constants.BOUNCING_ENEMY_HORIZONTAL_SPEED

        elif self._state == self.FALLING:
            # Movimento de queda rápida
            self.rect.y += Constants.BOUNCING_ENEMY_FALL_SPEED * dt
            
            # Verifica colisão com o terreno
            if terrain:
                hits = pygame.sprite.spritecollide(self, terrain, False)
                if hits:
                    self.rect.bottom = hits[0].rect.top
                    self._state = self.WAITING
                    self._timer = 0
                    return

        elif self._state == self.RISING:
            # Movimento de subida lenta
            self.rect.y -= Constants.BOUNCING_ENEMY_RISE_SPEED * dt
            if self.rect.centery <= self._original_y:
                # Apenas muda o estado, sem forçar a posição Y
                self._state = self.MOVING
                self._timer = 0
                self._fall_time = random.uniform(
                    Constants.BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL,
                    Constants.BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL
                )

    def _update_behavior(self, dt, terrain=None):
        """
        Atualiza o estado do inimigo e seus temporizadores.

        :param dt: Tempo desde a última atualização
        :param terrain: Grupo de sprites do terreno
        """
        if self._state == self.MOVING:
            self._timer += dt
            if self._timer >= self._fall_time:
                self._state = self.PREPARING
                self._timer = 0

        elif self._state == self.PREPARING:
            self._timer += dt
            if self._timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self._state = self.FALLING
                self._timer = 0

        elif self._state == self.FALLING:
            # A verificação de colisão com o terreno está no método _move
            pass

        elif self._state == self.WAITING:
            self._timer += dt
            if self._timer >= Constants.BOUNCING_ENEMY_WAIT_TIME:
                self._state = self.RISING
                self._timer = 0 