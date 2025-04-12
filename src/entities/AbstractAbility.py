import numpy as np
import pygame
from abc import ABC, abstractmethod
from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator


class AbstractAbility(pygame.sprite.Sprite, ABC):
    """
    Represents a generic skill
    """

    def __init__(self, damage):
        """
        Initializes a skill

        """
        super().__init__()
        self.__damage = damage

    @property
    def damage(self):
        """
        Returns the damage value of the ability.

        :return: The damage value
        """
        return self.__damage

    def update(self, dt, speed_multiplier=1.0):
        """
        Updates the skill's position and lifetime.

        :param dt: Duration of one iteration.
        :param speed_multiplier: increase the ability speed
        """
        dt *= speed_multiplier
        self._update_behavior(dt)
        self._move(dt)

    @abstractmethod
    def _initialize_sprite(self, position, angle, image):
        pass

    @abstractmethod
    def _move(self, dt):
        pass

    @abstractmethod
    def _update_behavior(self, dt):
        pass

    @abstractmethod
    def generate(self, target, dt, abilities_group):
        pass


class ProjectileAbility(AbstractAbility):
    """
    Base class for projectile-based abilities that move along a trajectory
    """

    def __init__(self, position, angle, velocity, image, damage,
                 lifetime=None):
        """
        Initializes a projectile ability

        :param position: position of the projectile
        :param angle: angle in radians (0 to 2pi)
        :param velocity: velocity vector of the projectile
        :param image: image of the projectile
        :param damage: damage caused by the projectile
        :param lifetime: lifetime in seconds (None for unlimited)
        """
        super().__init__(damage)
        self._position = position
        self._velocity = velocity
        self._lifetime = lifetime
        self._initialize_sprite(position, angle, image)
        self._time_alive = 0
        self.__lifetime = lifetime

    def _initialize_sprite(self, position, angle, image):
        """
        Initialize the sprite for the projectile

        :param position: Position of the projectile
        :param angle: Angle in radians
        :param image: Image of the projectile
        """
        self._image = image
        self._original_image = image
        self._angle = np.degrees(angle)
        self.image = pygame.transform.rotate(self._image, self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def _update_behavior(self, dt):
        """
        Update the projectile behavior (lifetime)

        :param dt: Duration of one iteration
        """
        if self.__lifetime is not None:
         self._time_alive += dt
         if self._time_alive >= self.__lifetime:
             self.kill()
             return
         if hasattr(self.image, "set_alpha"):
             alpha = int(255 * (1 - self._time_alive / self.__lifetime))
             self.image.set_alpha(alpha)

    def _move(self, dt):
        """
        Move the projectile along its trajectory

        :param dt: Duration of one iteration
        """
        self._position += self._velocity * dt
        self.rect.center = self._position

    def generate(self, target, dt, projectiles_group):
         """
         Implementation of the abstract method from AbstractAbility.
         ProjectileAbility instances are typically created, not generators themselves.

         :param target: The target position (not used for instances)
         :param dt: Duration of one iteration (not used for instances)
         :param projectiles_group: The group to add projectiles to (not used for instances)
         :return: Always False since instances don't generate other projectiles
         """
         # This implementation exists only to satisfy the abstract method requirement
         # Actual projectile instances don't generate other projectiles
         return False


class MissileBarrage(AbstractAbility):
    """
    Represents an Ability Missile Barrage
    """

    def __init__(self, agent, missile_speed, missile_image,
                 missile_damage, num_missiles, angle_spread,
                 explosion_radius):
        """
        Initializes an Ability Missile Barrage

        :param agent: agent of the missile barrage
        :param missile_speed: speed of the missile
        :param missile_image: image of the missile
        :param missile_damage: damage to the missile
        :param num_missiles: quantity of the missiles
        :param angle_spread: spread of the angle
        :param explosion_radius: radius of the explosion when missile hits
        """

        super().__init__(missile_damage)
        self.__agent = agent
        self.__missile_speed = missile_speed
        self._missile_image = missile_image
        self._damage = missile_damage
        self.__num_missiles = num_missiles
        self.__angle_spread = angle_spread * (np.pi / 180)
        self.__explosion_radius = explosion_radius

    def _initialize_sprite(self, position, angle, image):
        """
        Initialize the sprite for the projectile

        :param position: Position of the projectile
        :param angle: Angle in radians
        :param image: Image of the projectile
        """
        self._image = image
        self._original_image = image
        self._angle = np.degrees(angle)
        self.image = pygame.transform.rotate(self._image, self._angle)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.has_exploded = False

    def _update_behavior(self, dt):
        """
        MissileBarrage doesn't have behavior to update
        """
        pass
    def _move(self, dt):
        """
        Move the projectile along its trajectory

        :param dt: Duration of one iteration
        """
        # self._position += self._velocity * dt
        # self.rect.center = self._position

    def generate(self, missile_target, dt, missiles):
        """
        Uses the missile barrage skill, firing multiple missiles in a radial pattern.

        :param missile_target: Point where the center missile will be headed.
        :param dt: The duration of one iteration.
        :param missiles: Missiles sprite group.
        """

        origin = pygame.math.Vector2(self.__agent.rect.centerx,
                                     self.__agent.rect.centery)
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
                    self._missile_image,
                    self._damage
                )
                missile.explosion_radius = self.__explosion_radius
                missile.explosion_damage = self._damage * 0.8
                missile.create_explosion = self.create_explosion
                missile.has_exploded = False

                if pygame.sprite.collide_rect(self.__agent, missile):
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
        pygame.draw.circle(image_explosion, (255, 255, 255, 200),
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
                0.5
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

    def __init__(self, agent, damage, duration, width,
                 color, lifetime):
        """
        Initializes a laser beam

        :param agent: agent that fires the laser
        :param damage: laser damage
        :param duration: duration of the laser in seconds
        :param width: width of the laser
        :param color: color of the laser (RGB)
        :param lifetime: lifetime of the laser
        """
        super().__init__(damage)
        self._agent = agent
        self._duration = duration
        self._width_laser = width
        self._laser_color = color
        self._glow_color = Constants.GLOW_COLOR_LASER
        self._lifetime = lifetime
        self._damage = damage

    def _initialize_sprite(self, position=None, angle=None, image=None):
        """
        LaserBeam doesn't need a sprite, as it's just a generator
        """
        pass

    def _update_behavior(self, dt):
        """
        LaserBeam doesn't have behavior to update
        """
        pass

    def _move(self, dt):
        """
        Move the projectile along its trajectory

        :param dt: Duration of one iteration
        """

    def generate(self, target, dt, beams):
        """
        Generates a continuous laser beam with a fluid effect

        :param target: Point where the laser is aimed
        :param dt: Duration of one iteration
        :param beams: Sprite group to add the segments to
        """
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
        max_length = Constants.WIDTH * 9
        segment_length = Constants.SEGMENT_LASER_LENGTH
        num_segments = int(max_length / segment_length)
        time_factor = pygame.time.get_ticks() / 500.0

        for i in range(num_segments):
            segment_start = start_pos + direction * (
                    i * segment_length) * 0.15
            if not (
                    0 <= segment_start.x <= Constants.WIDTH and 0 <= segment_start.y <= Constants.HEIGHT):
                continue

            perpendicular = pygame.math.Vector2(-direction.y, direction.x)
            wave_offset = np.sin(time_factor + i * 0.2) * (
                    self._width_laser * 0.2)
            segment_pos = segment_start + perpendicular * wave_offset
            segment_surface = self._create_segment_surface(segment_length)
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
            laser_segment.create_explosion = self.create_explosion
            laser_segment.has_exploded = False

            beams.add(laser_segment)

    def _create_segment_surface(self, length):
        """
        Creates the visual surface for a laser segment

        :param length: Length of the segment
        """
        surface = pygame.Surface((length, int(self._width_laser * 3)),
                                 pygame.SRCALPHA)
        pygame.draw.line(
            surface,
            self._glow_color,
            (0, surface.get_height() // 2),
            (length, surface.get_height() // 2),
            int(self._width_laser * 2)
        )
        pygame.draw.line(
            surface,
            self._laser_color,
            (0, surface.get_height() // 2),
            (length, surface.get_height() // 2),
            int(self._width_laser)
        )
        for _ in range(2):
            pos_x = np.random.randint(0, length)
            pygame.draw.circle(
                surface,
                Constants.COLOR_LASER_CORE,
                (pos_x, surface.get_height() // 2),
                int(self._width_laser * 0.3)
            )

        return surface

    def _draw_explosion(self, radius, color):
        """
        Creates an explosion effect

        :param radius: Radius of the explosion
        :param color: Color of the explosion (RGBA)
        """
        surface_size = radius * 2
        image_explosion = pygame.Surface((surface_size, surface_size),
                                         pygame.SRCALPHA)
        pygame.draw.circle(image_explosion, (255, 0, 0, 10),
                           (radius, radius), radius * 0.3)
        return image_explosion

    def create_explosion(self, laser, ability_projectiles):
        """
        Creates an explosion effect when a laser is hit

        :param laser: The laser that was hit
        :param ability_projectiles: Group to add the explosion effect to
        """
        if not laser.has_exploded:
            image_explosion = self._draw_explosion(laser.explosion_radius,
                                                   Constants.COLOR_EXPLOSION)

            explosion = ProjectileAbility(
                pygame.math.Vector2(laser.rect.center),
                0,
                pygame.math.Vector2(0, 0),
                image_explosion,
                laser.explosion_damage,
                0.5
            )
            explosion.radio = laser.explosion_radius
            ability_projectiles.add(explosion)
            laser.has_exploded = True
            return explosion
        return None


class CriticalShot(AbstractAbility):
    """
    Represents a sniper critical shot that is charged after a certain
    number of normal shots.
    """

    def __init__(self, agent, shot_speed, critical_image, critical_damage):
        """
        Initializes the sniper's critical shot ability.

        :param agent: Agent that fires the critical shot
        :param shot_speed: Speed of the critical shot
        :param critical_image: Image of the critical shot
        :param critical_damage: Damage dealt by the critical shot
        """
        super().__init__(critical_damage)
        self._agent = agent
        self._shot_speed = shot_speed
        self._critical_image = critical_image
        self._damage = critical_damage

    def _initialize_sprite(self, position=None, angle=None, image=None):
        """
        CriticalShot doesn't need a sprite, as it's just a generator
        """
        pass

    def _update_behavior(self, dt):
        """
        CriticalShot doesn't have behavior to update
        """
        pass

    def _move(self, dt):
        """
        Move the projectile along its trajectory

        :param dt: Duration of one iteration
        """

    def generate(self, target, dt, projectiles):
        """
        Fires the charged critical shot.

        :param target: Point where the shot is aimed
        :param dt: Duration of one iteration (delta time)
        :param projectiles: Sprite group to add the projectile to
        """
        origin = pygame.math.Vector2(self._agent.rect.centerx,
                                     self._agent.rect.centery)
        angle = ProjectileGenerator.compute_shot_angle(origin, target)
        velocity = pygame.math.Vector2(
            self._shot_speed * np.cos(angle),
            self._shot_speed * np.sin(angle)
        )
        position = pygame.math.Vector2(origin)
        enhanced_image = self._apply_glow_effect(self._critical_image)

        projectile = ProjectileAbility(
            position,
            angle,
            velocity,
            enhanced_image,
            self._damage
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