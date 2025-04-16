import pygame
import numpy as np
from config.Constants import Constants
from .BombProjectile import BombProjectile
from .NormalProjectile import NormalProjectile
from src.utils.AudioManager import AudioManager


class ProjectileGenerator:
    """
    Projectile generator that controls projectile creation and behavior.
    """
    
    def __init__(self, projectile_speed, frequency,
                 projectile_image, projectile_damage,
                 sound, projectile_type="normal", is_player_projectile=False):
        """
        Initializes a projectile generator.

        :param projectile_speed: Projectile speed
        :param frequency: Firing frequency
        :param projectile_image: Projectile image
        :param projectile_damage: Projectile damage
        :param projectile_type: Projectile type ("normal" or "bomb")
        :param is_player_projectile: Indicates if it's a player projectile
        """
        self.__projectile_speed = projectile_speed
        self.__frequency = frequency
        self.__projectile_image = projectile_image
        self.__projectile_damage = projectile_damage
        self.__sound = sound
        self.__audio_manager = AudioManager()
        self.__projectile_type = projectile_type
        self.__is_player_projectile = is_player_projectile
        self.__time_without_generation = 0

    def generate(self, origin, target, dt, projectiles):
        """
        Generates a projectile if the time between shots allows.

        :param origin: Origin of the projectile
        :param target: Point where the projectile will be directed
        :param dt: Time since last update
        :param projectiles: Projectile sprite group
        """
        self.__time_without_generation += dt
        
        if self.__time_without_generation >= 1 / self.__frequency:
            self.__time_without_generation = 0

            angle = self.compute_shot_angle(origin, target)
            
            velocity = pygame.Vector2()
            velocity.x = self.__projectile_speed * np.cos(angle)
            velocity.y = self.__projectile_speed * np.sin(angle)
            
            if self.__projectile_type == "bomb":
                velocity = pygame.Vector2(0, self.__projectile_speed)
                projectile = BombProjectile(
                    position=origin,
                    velocity=velocity,
                    image=self.__projectile_image,
                    damage=self.__projectile_damage,
                    explosion_radius=Constants.TANK_BOMB_EXPLOSION_RADIUS
                )
            else:
                projectile = NormalProjectile(
                    position=origin,
                    velocity=velocity,
                    image=self.__projectile_image,
                    damage=self.__projectile_damage,
                )
            
            projectiles.add(projectile)
            self.__audio_manager.play_sound(self.__sound)

    @staticmethod
    def compute_shot_angle(origin, target):
        """
        Calculates the angle between the x-axis and the shot trajectory.

        :param origin: Shot origin point
        :param target: Shot target point
        :return: Angle in radians
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