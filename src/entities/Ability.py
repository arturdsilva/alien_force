import numpy as np
import pygame
from config.Constants import Constants
from config.Constants import Colors
from src.entities.Projectile import ProjectileGenerator
from src.entities.projectiles.ProjectileAbility import ProjectileAbility
from src.entities.AbstractAbility import AbstractAbility

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
        missile_image = pygame.image.load("assets/sprites/projectiles/MissileLauncherProjectile.png").convert_alpha()
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
        self.__width_laser = Constants.LASER_WIDTH
        self.__laser_color = Constants.COLOR_LASER
        self.__glow_color = Constants.GLOW_COLOR_LASER
        self.__lifetime = Constants.LASER_LIFETIME

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
        self._create_laser_segments(beam_start, direction, beams)

        return True

    def _create_laser_segments(self, start_pos, direction, beams):
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
            segment_surface = self._create_segment_surface(segment_length)
            angle = np.arctan2(direction.y, direction.x)

            laser_segment = ProjectileAbility(
                segment_pos,
                angle,
                direction,
                segment_surface,
                self._damage / num_segments,
                self.__lifetime
            )
            laser_segment.explosion_radius = Constants.EXPLOSION_RADIUS
            laser_segment.explosion_damage = 0
            laser_segment.create_hit_effect = self.create_hit_effect
            laser_segment.has_hit = False

            beams.add(laser_segment)

    def _create_segment_surface(self, length):
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

    def _draw_hit_effect(self, radius):
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
            image_explosion = self._draw_hit_effect(laser.explosion_radius)

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


class CriticalShot(AbstractAbility):
    """
    Represents a sniper critical shot that is charged after a certain
    number of normal shots.
    """

    def __init__(self, agent):
        """
        Initializes the sniper's critical shot ability.

        :param agent: Agent that fires the critical shot
        """
        super().__init__(agent)
        self.__shot_speed = self._speed * 3
        self.__critical_damage = self._damage * 5
        self.__lifetime = Constants.CRITICAL_SHOT_LIFETIME
        critical_shot_image = pygame.image.load(
            "assets/sprites/projectiles/SpecialPrecisionRifleProjectile.png").convert_alpha()
        critical_shot_image = pygame.transform.scale(
            critical_shot_image, (25, 25))
        self.__critical_shot_image = critical_shot_image

    def generate(self, target, dt, projectiles):
        """
        Fires the charged critical shot.

        :param target: Point where the shot is aimed
        :param dt: Duration of one iteration (delta time)
        :param projectiles: Sprite group to add the projectile to
        """
        import math
        if hasattr(self._agent, "get_projectile_origin"):
            origin = self._agent.get_projectile_origin()
        else:
            origin = pygame.math.Vector2(self._agent.rect.centerx,
                                         self._agent.rect.centery)
        angle = ProjectileGenerator.compute_shot_angle(origin, target)
        velocity = pygame.math.Vector2(
            self.__shot_speed * math.cos(angle),
            self.__shot_speed * math.sin(angle)
        )
        position = pygame.math.Vector2(origin)
        enhanced_image = self._apply_glow_effect(self.__critical_shot_image)

        projectile = ProjectileAbility(
            position,
            angle,
            velocity,
            enhanced_image,
            self.__critical_damage,
            self.__lifetime
        )
        projectiles.add(projectile)

        return True

    def _apply_glow_effect(self, base_image):
        """
        Applies a glow effect to the base image without heavy processing.
        """
        glow_width = Constants.CRITICAL_SHOT_WIDTH_BORDER
        glow_height = Constants.CRITICAL_SHOT_HEIGHT_BORDER
        glow = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        rect = glow.get_rect()
        pygame.draw.rect(glow, Constants.COLOR_GLOW_CRITICAL_SHOT,
                         rect.inflate(-2, -2), width=8, border_radius=12)
        combined = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
        image_pos = (
            (glow_width - base_image.get_width()) // 2,
            (glow_height - base_image.get_height()) // 2
        )
        combined.blit(glow, (0, 0))
        combined.blit(base_image, image_pos)

        return combined
