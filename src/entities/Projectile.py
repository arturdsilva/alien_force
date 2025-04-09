import pygame
import numpy as np
from config.Constants import Constants


class Projectile(pygame.sprite.Sprite):
    """
    Represents a projectile.
    """

    def __init__(self, position, angle, velocity, image, damage):
        """
        Initializes a projectile.

        :param position: The projectile's position.
        :param angle: The projectile's angle from 0 to 2pi radians.
        :param velocity: The projectile's absolute velocity.
        :param image: The projectile's image.
        :param damage: The damage the projectile will inflict.
        """

        super().__init__()

        self.__position = position
        self.__angle = angle
        self.__velocity = velocity
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.__damage = damage

    @property
    def damage(self):
        """
        Retorna o dano que o projétil causa.
        
        :return: Valor do dano do projétil
        """
        return self.__damage

    def update(self, dt):
        """
        Updates the projectile's position.

        :param dt: The duration of one iteration.
        """

        self.__position += self.__velocity * dt
        self.rect.center = self.__position
        self.__handle_bounds()

    def __handle_bounds(self):
        """
        Kills projectiles that go out of bounds.
        """

        if (self.rect.right < 0 or
                self.rect.left > Constants.WIDTH or
                self.rect.bottom < 0 or self.rect.top > Constants.HEIGHT):
            self.kill()

    @property
    def damage(self):
        """
        The damage the projectile will inflict.
        """

        return self.__damage


class ProjectileGenerator:
    """
    Generates projectiles.
    """

    def __init__(self, agent, projectile_speed, frequency, projectile_image,
                 projectile_damage):
        """
        Initializes a projectile generator.

        :param agent: The agent who's firing the projectile.
        :param projectile_speed: The projectile's speed.
        :param frequency: The frequency at which projectiles are generated.
        :param projectile_image: The image used for the projectile.
        :param projectile_damage: The damage each projectile will inflict.
        """

        self.__agent = agent
        self.__projectile_speed = projectile_speed
        self.__frequency = frequency
        self.__projectile_image = projectile_image
        self.__projectile_damage = projectile_damage
        self.time_without_generation = 0

    def generate(self, target, dt, projectiles):
        """
        Generates a projectile.

        :param target: Point where projectile will be headed at.
        :param dt: The duration of one iteration.
        :param projectiles: Projectiles sprite group.
        """

        self.time_without_generation += dt
        origin = pygame.math.Vector2(self.__agent.rect.centerx,
                                     self.__agent.rect.centery)

        angle = self.__compute_shot_angle(origin, target)

        velocity = pygame.Vector2()
        velocity.x = self.__projectile_speed * np.cos(angle)
        velocity.y = self.__projectile_speed * np.sin(angle)
        if self.time_without_generation >= 1 / self.__frequency:
            self.time_without_generation = 0
            initial_position = origin
            self_collision = True
            while self_collision:
                initial_position.x += velocity.x * dt
                initial_position.y += velocity.y * dt
                projectile = Projectile(initial_position, angle, velocity,
                                        self.__projectile_image,
                                        self.__projectile_damage)
                if pygame.sprite.collide_rect(self.__agent, projectile):
                    projectile.kill()
                else:
                    projectiles.add(projectile)
                    self_collision = False

    @staticmethod
    def __compute_shot_angle(origin, target):
        """
        Calculates angle between x-axis and shot trajectory.
        :param origin: The shot origin point.
        :param target: The point where the shot is targeted at.
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
