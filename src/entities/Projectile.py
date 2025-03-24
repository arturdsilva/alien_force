import pygame
import numpy as np
from config.Constants import Constants


class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle, velocity, image, damage):
        super().__init__()

        self.position = position
        self.angle = angle  # ranges from 0 to 2 * pi radians
        self.velocity = velocity
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.damage = damage

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position

    def handle_bounds(self):
        if (self.rect.right < 0 or
                self.rect.left > Constants.WIDTH or
                self.rect.bottom < 0 or self.rect.top > Constants.HEIGHT):
            self.kill()


class ProjectileGenerator:
    def __init__(self, agent, projectile_speed, frequency, projectile_image,
                 projectile_damage):
        self.agent = agent
        self.projectile_speed = projectile_speed
        self.frequency = frequency
        self.projectile_image = projectile_image
        self.projectile_damage = projectile_damage
        self.time_without_generation = 0

    def generate(self, target, dt, projectiles):
        self.time_without_generation += dt
        origin = pygame.math.Vector2(self.agent.rect.centerx,
                                     self.agent.rect.centery)

        angle = self.compute_shot_angle(origin, target)

        velocity = pygame.Vector2()
        velocity.x = self.projectile_speed * np.cos(angle)
        velocity.y = self.projectile_speed * np.sin(angle)
        if self.time_without_generation >= 1 / self.frequency:
            self.time_without_generation = 0
            initial_position = origin
            self_collision = True
            while self_collision:
                initial_position.x += velocity.x * dt
                initial_position.y += velocity.y * dt
                projectile = Projectile(initial_position, angle, velocity,
                                        self.projectile_image,
                                        self.projectile_damage)
                if pygame.sprite.collide_rect(self.agent, projectile):
                    projectile.kill()
                else:
                    self_collision = False

            projectile = Projectile(initial_position, angle, velocity,
                                    self.projectile_image,
                                    self.projectile_damage)
            projectiles.add(projectile)

    @staticmethod
    def compute_shot_angle(origin, target):
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
