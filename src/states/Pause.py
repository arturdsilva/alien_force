import pygame
from src.states import GameState
from config.Constants import Constants


class Pause(GameState):
    """
    Estado de pausa do jogo.
    """
    def __init__(self, game, play_state):
        super().__init__(game)
        self.play_state = play_state  # Guarda o estado do jogo para poder retornar
        self.next_state = self 
        
        # Configuração das fontes
        self.font_title = pygame.font.Font(None, 74)
        self.font_options = pygame.font.Font(None, 48)
        
        # Título
        self.title = self.font_title.render('PAUSADO', True, pygame.Color('white'))
        self.title_rect = self.title.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/3))
        
        # Opções
        self.options = [
            {'text': 'Continuar (P)', 'action': self.resume_game},
            {'text': 'Menu Principal (ESC)', 'action': self.return_to_menu}
        ]
        
        self.options_surfaces = []
        self.options_rects = []
        
        for i, option in enumerate(self.options):
            surface = self.font_options.render(option['text'], True, pygame.Color('white'))
            rect = surface.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2 + i * 60))
            self.options_surfaces.append(surface)
            self.options_rects.append(rect)

    def update(self, dt):
        pass

    def draw(self, screen):
        self.play_state.draw(screen)
        
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128) 
        screen.blit(overlay, (0, 0))
        
        screen.blit(self.title, self.title_rect)
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.resume_game()
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu()

    def resume_game(self):
        """Retorna ao jogo."""
        self.next_state = self.play_state

    def return_to_menu(self):
        """Retorna ao menu principal."""
        from src.states.Menu import Menu
        self.next_state = Menu(self.game)
