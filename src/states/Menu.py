import json

import pygame

from config.Constants import Constants, Sounds
from src.states.GameState import GameState
from src.states.CharacterSelect import CharacterSelect
from src.utils.AudioManager import AudioManager


class Menu(GameState):
    """
    Main menu game state.
    """

    def __init__(self, game):
        """
        Initializes the main menu.

        :param game: The main game instance.
        """
        super().__init__(game)
        self.bg_image = pygame.image.load("assets/sprites/Menu.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (Constants.WIDTH, Constants.HEIGHT))
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Alien Force', True,
                                      pygame.Color('white'))
        self.title_rect = self.title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 4))

        self.font_options = pygame.font.Font(None, 54)

        self.__audio_manager = AudioManager()

        self.options = [
            {'text': 'ESPAÇO: Novo Jogo', 'action':
                self.start_from_beginning},
            {'text': 'C: Continuar Jogo Salvo',
             'action': self.start_from_save},
        ]

        self.options_surfaces = []
        self.options_rects = []

        for i, option in enumerate(self.options):
            surface = self.font_options.render(option['text'], True,
                                               pygame.Color('white'))
            rect = surface.get_rect(
                center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + i * 60))
            self.options_surfaces.append(surface)
            self.options_rects.append(rect)

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
        screen.blit(self.bg_image, (0, 0))
        screen.blit(self.title, self.title_rect)
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events in menu.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = CharacterSelect(self.game)
                    self.__audio_manager.play_sound(Sounds.CLICK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.options_rects):
                        if rect.collidepoint(event.pos):
                            self.options[i]['action']()
                            self.__audio_manager.play_sound(Sounds.CLICK)

    def start_from_beginning(self):
        self.load_from_save = False
        self.next_state = CharacterSelect(self.game)

    def start_from_save(self):
        self.load_from_save = True
        try:
            with open("saves/save_game.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Error: save file not found! Starting new game")
            self.start_from_beginning()
            return
        player_name = "Jones"  # Default name
        from src.states.Play import Play
        self.next_state = Play.from_dict(data, self.game, player_name)
