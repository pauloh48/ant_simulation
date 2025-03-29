import pygame
from global_var import GlobalVar

class Renderer:
    """
    Classe para renderização da simulação. Ele desenha todos os elementos da simulação incluindo a colônia, 
    fontes de comida, feromônios, formigas e informações de status. E gerencia FPS e quit.

    Atributos:
        screen: Superfície principal onde os elementos são desenhados.
        clock: Objeto para controlar a taxa de quadros (FPS).
        font: Fonte usada para o textos na tela.

    Métodos:
        render: Renderiza o estado atual do ambiente na tela.
        render_info: Renderiza informações de status na tela.
        check_quit(): Verifica se o programa deve encerrar.
    """
    
    def __init__(self):
        """
        Inicializa o sistema de renderização.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((GlobalVar.WINDOW_WIDTH, GlobalVar.WINDOW_HEIGHT))
        pygame.display.set_caption("Simulação de Formigas Evolutivas")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)
    
    def render(self, environment):
        """
        Renderiza o estado atual do ambiente que inclui a colônia; comidas; feromônios; formigas; informações.

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).
        """
        self.screen.fill(GlobalVar.WINDOW_BACKGROUND_COLOR)
        
        # Desenha colônia
        pygame.draw.circle(
            self.screen, 
            GlobalVar.COLONY_COLOR, 
            environment.colony.position, 
            GlobalVar.COLONY_RADIUS
        )
        
        # Desenha comida
        for food in environment.food_sources:
            pygame.draw.circle(
                self.screen,
                food.get_color(),
                food.position,
                food.get_size()
            )
        
        # Desenha feromônios
        for pheromone in environment.pheromones:
            # Intensidade determina o tamanho e a opacidade do feromônio
            size = max(1, min(3, pheromone.intensity / 5))
            alpha = int(min(255, pheromone.intensity * 80))
            
            # Cria uma superfície com canal alpha para transparência
            pheromone_surface = pygame.Surface((int(size*2), int(size*2)), pygame.SRCALPHA)
            pygame.draw.circle(
                pheromone_surface,
                (*GlobalVar.PHEROMONE_COLOR, alpha),  # Cor com canal alpha
                (int(size), int(size)),
                int(size)
            )
            self.screen.blit(pheromone_surface, (
                int(pheromone.position[0] - size),
                int(pheromone.position[1] - size)
            ))
        
        # Desenha formigas
        for ant in environment.colony.ants:
            # Tamanho da formiga baseado em sua velocidade
            ant_size = max(2, min(5, ant.ag_speed / 2 + 1))
            
            pygame.draw.circle(
                self.screen,
                ant.get_color(),
                ant.get_display_position(),
                ant_size
            )
    
        for ant_scout in environment.colony.ants_scout:
            # Tamanho da formiga baseado em sua velocidade
            ant_size = max(2, min(5, ant_scout.ag_speed / 2 + 1))
            
            pygame.draw.circle(
                self.screen,
                ant_scout.get_color(),
                ant_scout.get_display_position(),
                ant_size
            )
        
        # Desenha informações na tela
        self.render_info(environment)
                
        pygame.display.flip()
        self.clock.tick(GlobalVar.FPS)
    
    def render_info(self, environment):
        """
        Renderiza informações de status na tela, incluindo a geração atual, quantidade de comida coletada,
        quantidade de comida necessária para a próxima evolução, número de formigas e fontes de comida restantes e
        estatísticas médias da população (velocidade, detecção, força de feromônios).

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).
        """
        info_texts = [
            f"Geração: {environment.colony.generation}",
            f"Comida coletada: {environment.total_food_collected}",
            f"Próxima evolução: {GlobalVar.AG_FOOD_COLLECT_TO_EVOLVE - environment.food_delivery_count} comidas",
            f"Formigas: {len(environment.colony.ants)}",
            f"Fontes de comida: {len(environment.food_sources)}"
        ]
        
        # Estatísticas da população
        if environment.colony.ants:
            avg_speed = environment.colony.calculate_average(environment.colony.ants, "ag_speed")
            avg_sense = environment.colony.calculate_average(environment.colony.ants, "ag_pheromone_detection_range")
            avg_strength = environment.colony.calculate_average(environment.colony.ants, "ag_pheromone_strength")
            
            info_texts.extend([
                f"Velocidade média: {avg_speed:.2f}",
                f"Detecção média: {avg_sense:.2f}",
                f"Força feromônio média: {avg_strength:.2f}"
            ])
        
        # Renderiza textos
        y_offset = 10
        for text in info_texts:
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 20
    
    def check_quit(self):
        """
        Retorna False se o programa deve encerrar, True caso contrário.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
        return True