import pygame
import numpy as np
from config.Constants import Constants
from .BombProjectile import BombProjectile
from .NormalProjectile import NormalProjectile


class ProjectileGenerator:
    """
    Gerador de projéteis que controla a criação e comportamento dos projéteis.
    """
    
    def __init__(self, agent, projectile_speed, frequency, projectile_image, projectile_damage, projectile_type="normal", is_player_projectile=False):
        """
        Inicializa um gerador de projéteis.

        :param agent: Agente que dispara os projéteis
        :param projectile_speed: Velocidade dos projéteis
        :param frequency: Frequência de disparo
        :param projectile_image: Imagem do projétil
        :param projectile_damage: Dano do projétil
        :param projectile_type: Tipo do projétil ("normal" ou "bomb")
        :param is_player_projectile: Indica se é um projétil do jogador
        """
        self._agent = agent
        self._projectile_speed = projectile_speed
        self._frequency = frequency
        self._projectile_image = projectile_image
        self._projectile_damage = projectile_damage
        self._projectile_type = projectile_type
        self._is_player_projectile = is_player_projectile
        self._time_without_generation = 0

    def generate(self, target, dt, projectiles):
        """
        Gera um projétil se o tempo entre disparos permitir.

        :param target: Ponto para onde o projétil será direcionado
        :param dt: Tempo desde a última atualização
        :param projectiles: Grupo de sprites dos projéteis
        """
        self._time_without_generation += dt
        
        if self._time_without_generation >= 1 / self._frequency:
            self._time_without_generation = 0
            
            origin = pygame.Vector2(self._agent.rect.centerx, self._agent.rect.centery)
            angle = self._compute_shot_angle(origin, target)
            
            velocity = pygame.Vector2()
            velocity.x = self._projectile_speed * np.cos(angle)
            velocity.y = self._projectile_speed * np.sin(angle)
            
            if self._projectile_type == "bomb":
                # Para bombas, a velocidade é sempre vertical para baixo
                velocity = pygame.Vector2(0, self._projectile_speed)
                projectile = BombProjectile(
                    position=origin,
                    velocity=velocity,
                    image=self._projectile_image,
                    damage=self._projectile_damage,
                    explosion_radius=Constants.TANK_BOMB_EXPLOSION_RADIUS
                )
            else:
                # Para projéteis normais, usa a velocidade calculada
                projectile = NormalProjectile(
                    position=origin,
                    velocity=velocity,
                    image=self._projectile_image,
                    damage=self._projectile_damage,
                    is_player_projectile=self._is_player_projectile
                )
            
            projectiles.add(projectile)

    @staticmethod
    def _compute_shot_angle(origin, target):
        """
        Calcula o ângulo entre o eixo x e a trajetória do tiro.

        :param origin: Ponto de origem do tiro
        :param target: Ponto alvo do tiro
        :return: Ângulo em radianos
        """
        if np.abs(target.x - origin.x) < Constants.EPSILON:
            if target.y > origin.y:
                angle = np.pi / 2
            else:
                angle = -np.pi / 2
        elif np.abs(target.y - origin.y) < Constants.EPSILON:
            if target.x > origin.x:
                angle = 0
            else:
                angle = -np.pi
        else:
            angle = np.arctan((target.y - origin.y) / (target.x - origin.x))

        if angle > 0 > target.y - origin.y:
            angle += np.pi
        if angle < 0 < target.y - origin.y:
            angle += np.pi
        if angle < 0:
            angle += 2 * np.pi

        return angle 