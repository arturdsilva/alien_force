import pygame

from config.Constants import Constants, Sounds
from src.entities.players.Cyborg import Cyborg
from src.entities.players.Jones import Jones
from src.entities.players.Rain import Rain
from src.states.AbstractState import AbstractState
from src.states.Play import Play
from src.utils.AudioManager import AudioManager


class CharacterSelect(AbstractState):
    """
    Character selection state.
    """

    def __init__(self, game):
        """
        Initializes the character selection screen.

        :param game: The main game instance.
        """
        super().__init__(game)

        self.__bg_image = pygame.image.load(
            "assets/sprites/Menu.png").convert()
        self.__bg_image = pygame.transform.scale(self.__bg_image, (
            Constants.WIDTH, Constants.HEIGHT))
        # Font configuration
        self.__font_title = pygame.font.Font(None, 74)
        self.__font_chars = pygame.font.Font(None, 54)
        self.__font_desc = pygame.font.Font(None, 36)

        self.__title = self.__font_title.render('Selecione seu Personagem',
                                                True,
                                                pygame.Color('white'))
        self.__title_rect = self.__title.get_rect(
            center=(Constants.WIDTH / 2, 80))

        # Available characters
        self.__characters = [
            {
                'name': 'Captain Cyborg',
                'class': Cyborg,
                'desc': 'Especialista em armas de assalto',
                'image': pygame.image.load(
                    "assets/sprites/players/CyborgIdle.png").convert_alpha()
            },
            {
                'name': 'Sergeant Jones',
                'class': Jones,
                'desc': 'Especialista em explosivos',
                'image': pygame.image.load(
                    "assets/sprites/players/JonesIdle.png").convert_alpha()
            },
            {
                'name': 'Lieutenant Rain',
                'class': Rain,
                'desc': 'Especialista em precisão',
                'image': pygame.image.load(
                    "assets/sprites/players/RainIdle.png").convert_alpha()
            }
        ]

        self.__selected = 0
        self.__preview_size = 150

        self.__char_name = None
        self.__char_name_rect = None
        self.__char_desc = None
        self.__char_desc_rect = None
        self.__controls = None
        self.__controls_rect = None
        self.__update_character_info()

        char = self.__characters[self.__selected]
        orig_width, orig_height = char['image'].get_size()
        new_height = 150
        new_width = int((orig_width / orig_height) * new_height)
        self.__image = pygame.transform.scale(char['image'],
                                              (new_width, new_height))

        self.__preview_rect = self.__image.get_rect(
            center=(Constants.WIDTH // 2, Constants.HEIGHT // 2))

        self.__right_arrow = self.__font_chars.render('>', True,
                                                      pygame.Color('white'))
        self.__right_rect = self.__right_arrow.get_rect(
            midleft=(self.__preview_rect.right + 30, Constants.HEIGHT / 2))

        self.__left_arrow = self.__font_chars.render('<', True,
                                                     pygame.Color('white'))
        self.__left_rect = self.__left_arrow.get_rect(
            midright=(self.__preview_rect.left - 30, Constants.HEIGHT / 2))

        self.__audio_manager = AudioManager()

    def __update_character_info(self):
        """
        Updates the selected character information.
        """
        char = self.__characters[self.__selected]

        # Character name
        self.__char_name = self.__font_chars.render(char['name'], True,
                                                    pygame.Color('white'))
        self.__char_name_rect = self.__char_name.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 - 100))

        # Character description
        self.__char_desc = self.__font_desc.render(char['desc'], True,
                                                   pygame.Color('white'))
        self.__char_desc_rect = self.__char_desc.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + 100))

        self.__controls = self.__font_desc.render('ESPAÇO para confirmar',
                                                  True,
                                                  pygame.Color('white'))
        self.__controls_rect = self.__controls.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT - 80))

        char = self.__characters[self.__selected]
        orig_width, orig_height = char['image'].get_size()
        new_height = 150
        new_width = int((orig_width / orig_height) * new_height)
        self.__image = pygame.transform.scale(char['image'],
                                              (new_width, new_height))

    def update(self, dt):
        """
        Updates the character selection state.

        :param dt: Time interval since last update.
        """
        pass

    def draw(self, screen):
        """
        Draws the character selection screen.

        :param screen: The screen surface to draw on.
        """
        screen.blit(self.__bg_image, (0, 0))

        # Draw title
        screen.blit(self.__title, self.__title_rect)

        # Draw character preview
        screen.blit(self.__image, self.__preview_rect)

        # Draw navigation arrows
        if self.__selected > 0:
            screen.blit(self.__left_arrow, self.__left_rect)

        if self.__selected < len(self.__characters) - 1:
            screen.blit(self.__right_arrow, self.__right_rect)

        # Draw name and description
        screen.blit(self.__char_name, self.__char_name_rect)
        screen.blit(self.__char_desc, self.__char_desc_rect)
        screen.blit(self.__controls, self.__controls_rect)

    def handle_events(self, events):
        """
        Processes pygame events in character selection.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._is_running = False
            if event.type == pygame.KEYDOWN:
                if (
                        event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.__selected > 0:
                    self.__selected -= 1
                    self.__update_character_info()
                    self.__audio_manager.play_sound(Sounds.CLICK)
                elif (
                        event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.__selected < len(
                    self.__characters) - 1:
                    self.__selected += 1
                    self.__update_character_info()
                    self.__audio_manager.play_sound(Sounds.CLICK)
                elif event.key == pygame.K_SPACE:
                    selected_char = self.__characters[self.__selected][
                        'class']()
                    selected_char_name = selected_char.__class__.__name__
                    self._next_state = Play(self._game, selected_char_name)
                    self.__audio_manager.play_sound(Sounds.CLICK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    # Check if clicked on navigation arrows
                    preview_rect = pygame.Rect(0, 0, self.__preview_size,
                                               self.__preview_size)
                    preview_rect.center = (
                        Constants.WIDTH / 2, Constants.HEIGHT / 2)

                    if self.__selected > 0:
                        if self.__left_rect.collidepoint(mouse_pos):
                            self.__selected -= 1
                            self.__update_character_info()
                            self.__audio_manager.play_sound(Sounds.CLICK)

                    if self.__selected < len(self.__characters) - 1:
                        if self.__right_rect.collidepoint(mouse_pos):
                            self.__selected += 1
                            self.__update_character_info()
                            self.__audio_manager.play_sound(Sounds.CLICK)

                    # Check if clicked on character preview
                    if preview_rect.collidepoint(mouse_pos):
                        selected_char = self.__characters[self.__selected][
                            'class']()
                        selected_char_name = selected_char.__class__.__name__
                        self._next_state = Play(self._game,
                                                selected_char_name)
                        self.__audio_manager.play_sound(Sounds.CLICK)
