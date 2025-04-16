import pygame

from config.Constants import Constants, Colors
from src.states.AbstractState import AbstractState
from src.utils.AudioManager import AudioManager


class GameOver(AbstractState):
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
        self.__game_over_image = pygame.image.load(
            "assets/sprites/GameOver.png").convert_alpha()
        self.__game_over_image = pygame.transform.scale(
            self.__game_over_image, (
                Constants.WIDTH, Constants.HEIGHT))
        self.__score = score
        self.__font_large = pygame.font.Font(None, 120)
        self.__font_medium = pygame.font.Font(None, 60)
        self.__font_small = pygame.font.Font(None, 40)
        self.__audio_manager = AudioManager()
        self.__player_name = player_name

        # Menu options
        self.__options = [
            {'text': 'Reiniciar', 'action': self.__restart_game},
            {'text': 'Voltar ao Menu', 'action': self.__return_to_menu}
        ]

        self.__options_surfaces = []
        self.__options_rects = []

        # Create surfaces and rectangles for each option
        for i, option in enumerate(self.__options):
            surface = self.__font_small.render(option['text'], True,
                                               Colors.WHITE)
            rect = surface.get_rect(center=(
                Constants.WIDTH / 2, Constants.HEIGHT * 2 / 3 + i * 30))
            self.__options_surfaces.append(surface)
            self.__options_rects.append(rect)

    def __restart_game(self):
        """Restarts the game."""
        from src.states.Play import Play
        self._next_state = Play(self._game, self.__player_name)
        self.__audio_manager.unpause_music()

    def __return_to_menu(self):
        """Returns to the main menu."""
        from src.states.Menu import Menu
        self._next_state = Menu(self._game)
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
        screen.blit(self.__game_over_image, (0, 0))
        overlay = pygame.Surface((Constants.WIDTH, Constants.HEIGHT),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.__font_large.render("GAME OVER", True, Colors.RED)
        title_rect = title.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 3))
        screen.blit(title, title_rect)

        # Score
        score_text = self.__font_medium.render(f"Final Score: {self.__score}",
                                               True, Colors.WHITE)
        score_rect = score_text.get_rect(
            center=(Constants.WIDTH / 2, Constants.HEIGHT / 2))
        screen.blit(score_text, score_rect)

        # Draws the options
        for surface, rect in zip(self.__options_surfaces,
                                 self.__options_rects):
            screen.blit(surface, rect)

    def handle_events(self, events):
        """
        Processes pygame events during game over.

        :param events: List of pygame events to process.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self._is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    self.__restart_game()
                elif event.key == pygame.K_ESCAPE:  # Return to menu
                    self.__return_to_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(self.__options_rects):
                        if rect.collidepoint(event.pos):
                            self.__options[i]['action']()
