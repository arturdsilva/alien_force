import pygame
import numpy as np
from config.Constants import Constants
from entities.players.AbstractPlayer import AbstractPlayer


# from states.Menu import Menu


# from entities.players.AbstractPlayer import AbstractPlayer


class Game:
    def __init__(self):
        print('initializing game')
        self.clock = pygame.time.Clock()
        self.dt = 1 / Constants.FPS
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Constants.WIDTH, Constants.HEIGHT))
        self.running = True
        self.player = AbstractPlayer()
        self.all_sprites = pygame.sprite.Group(self.player)


    def run(self):
        print('Hi')
        while self.running:
            self.clock.tick(Constants.FPS)
            self.handle_events()
            self.update()
            self.draw()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self):
        keys = pygame.key.get_pressed()
        self.all_sprites.update(keys, self.dt)


    def draw(self):
        self.screen.fill("purple")
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
