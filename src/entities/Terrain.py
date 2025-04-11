import math

import pygame

from config.Constants import Constants


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((math.ceil(width), math.ceil(height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.fill(Constants.TERRAIN_COLOR)


class Terrain(pygame.sprite.Group):
    def __init__(self, terrain):
        super().__init__()

        num_blocks_horizontal = len(terrain[0])
        num_blocks_vertical = len(terrain)

        width = Constants.WIDTH / num_blocks_horizontal
        height = Constants.HEIGHT / num_blocks_vertical

        for line_index, line in enumerate(terrain):
            for block_index, block in enumerate(line):
                if line[block_index] == 'X':
                    x = block_index * width
                    y = line_index * height
                    block = Block(x, y, width, height)
                    self.add(block)
