import pygame
from src.states import GameState
from config.Constants import Constants, Colors


class GameOver(GameState):
    """
    Estado de game over do jogo.
    Mostra o score final e opções para reiniciar ou voltar ao menu.
    """

    def __init__(self, game, score):
        """
        Inicializa o estado de game over.

        :param game: A instância principal do jogo.
        :param score: O score final do jogador.
        """
        super().__init__(game)
        self.score = score
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def update(self, dt):
        """
        Atualiza o estado de game over.
        Não há atualizações necessárias neste estado.

        :param dt: O intervalo de tempo desde a última atualização.
        """
        pass

    def draw(self, screen):
        """
        Desenha a tela de game over.

        :param screen: A superfície da tela onde desenhar.
        """
        # Fundo escuro semi-transparente
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Título
        title = self.font_large.render("GAME OVER", True, Colors.RED)
        title_rect = title.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/3))
        screen.blit(title, title_rect)

        # Score
        score_text = self.font_medium.render(f"Score Final: {self.score}", True, Colors.WHITE)
        score_rect = score_text.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2))
        screen.blit(score_text, score_rect)

        # Instruções
        restart_text = self.font_small.render("Pressione R para reiniciar", True, Colors.WHITE)
        menu_text = self.font_small.render("Pressione M para voltar ao menu", True, Colors.WHITE)
        
        restart_rect = restart_text.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT*2/3))
        menu_rect = menu_text.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT*2/3 + 30))
        
        screen.blit(restart_text, restart_rect)
        screen.blit(menu_text, menu_rect)

    def handle_events(self, events):
        """
        Processa eventos do pygame durante o game over.

        :param events: Lista de eventos do pygame para processar.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    from src.states.CharacterSelect import CharacterSelect
                    self.next_state = CharacterSelect(self.game)
                elif event.key == pygame.K_m:  # Voltar ao menu
                    from src.states.Menu import Menu
                    self.next_state = Menu(self.game) 