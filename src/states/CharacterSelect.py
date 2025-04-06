import pygame
from src.states import GameState
from src.states.Play import Play
from src.entities.players.Kane import Kane
from src.entities.players.Jones import Jones
from src.entities.players.Rain import Rain
from config.Constants import Constants


class CharacterSelect(GameState):
    """
    Estado de seleção de personagem.
    """
    def __init__(self, game):
        """
        Inicializa a tela de seleção de personagem.

        :param game: A instância principal do jogo.
        """
        super().__init__(game)
        # Configuração das fontes
        self.font_title = pygame.font.Font(None, 74)
        self.font_chars = pygame.font.Font(None, 54)
        self.font_desc = pygame.font.Font(None, 36)
        
        # Título
        self.title = self.font_title.render('Selecione seu Personagem', True, pygame.Color('white'))
        self.title_rect = self.title.get_rect(center=(Constants.WIDTH/2, 80))
        
        # Personagens disponíveis
        self.characters = [
            {
                'name': 'Capitão Kane',
                'class': Kane,
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

    def update_character_info(self):
        """
        Atualiza as informações do personagem selecionado.
        """
        char = self.characters[self.selected]
        
        # Nome do personagem
        self.char_name = self.font_chars.render(char['name'], True, char['color'])
        self.char_name_rect = self.char_name.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2 - 100))
        
        # Descrição do personagem
        self.char_desc = self.font_desc.render(char['desc'], True, pygame.Color('white'))
        self.char_desc_rect = self.char_desc.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2 + 100))
        
        # Controles
        self.controls = self.font_desc.render('ESPAÇO para confirmar', True, pygame.Color('white'))
        self.controls_rect = self.controls.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT - 80))

    def update(self, dt):
        """
        Atualiza o estado da seleção de personagem.

        :param dt: O intervalo de tempo desde a última atualização.
        """
        pass

    def draw(self, screen):
        """
        Desenha a tela de seleção de personagem.

        :param screen: A superfície da tela onde desenhar.
        """
        screen.fill(pygame.Color('black'))
        
        # Desenha o título
        screen.blit(self.title, self.title_rect)
        
        # Desenha o preview do personagem
        char = self.characters[self.selected]
        preview = pygame.Surface((self.preview_size, self.preview_size))
        preview.fill(char['color'])
        preview_rect = preview.get_rect(center=(Constants.WIDTH/2, Constants.HEIGHT/2))
        screen.blit(preview, preview_rect)
        
        # Desenha setas de navegação
        if self.selected > 0:
            left_arrow = self.font_chars.render('<', True, pygame.Color('white'))
            left_rect = left_arrow.get_rect(midright=(preview_rect.left - 30, Constants.HEIGHT/2))
            screen.blit(left_arrow, left_rect)
            
        if self.selected < len(self.characters) - 1:
            right_arrow = self.font_chars.render('>', True, pygame.Color('white'))
            right_rect = right_arrow.get_rect(midleft=(preview_rect.right + 30, Constants.HEIGHT/2))
            screen.blit(right_arrow, right_rect)
        
        # Desenha nome e descrição
        screen.blit(self.char_name, self.char_name_rect)
        screen.blit(self.char_desc, self.char_desc_rect)
        screen.blit(self.controls, self.controls_rect)

    def handle_events(self, events):
        """
        Processa eventos do pygame na seleção de personagem.

        :param events: Lista de eventos do pygame para processar.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.selected > 0:
                    self.selected -= 1
                    self.update_character_info()
                elif event.key == pygame.K_RIGHT and self.selected < len(self.characters) - 1:
                    self.selected += 1
                    self.update_character_info()
                elif event.key == pygame.K_SPACE:
                    selected_char = self.characters[self.selected]['class']()
                    self.next_state = Play(self.game, selected_char) 