import pygame

from config.Constants import Constants, Sounds
from src.entities.players.Jones import Jones
from src.entities.players.Cyborg import Cyborg
from src.entities.players.Rain import Rain
from src.states.GameState import GameState
from src.states.Play import Play
from src.utils.AudioManager import AudioManager


class CharacterSelect(GameState):
    """
    Character selection state.
    """

    def __init__(self, game):
        """
        Initializes the character selection screen.

        :param game: The main game instance.
        """
        super().__init__(game)
        # Font configuration
        self.font_title = pygame.font.Font(None, 74)
        self.font_chars = pygame.font.Font(None, 54)
        self.font_desc = pygame.font.Font(None, 36)

        # Título
        self.title = self.font_title.render('Selecione seu Personagem', True,
                                            pygame.Color('white'))
        self.title_rect = self.title.get_rect(
            center=(Constants.WIDTH / 2, 80))

        # Available characters
        self.characters = [
            {
                'name': 'Captain Cyborg',
                'class': Cyborg,
                'desc': 'Especialista em armas de assalto',
                'color': pygame.Color('steelblue')
            },
            {
                'name': 'Sargento Jones',
                'class': Jones,
                'desc': 'Especialista em explosivos',
                'color': pygame.Color('olive')
            },
            {
                'name': 'Tenente Rain',
                'class': Rain,
                'desc': 'Especialista em precisão',
                'color': pygame.Color('darkgreen')
            }
        ]

        self.selected = 0
        self.preview_size = 150
        self.update_character_info()
        self.__audio_manager = AudioManager()

    def update_character_info(self):
        """
        Updates the selected character information.
        """
        char = self.characters[self.selected]

        # Character name
        self.char_name = self.font_chars.render(char['name'], True,
                                                char['color'])
        self.char_name_rect = self.char_name.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 - 100))

        # Character description
        self.char_desc = self.font_desc.render(char['desc'], True,
                                               pygame.Color('white'))
        self.char_desc_rect = self.char_desc.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2 + 100))

        # Controles
        self.controls = self.font_desc.render('ESPAÇO para confirmar', True,
                                              pygame.Color('white'))
        self.controls_rect = self.controls.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT - 80))

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
        screen.fill(pygame.Color('black'))

        # Draw title
        screen.blit(self.title, self.title_rect)

        # Draw character preview
        char = self.characters[self.selected]
        preview = pygame.Surface((self.preview_size, self.preview_size))
        preview.fill(char['color'])
        preview_rect = preview.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2))
        screen.blit(preview, preview_rect)

        # Draw navigation arrows
        if self.selected > 0:
            left_arrow = self.font_chars.render('<', True,
                                                pygame.Color('white'))
            left_rect = left_arrow.get_rect(
                midright=(preview_rect.left - 30, Constants.HEIGHT / 2))
            screen.blit(left_arrow, left_rect)

        if self.selected < len(self.characters) - 1:
            right_arrow = self.font_chars.render('>', True,
                                                 pygame.Color('white'))
            right_rect = right_arrow.get_rect(
                midleft=(preview_rect.right + 30, Constants.HEIGHT / 2))
            screen.blit(right_arrow, right_rect)

        # Draw name and description
        screen.blit(self.char_name, self.char_name_rect)
        screen.blit(self.char_desc, self.char_desc_rect)
        screen.blit(self.controls, self.controls_rect)

    def handle_events(self, events):
        """
        Processes pygame events in character selection.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.selected > 0:
                    self.selected -= 1
                    self.update_character_info()
                    self.__audio_manager.play_sound(Sounds.CLICK)
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.selected < len(self.characters) - 1:
                    self.selected += 1
                    self.update_character_info()
                    self.__audio_manager.play_sound(Sounds.CLICK)
                elif event.key == pygame.K_SPACE:
                    selected_char = self.characters[self.selected]['class']()
                    selected_char_name = selected_char.__class__.__name__
                    self.next_state = Play(self.game, selected_char_name)
                    self.__audio_manager.play_sound(Sounds.CLICK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = event.pos
                    # Check if clicked on navigation arrows
                    preview_rect = pygame.Rect(0, 0, self.preview_size, self.preview_size)
                    preview_rect.center = (Constants.WIDTH/2, Constants.HEIGHT/2)
                    
                    if self.selected > 0:
                        left_arrow = self.font_chars.render('<', True, pygame.Color('white'))
                        left_rect = left_arrow.get_rect(midright=(preview_rect.left - 30, Constants.HEIGHT/2))
                        if left_rect.collidepoint(mouse_pos):
                            self.selected -= 1
                            self.update_character_info()
                            self.__audio_manager.play_sound(Sounds.CLICK)

                    if self.selected < len(self.characters) - 1:
                        right_arrow = self.font_chars.render('>', True, pygame.Color('white'))
                        right_rect = right_arrow.get_rect(midleft=(preview_rect.right + 30, Constants.HEIGHT/2))
                        if right_rect.collidepoint(mouse_pos):
                            self.selected += 1
                            self.update_character_info()
                            self.__audio_manager.play_sound(Sounds.CLICK)

                    # Check if clicked on character preview
                    if preview_rect.collidepoint(mouse_pos):
                        selected_char = self.characters[self.selected]['class']()
                        selected_char_name = selected_char.__class__.__name__
                        self.next_state = Play(self.game, selected_char_name)
                        self.__audio_manager.play_sound(Sounds.CLICK)
