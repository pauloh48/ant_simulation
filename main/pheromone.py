class Pheromone:
    """
    Classe do feromônio ( tem decaimento ao longo do tempo).
    
    Atributos:
        position (): A posição (x, y) do feromônio.
        intensity (): A intensidade do feromônio (padrão = 1.0).    
    Métodos:
        gradual_decay(rate): Diminui a intensidade do feromônio multiplicando por taxa fornecida.
        is_active(): Se o feromônio está ativo (True e > 0.1) ou não (False).
    """
    def __init__(self, position, intensity=1.0):
        """
        Construtor de novo feromônio.

        Parameters:
            position: Coordenadas (x, y) que representam a posição do feromônio.
            intensity (opcional): Intensidade inicial do feromônio.
        """
        self.position = position
        self.intensity = intensity
        
    def gradual_decay(self, rate = 0.95):
        """
        Reduz a intensidade do feromônio pelo fator de taxa fornecido.

        Parameters:
            rate: A taxa de decaimento. O valor padrão é 0.95, ou seja, o decaimento é de 5% por chamada.
        """
        self.intensity *= rate
        
    def is_active(self):
        """
        Verifica se o feromônio ainda está ativo (intensidade > 0.1) no ambiente e retorna True, caso contrário False.
        """
        return self.intensity > 0.1

