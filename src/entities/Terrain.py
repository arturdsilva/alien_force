import math
import pygame
from config.Constants import Constants

class Block(pygame.sprite.Sprite):
    """
    Represents a terrain block sprite.
    """
    def __init__(self, x, y, width, height):
        """
        Initializes a terrain block.

        :param x: X position of the block
        :param y: Y position of the block
        :param width: Width of the block
        :param height: Height of the block
        """
        super().__init__()
        self.texture = pygame.image.load("assets/sprites/Tile.png").convert_alpha()
        self.image = pygame.transform.scale(self.texture, (math.ceil(width), math.ceil(height)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Terrain(pygame.sprite.Group):
    """
    Represents a group of terrain blocks that form the game terrain.
    """
    def __init__(self, terrain):
        """
        Initializes the terrain from a matrix.

        :param terrain: Matrix where 'X' represents a block and other characters represent empty space
        """
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

    def to_dict(self):
        """
        Converts the Terrain state into a dictionary.
        Each block's position and dimensions are stored.
        """
        blocks = []
        for sprite in self.sprites():
            blocks.append({
                "topleft": list(sprite.rect.topleft),
                "width": sprite.image.get_width(),
                "height": sprite.image.get_height()
            })
        return {
            "blocks": blocks
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates an instance of Terrain from a dictionary.
        The dictionary should contain a list of blocks with their positions and dimensions.
        """
        instance = cls.__new__(cls)
        pygame.sprite.Group.__init__(instance)
        for block_data in data.get("blocks", []):
            topleft = block_data["topleft"]
            width = block_data["width"]
            height = block_data["height"]
            x = topleft[0]
            y = topleft[1]
            block = Block(x, y, width, height)
            instance.add(block)
        return instance
