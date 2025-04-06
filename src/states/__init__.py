from abc import ABC, abstractmethod
import pygame


class GameState(ABC):
    """
    Classe base abstrata para os estados do jogo.
    """
    def __init__(self, game):
        """
        Inicializa um estado do jogo.

        :param game: A instância principal do jogo.
        """
        self.game = game
        self.next_state = self

    @abstractmethod
    def update(self, dt):
        """
        Atualiza o estado.

        :param dt: O intervalo de tempo desde a última atualização.
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Desenha o estado na tela.

        :param screen: A superfície da tela onde desenhar.
        """
        pass

    @abstractmethod
    def handle_events(self, events):
        """
        Processa eventos do pygame.

        :param events: Lista de eventos do pygame para processar.
        """
        pass
