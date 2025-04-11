import numpy as np
import pygame

from config.Constants import Constants


class Ability(pygame.sprite.Sprite):
    """
    Represents a generic skill
    """

    def __init__(self, position, angle, velocity, image, damage,
                 lifetime=None):
        """
        Initializes a skill

        :param position: position of the skill
        :param angle: angle in radians (0 to 2pi)
        :param velocity: speed of the skill
        :param image: image of the skill
        :param damage: damage caused by the skill
        :param lifetime: lifetime in seconds (None to unlimited)
        """
        super().__init__()

        self._position = position
        self._image = image
        self._original_image = image
        self.__angle = np.degrees(angle)
        self._velocity = velocity
        self.image = pygame.transform.rotate(self._image, self.__angle)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.__damage = damage
        self.__lifetime = lifetime
        self._time_alive = 0

    def update(self, dt, speed_multiplier=1.0):
        """
        Updates the skill's position and lifetime.

        :param dt: Duration of one iteration.
        :param speed_multiplier: increase the ability speed
        """
        dt *= speed_multiplier

        if self.__lifetime is not None:
            self._time_alive += dt
            if self._time_alive >= self.__lifetime:
                self.kill()
                return
            if hasattr(self.image, "set_alpha"):
                alpha = int(255 * (1 - self._time_alive / self.__lifetime))
                self.image.set_alpha(alpha)
        self._position += self._velocity * dt
        self.rect.center = self._position
        self._handle_bounds()

    def _handle_bounds(self):
        """
        Removes objects that go off screen
        """
        if (self.rect.right < 0 or
                self.rect.left > Constants.WIDTH or
                self.rect.bottom < 0 or
                self.rect.top > Constants.HEIGHT):
            self.kill()

    @staticmethod
    def compute_shot_angle(origin, target):
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


class MissileBarrage(Ability):
    """
    Represents an Abilitiy Missile Barrage
    """

    def __init__(self, agent, missile_speed, missile_image,
                 missile_damage, num_missiles, angle_spread=10):
        """
        Initializes an Abilitiy Missile Barrage

        :param agent: agent of the missile barrage
        :param missile_speed: speed of the missile
        :param missile_image: image of the missile
        :param missile_damage: damage to the missile
        :param num_missiles: quantity of the missiles
        :param angle_spread: spread of the angle
        """
        self.__agent = agent
        self.__missile_speed = missile_speed
        self.missile_image = missile_image
        self.__missile_damage = missile_damage
        self.__num_missiles = num_missiles
        self.__angle_spread = angle_spread * (np.pi / 180)

    def generate(self, missile_target, dt, missiles):
        """
        Uses the missile barrage skill, firing multiple missiles in a radial pattern.

        :param missile_target: Point where the center missile will be headed.
        :param dt: The duration of one iteration.
        :param missiles: Missiles sprite group.
        """
        origin = pygame.math.Vector2(self.__agent.rect.centerx,
                                     self.__agent.rect.centery)
        center_angle = Ability.compute_shot_angle(origin, missile_target)
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

                missile = Ability(pygame.math.Vector2(temp_position),
                                  missile_angle, velocity,
                                  self.missile_image,
                                  self.__missile_damage)

                if pygame.sprite.collide_rect(self.__agent, missile):
                    missile.kill()
                else:
                    missiles.add(missile)
                    self_collision = False

        return True


class LaserBeam(Ability):
    """
    Representa um feixe de laser fluido e contínuo
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
        :param color: color of the laser (RGBA)
        :param lifetime: lifetime of the laser
        """
        self.__agent = agent
        self.__damage = damage
        self.__duration = duration
        self.__width_laser = width
        self._laser_color = color
        self._glow_color = Constants.GLOW_COLOR_LASER  # Adiciona alpha para o brilho
        self.__lifetime = lifetime

    def generate(self, target, dt, beams):
        """
        Generates a continuous laser beam with a fluid effect

        :param target: Point where the laser is aimed
        :param dt: Duration of one iteration
        :param beams: Sprite group to add the segments to
        """

        origin = pygame.math.Vector2(self.__agent.rect.centerx,
                                     self.__agent.rect.centery)
        angle = Ability.compute_shot_angle(origin, target)
        direction = pygame.math.Vector2(np.cos(angle), np.sin(angle))
        safe_distance = self.__agent.rect.width / 2
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

        max_length = Constants.WIDTH * 10
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
                        self.__width_laser * 0.2)
            segment_pos = segment_start + perpendicular * wave_offset
            segment_surface = self._create_segment_surface(segment_length)
            angle = np.arctan2(direction.y, direction.x)

            segment = Ability(
                segment_pos,
                angle,
                direction,
                segment_surface,
                self.__damage / num_segments,
                self.__lifetime
            )

            beams.add(segment)

    def _create_segment_surface(self, length):
        """
        Creates the visual surface for a laser segment

        :param length: Length of the segment
        """

        surface = pygame.Surface((length, int(self.__width_laser * 3)),
                                 pygame.SRCALPHA)
        pygame.draw.line(
            surface,
            self._glow_color,
            (0, surface.get_height() // 2),
            (length, surface.get_height() // 2),
            int(self.__width_laser * 2)
        )
        pygame.draw.line(
            surface,
            self._laser_color,
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


class CriticalShot(Ability):
    """
    Represents a sniper critical shot that is charged after a certain
    number of normal shots.
    """

    def __init__(self, agent, shot_speed,
                 critical_image, critical_damage):
        """
        Initializes the sniper's critical shot ability.

        :param agent: Agent that fires the critical shot
        :param shot_speed: Speed of the critical shot
        :param critical_image: Image of the critical shot
        :param critical_damage: Damage dealt by the critical shot
        """
        self.__agent = agent
        self.__shot_speed = shot_speed
        self.__critical_image = critical_image
        self.__critical_damage = critical_damage

    def generate(self, target, dt, projectiles):
        """
        Fires the charged critical shot.

        :param target: Point where the shot is aimed
        :param dt: Duration of one iteration (delta time)
        :param projectiles: Sprite group to add the projectile to
        """

        origin = pygame.math.Vector2(self.__agent.rect.centerx,
                                     self.__agent.rect.centery)
        angle = Ability.compute_shot_angle(origin, target)
        velocity = pygame.math.Vector2(
            self.__shot_speed * np.cos(angle),
            self.__shot_speed * np.sin(angle)
        )
        position = pygame.math.Vector2(origin)
        final_image = self._apply_glow_effect(self.__critical_image)
        self.__critical_image = final_image
        critical_shot = Ability(
            position,
            angle,
            velocity,
            self.__critical_image,
            self.__critical_damage
        )
        self.__damage = self.__critical_damage * 1.5
        projectiles.add(critical_shot)

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
