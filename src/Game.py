import pygame
from config.Constants import Constants
import numpy as np


# from states.Menu import Menu


# from entities.players.AbstractPlayer import AbstractPlayer


class Game:
    def __init__(self):
        print('initializing game')
        self.clock = pygame.time.Clock()
        self.elapsed_time = 1 / Constants.FPS
        pygame.init()
        self.screen = pygame.display.set_mode(
            (Constants.WIDTH, Constants.HEIGHT))
        self.running = True
        # self.player = Player()
        # TODO: use class player instead o player_position and player_speed
        self.player_position = np.array(
            [Constants.WIDTH / 2, Constants.HEIGHT / 2])
        self.player_speed = 300

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
        if keys[pygame.K_w]:
            self.player_position[1] -= self.player_speed * self.elapsed_time
        if keys[pygame.K_s]:
            self.player_position[1] += self.player_speed * self.elapsed_time
        if keys[pygame.K_a]:
            self.player_position[0] -= self.player_speed * self.elapsed_time
        if keys[pygame.K_d]:
            self.player_position[0] += self.player_speed * self.elapsed_time

    def draw(self):
        self.screen.fill("purple")
        pygame.draw.circle(self.screen, "red", self.player_position, 40)
        pygame.display.flip()
