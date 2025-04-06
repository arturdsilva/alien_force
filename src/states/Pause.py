import pygame
from src.states import GameState
from config.Constants import Constants


class Pause(GameState):
    """
    Estado de pausa do jogo.
    """
    def __init__(self, game, play_state):
        """
        Inicializa o menu de pausa.

        :param game: A instância principal do jogo.
        :param play_state: O estado do jogo que foi pausado.
        """
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
        """
        Atualiza o estado do menu de pausa.

        :param dt: O intervalo de tempo desde a última atualização.
        """
        pass

    def draw(self, screen):
        """
        Desenha o menu de pausa.

        :param screen: A superfície da tela onde desenhar.
        """
        # Desenha o estado atual do jogo (congelado)
        self.play_state.draw(screen)
        
        # Cria uma superfície semi-transparente para escurecer o jogo
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT))
        overlay.fill(pygame.Color('black'))
        overlay.set_alpha(128)  # 128 é 50% de opacidade
        screen.blit(overlay, (0, 0))
        
        # Desenha o menu de pausa
        screen.blit(self.title, self.title_rect)
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processa eventos do pygame no menu de pausa.

        :param events: Lista de eventos do pygame para processar.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.resume_game()
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_menu()

    def resume_game(self):
        """
        Retorna ao jogo pausado.
        """
        self.next_state = self.play_state

    def return_to_menu(self):
        """
        Retorna ao menu principal.
        """
        from src.states.Menu import Menu
        self.next_state = Menu(self.game)
