import pygame
from src.states import GameState
from src.states.CharacterSelect import CharacterSelect
from config.Constants import Constants


class Menu(GameState):
    """
    Estado do menu principal do jogo.
    """
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.title = self.font.render('Alien Force', True, pygame.Color('white'))
        self.title_rect = self.title.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/4))
        
        self.font_options = pygame.font.Font(None, 54)
        self.start_text = self.font_options.render('Pressione ESPAÇO para iniciar', True, pygame.Color('white'))
        self.start_rect = self.start_text.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT*3/4))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(pygame.Color('black'))
        screen.blit(self.title, self.title_rect)
        screen.blit(self.start_text, self.start_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = CharacterSelect(self.game)
