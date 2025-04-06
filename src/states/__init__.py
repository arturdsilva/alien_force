from abc import ABC, abstractmethod
import pygame


class GameState(ABC):
    """
    Classe base abstrata para os estados do jogo.
    """
    def __init__(self, game):
        self.game = game
        self.next_state = self

    @abstractmethod
    def update(self, dt):
        """Atualiza o estado."""
        pass

    @abstractmethod
    def draw(self, screen):
        """Desenha o estado na tela."""
        pass

    @abstractmethod
    def handle_events(self, events):
        """Processa eventos do pygame."""
        pass
