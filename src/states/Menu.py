import json

import pygame

from config.Constants import Constants, Sounds
from src.states.AbstractState import AbstractState
from src.states.CharacterSelect import CharacterSelect
from src.utils.AudioManager import AudioManager


class Menu(AbstractState):
    """
    Main menu game state.
    """

    def __init__(self, game):
        """
        Initializes the main menu.

        :param game: The main game instance.
        """
        super().__init__(game)
        self.__bg_image = pygame.image.load("assets/sprites/Menu.png").convert()
        self.__bg_image = pygame.transform.scale(self.__bg_image, (
            Constants.WIDTH, Constants.HEIGHT))
        self.__font = pygame.font.Font(None, 74)
        self.__title = self.__font.render('Alien Force', True,
                                          pygame.Color('white'))
        self.__title_rect = self.__title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 4))

        self.__font_options = pygame.font.Font(None, 54)

        self.__audio_manager = AudioManager()

        self.__options = [
            {'text': 'Novo Jogo', 'action':
                self.__start_from_beginning},
            {'text': 'Continuar Jogo Salvo',
             'action': self.__start_from_save},
        ]

        self.__options_surfaces = []
        self.__options_rects = []

        for i, option in enumerate(self.__options):
            surface = self.__font_options.render(option['text'], True,
                                                 pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
            self.__options_surfaces.append(surface)
            self.__options_rects.append(rect)

    def update(self, dt):
        """
        Updates the menu state.

        :param dt: Time interval since last update.
        """
        pass

    def draw(self, screen):
        """
        Draws the menu on screen.

        :param screen: The screen surface to draw on.
        """
        screen.blit(self.__bg_image, (0, 0))
        screen.blit(self.__title, self.__title_rect)
        for surface, rect in zip(self.__options_surfaces, self.__options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events in menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self._next_state = CharacterSelect(self._game)
                    self.__audio_manager.play_sound(Sounds.CLICK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.__options_rects):
                        if rect.collidepoint(event.pos):
                            self.__options[i]['action']()
                            self.__audio_manager.play_sound(Sounds.CLICK)

    def __start_from_beginning(self):
        self._load_from_save = False
        self._next_state = CharacterSelect(self._game)

    def __start_from_save(self):
        self._load_from_save = True
        try:
            with open("saves/save_game.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Error: save file not found! Starting new game")
            self.__start_from_beginning()
            return
        player_name = "Jones"  # Default name
        from src.states.Play import Play
        self._next_state = Play.from_dict(data, self._game, player_name)
