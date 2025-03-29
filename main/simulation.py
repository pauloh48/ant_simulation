import pygame

from environment import Environment
from renderer import Renderer

class Simulation:
    """
    Classe da similução, ela integra o environment com o renderer e controla a execução  da simulação.

    Atributos:
        environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).
        renderer: Exibe os elementos na tela.
        running: Se a simulação está ou não em execução.

    Métodos:
        run(): Executa o loop da simulação.
    """
    def __init__(self):
        """
        Cria o ambiente e o sistema de renderização.
        """
        self.environment = Environment()
        self.renderer = Renderer()
        self.running = True
    
    def run(self):
        """
        Executa o loop principal e verifica se o programa deve encerrar, atualiza o estado 
        do ambiente (movimento das formigas, evolução, etc.) e fica renderizando a tela.
        """
        while self.running:
            is_quit = self.renderer.check_quit()
            
            if is_quit == False:
                self.running = False
            else:
                self.environment.update()
                self.renderer.render(self.environment)
        
        pygame.quit()

