import pygame
from src.states.GameState import GameState
from config.Constants import Constants, Colors, Sounds
from src.utils.AudioManager import AudioManager


class GameOver(GameState):
    """
    Game over state of the game.
    Shows the final score and options to restart or return to menu.
    """

    def __init__(self, game, score, player_name="Unknown"):
        """
        Initializes the game over state.

        :param game: The main game instance.
        :param score: The player's final score.
        """
        super().__init__(game)
        self.score = score
        self.font_large = pygame.font.Font(None, 120)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)
        self.__audio_manager = AudioManager()
        self.player_name = player_name

        # Opções do menu
        self.options = [
            {'text': 'Reiniciar', 'action': self.restart_game},
            {'text': 'Voltar ao Menu', 'action': self.return_to_menu}
        ]

        self.options_surfaces = []
        self.options_rects = []

        # Cria as superfícies e retângulos para cada opção
        for i, option in enumerate(self.options):
            surface = self.font_small.render(option['text'], True,
                                             Colors.WHITE)
            rect = surface.get_rect(center=(
                Constants.WIDTH / 2, Constants.HEIGHT * 2 / 3 + i * 30))
            self.options_surfaces.append(surface)
            self.options_rects.append(rect)

    def restart_game(self):
        """Reinicia o jogo."""
        from src.states.Play import Play
        self.next_state = Play(self.game, self.player_name)
        self.__audio_manager.unpause_music()

    def return_to_menu(self):
        """Volta para o menu principal."""
        from src.states.Menu import Menu
        self.next_state = Menu(self.game)
        self.__audio_manager.unpause_music()

    def update(self, dt):
        """
        Updates the game over state.
        No updates are needed in this state.

        :param dt: Time since last update.
        """
        pass

    def draw(self, screen):
        """
        Draws the game over screen.

        :param screen: The screen surface to draw on.
        """
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.font_large.render("GAME OVER", True, Colors.RED)
        title_rect = title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))
        screen.blit(title, title_rect)

        # Score
        score_text = self.font_medium.render(f"Final Score: {self.score}",
                                             True, Colors.WHITE)
        score_rect = score_text.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2))
        screen.blit(score_text, score_rect)

        # Desenha as opções
        for surface, rect in zip(self.options_surfaces, self.options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events during game over.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:  # Voltar ao menu
                    self.return_to_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.options_rects):
                        if rect.collidepoint(event.pos):
                            self.options[i]['action']()
