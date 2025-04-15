import numpy as np
import pygame

from config.Constants import Colors
from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator
from src.entities.abilities.AbstractAbility import AbstractAbility
from src.entities.projectiles.ProjectileAbility import ProjectileAbility


class MissileBarrage(AbstractAbility):
    """
    Represents an Ability Missile Barrage
    """

    def __init__(self, agent):
        """
        Initializes an Ability Missile Barrage

        :param agent: agent of the missile barrage
        """

        super().__init__(agent)
        self.__missile_speed = self._speed
        self.__missile_damage = self._damage
        self.__num_missiles = Constants.MISSILE_SHOT_CAPACITY
        self.__angle_spread = Constants.ANGLE_SPREAD_MISSILE * (np.pi / 180)
        self.__explosion_radius = Constants.EXPLOSION_RADIUS
        self.__lifetime_missile = Constants.MISSILE_LIFETIME
        missile_image = pygame.image.load(
            "assets/sprites/projectiles/MissileLauncherProjectile.png").convert_alpha()
        missile_image = pygame.transform.scale(
            missile_image, (30, 30))
        self.__missile_image = missile_image

    def generate(self, missile_target, dt, missiles):
        """
        Uses the missile barrage skill, firing multiple missiles in a radial pattern.

        :param missile_target: Point where the center missile will be headed.
        :param dt: The duration of one iteration.
        :param missiles: Missiles sprite group.
        """

        if hasattr(self._agent, "get_projectile_origin"):
            origin = self._agent.get_projectile_origin()
        else:
            origin = pygame.math.Vector2(self._agent.rect.centerx,
                                         self._agent.rect.centery)
        center_angle = ProjectileGenerator.compute_shot_angle(origin,
                                                              missile_target)
        start_angle = center_angle - (
                (self.__num_missiles - 1) / 2) * self.__angle_spread

        for i in range(self.__num_missiles):
            missile_angle = start_angle + (i * self.__angle_spread)
            while missile_angle < 0:
                missile_angle += 2 * np.pi
            while missile_angle > 2 * np.pi:
                missile_angle -= 2 * np.pi

            velocity = pygame.math.Vector2()
            velocity.x = self.__missile_speed * np.cos(missile_angle)
            velocity.y = self.__missile_speed * np.sin(missile_angle)
            initial_position = pygame.math.Vector2(origin)
            self_collision = True
            temp_position = pygame.math.Vector2(initial_position)

            while self_collision:
                temp_position.x += velocity.x * dt
                temp_position.y += velocity.y * dt
                missile = ProjectileAbility(
                    pygame.math.Vector2(temp_position),
                    missile_angle,
                    velocity,
                    self.__missile_image,
                    self.__missile_damage,
                    self.__lifetime_missile
                )
                missile.explosion_radius = self.__explosion_radius
                missile.explosion_damage = self.__missile_damage * 0.8
                missile.create_explosion = self.create_explosion
                missile.has_exploded = False

                if pygame.sprite.collide_rect(self._agent, missile):
                    missile.kill()
                else:
                    missiles.add(missile)
                    self_collision = False

        return True

    def _draw_explosion(self, radius, color):
        """
        Creates an explosion effect with area of effect damage

        :param radius: Radius of the explosion
        :param color: Color of the explosion (RGBA)
        """
        surface_size = radius * 2
        image_explosion = pygame.Surface((surface_size, surface_size),
                                         pygame.SRCALPHA)
        pygame.draw.circle(image_explosion,
                           (color[0], color[1], color[2], 80),
                           (radius, radius), radius)
        pygame.draw.circle(image_explosion, color,
                           (radius, radius), radius * 0.7)
        pygame.draw.circle(image_explosion, Colors.GLOW_WHITE,
                           (radius, radius), radius * 0.3)
        return image_explosion

    def create_explosion(self, missile, ability_projectiles):
        """
        Creates an explosion effect when a missile is hit

        :param missile: The missile that was hit
        :param ability_projectiles: Group to add the explosion effect to
        """
        if not missile.has_exploded:
            image_explosion = self._draw_explosion(missile.explosion_radius,
                                                   Constants.COLOR_EXPLOSION)

            explosion = ProjectileAbility(
                pygame.math.Vector2(missile.rect.center),
                0,
                pygame.math.Vector2(0, 0),
                image_explosion,
                missile.explosion_damage,
                Constants.HIT_LIFETIME
            )
            explosion.radius = missile.explosion_radius
            ability_projectiles.add(explosion)
            missile.has_exploded = True
            return explosion
        return None
