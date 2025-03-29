class FoodSource:
    """
    Classe da fonte de comida. Ela é espalhada pelo ambiente que as formigas podem coletar e levar de volta para 
    a colônia. A quantidade de comida diminui conforme é coletada, e a representação visual muda dinamicamente.
    
    Atributos:
        position: Coordenadas (x, y) da fonte de comida.
        stock: Quantidade de unidades de comida disponíveis.
    
    Métodos:
        decrement_food_stock(): Remove uma unidade de comida e retorna True (há comida), False (contrário).
        get_color(): Calcula a cor da comida com base na quantidade restante.
        get_size(): Calcula o tamanho da representação visual da comida (diminui quando é consumida).
    """
    def __init__(self, position, stock):
        """
        Construtor de nova fonte de comida.

        Parameters:
            position: Coordenadas (x, y) da fonte de comida.
            stock: Quantidade inicial de unidades de comida disponíveis.
        """
        self.position = position
        self.stock = stock
    
    def decrement_food_stock(self):
        """
        Remove uma unidade de comida da fonte.
        """
        self.stock -= 1
        return self.stock > 0
    
    def get_color(self):
        """
        Determina e retorna a cor da comida dinamicamente com base na quantidade restante.
        """
        intensity = 190 - (self.stock * 10)
        return (190 - intensity, 17, 18)
    
    def get_size(self):
        """
        Retorna o tamanho da representação visual da comida. O tamanho combina um valor base (5px) com a quantidade 
        disponível (stock). Conforme a comida é consumida o tamanho diminui. Quando o estoque se esgota o tamanho 
        retorna ao mínimo e a comida é removida do ambiente.
        """
        return 5 + self.stock
