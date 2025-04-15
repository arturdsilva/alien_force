import numpy as np
import pygame

from config.Constants import Constants, Colors
from src.entities.abilities.AbstractAbility import AbstractAbility
from src.entities.projectiles.ProjectileAbility import ProjectileAbility
from src.entities.projectiles.ProjectileGenerator import ProjectileGenerator


class LaserBeam(AbstractAbility):
    """
    Represents a continuous, fluid laser beam
    """

    def __init__(self, agent):
        """
        Initializes a laser beam

        :param agent: agent that fires the laser
        """
        super().__init__(agent)
        self._damage = Constants.LASER_DAMAGE
        self._speed = Constants.LASER_SPEED
        self._lifetime = Constants.LASER_LIFETIME
        self.__width_laser = Constants.LASER_WIDTH
        self.__laser_color = Constants.COLOR_LASER
        self.__glow_color = Constants.GLOW_COLOR_LASER

    def generate(self, target, dt, beams):
        """
        Generates a continuous laser beam with a fluid effect

        :param target: Point where the laser is aimed
        :param dt: Duration of one iteration
        :param beams: Sprite group to add the segments to
        """
        if hasattr(self._agent, "get_projectile_origin"):
            origin = self._agent.get_projectile_origin()
        else:
            origin = pygame.math.Vector2(self._agent.rect.centerx,
                                         self._agent.rect.centery)
        angle = ProjectileGenerator.compute_shot_angle(origin, target)
        direction = pygame.math.Vector2(np.cos(angle), np.sin(angle))
        safe_distance = self._agent.rect.width / 2
        beam_start = origin + direction * safe_distance
        self.__create_laser_segments(beam_start, direction, beams)

        return True

    def __create_laser_segments(self, start_pos, direction, beams):
        """
        Creates laser segments with a fluid effect

        :param start_pos: Starting position of the laser
        :param direction: Direction of the laser
        :param beams: Sprite group to add the segments to
        """
        max_length = Constants.LIMIT_WIDTH_LASER
        segment_length = Constants.SEGMENT_LASER_LENGTH
        num_segments = int(max_length / segment_length)
        time_factor = pygame.time.get_ticks() / Constants.LASER_TIME_DIVISOR

        for i in range(num_segments):
            segment_start = start_pos + direction * i * segment_length * 0.2
            if not (
                    0 <= segment_start.x <= Constants.WIDTH and 0 <= segment_start.y <= Constants.HEIGHT):
                continue

            perpendicular = pygame.math.Vector2(-direction.y, direction.x)
            wave_offset = np.sin(time_factor + i * 0.2) * (
                    self.__width_laser * 0.2)
            segment_pos = segment_start + perpendicular * wave_offset
            segment_surface = self.__create_segment_surface(segment_length)
            angle = np.arctan2(direction.y, direction.x)

            laser_segment = ProjectileAbility(
                segment_pos,
                angle,
                direction,
                segment_surface,
                self._damage / num_segments,
                self._lifetime
            )
            laser_segment.explosion_radius = Constants.EXPLOSION_RADIUS
            laser_segment.explosion_damage = 0
            laser_segment.create_hit_effect = self.create_hit_effect
            laser_segment.has_hit = False

            beams.add(laser_segment)

    def __create_segment_surface(self, length):
        """
        Creates the visual surface for a laser segment

        :param length: Length of the segment
        """
        surface = pygame.Surface((length, int(self.__width_laser * 3)),
                                 pygame.SRCALPHA)
        pygame.draw.line(
            surface,
            self.__glow_color,
            (0, surface.get_height() // 2),
            (length, surface.get_height() // 2),
            int(self.__width_laser * 2)
        )
        pygame.draw.line(
            surface,
            self.__laser_color,
            (0, surface.get_height() // 2),
            (length, surface.get_height() // 2),
            int(self.__width_laser)
        )
        for _ in range(2):
            pos_x = np.random.randint(0, length)
            pygame.draw.circle(
                surface,
                Constants.COLOR_LASER_CORE,
                (pos_x, surface.get_height() // 2),
                int(self.__width_laser * 0.3)
            )

        return surface

    def __draw_hit_effect(self, radius):
        """
        Creates an explosion effect

        :param radius: Radius of the hit effect
        """
        surface_size = radius * 2
        image_hit_effect = pygame.Surface((surface_size, surface_size),
                                          pygame.SRCALPHA)
        pygame.draw.circle(image_hit_effect, Colors.RED_GLOW,
                           (radius, radius), radius * 0.3)
        return image_hit_effect

    def create_hit_effect(self, laser, ability_projectiles):
        """
        Creates an effect when a laser is hit

        :param laser: The laser that was hit
        :param ability_projectiles: Group to add the explosion effect to
        """
        if not laser.has_hit:
            image_explosion = self.__draw_hit_effect(laser.explosion_radius)

            effect = ProjectileAbility(
                pygame.math.Vector2(laser.rect.center),
                0,
                pygame.math.Vector2(0, 0),
                image_explosion,
                laser.explosion_damage,
                Constants.HIT_LIFETIME
            )
            effect.radio = laser.explosion_radius
            ability_projectiles.add(effect)
            laser.has_hit = True
            return effect
        return None
