import pygame

from config.Constants import Constants
from src.entities.Projectile import ProjectileGenerator
from src.entities.abilities.AbstractAbility import AbstractAbility
from src.entities.projectiles.ProjectileAbility import ProjectileAbility


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
