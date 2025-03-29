import random
from ant import euclidean_distance
from colony import Colony
from food_source import FoodSource
from pheromone import Pheromone
from global_var import GlobalVar

class Environment:
    """
    Classe para gerenciar o ambiente. Ele contém a colônia de formigas, fontes de comida e feromônios.
    Ele é responsável por atualizar o estado da simulação, incluindo o movimento das formigas, a evolução genética 
    e o gerenciamento de feromônios e comida.

    Atributos:
        colony: A colônia de formigas no ambiente.
        food_sources: Fontes de comida disponíveis no ambiente.
        pheromones: Feromônios ativos no ambiente.
        food_delivery_count: Contador de entregas de comida desde a última evolução.
        total_food_collected: Quantidade total de comida coletada na simulação.

    Métodos:
        create_random_food_sources(num_food): Gera fontes de comida em posições aleatórias.
        update(): Atualiza o estado do ambiente, incluindo o movimento das formigas e a evolução.
        update_pheromones(): Atualiza a intensidade dos feromônios (remove os inativos).
        find_nearest_pheromone(position, max_distance): Encontra o feromônio mais próximo de uma posição.
        find_nearest_food(position): Encontra a fonte de comida mais próxima de uma posição.
        take_food(food_source): Remove uma unidade de comida de uma fonte e verifica se ainda há comida.
        add_pheromone(position, strength): Adiciona um novo feromônio na posição especificada.
    """
    def __init__(self):
        """
        Construtor do ambiente da simulação.
        """
        self.colony = Colony(GlobalVar.WINDOW_WIDTH // 2, GlobalVar.WINDOW_HEIGHT // 2)
        self.food_sources = []
        self.pheromones = []
        
        self.create_random_food_sources(GlobalVar.FOOD_AVAILABLE)
        self.colony.create_ants(GlobalVar.ANT_POPULATION_SIZE)
        
        self.food_delivery_count = 0
        self.total_food_collected = 0
    
    def create_random_food_sources(self, num_food):
        """
        Cria fontes de comida em posições aleatórias.

        Parameters:
            num_food: Quantidade de fontes de comida a serem criadas.
        """
        for _ in range(num_food):
            pos = (
                random.randint(50, GlobalVar.WINDOW_WIDTH - 50),
                random.randint(50, GlobalVar.WINDOW_HEIGHT - 50)
            )
            self.food_sources.append(FoodSource(pos, GlobalVar.FOOD_STORAGE_CAPACITY))
    
    def update(self):
        """
        Atualiza o estado do ambiente, realizando as seguintes ações:
            Move as formigas e realiza interações com comida e colônia.
            Evolui as formigas se a quantidade de comida entregue atingir o limite.
            Atualiza a intensidade dos feromônios no ambiente.
        """
        food_delivered_count = 0
        
        for ant in self.colony.ants:
            food_delivered = ant.move(self)
            if food_delivered:
                food_delivered_count += 1
                self.food_delivery_count += 1
                self.colony.food_collected += 1
                self.total_food_collected += 1

        for ant_scout in self.colony.ants_scout:
            food_delivered = ant_scout.move(self)
            if food_delivered:
                food_delivered_count += 1
                self.food_delivery_count += 1
                self.colony.food_collected += 1
                self.total_food_collected += 1
        
        # Evolui formigas se necessário
        if self.food_delivery_count >= GlobalVar.AG_FOOD_COLLECT_TO_EVOLVE:
            self.colony.evolve_ants()
            self.food_delivery_count = 0
        
        # Atualiza feromônios
        self.update_pheromones()
    
    def update_pheromones(self):
        """
        Atualiza a intensidade dos feromônios e remove os inativos.
        """
        active_pheromones = []
        for pheromone in self.pheromones:
            pheromone.gradual_decay(GlobalVar.PHEROMONE_DECAY_RATE)
            
            if pheromone.is_active():
                active_pheromones.append(pheromone)
        
        self.pheromones = active_pheromones
    
    def find_nearest_pheromone(self, position, max_distance):
        """
        Encontra o feromônio mais próximo da posição da formiga em uma distância máxima.

        Parameters:
            position: A posição (x, y) da formiga.
            max_distance: A distância máxima para considerar feromônios.

        Returns:
            Pheromone: O feromônio mais próximo ou None se nenhum for encontrado.
        """
        if not self.pheromones:
            return None
        
        # Filtra feromônios dentro do alcance
        in_range_pheromones = []
        for phero in self.pheromones:
            distance = euclidean_distance(position, phero.position)
            if distance <= max_distance:
                in_range_pheromones.append(phero)
                
        if not in_range_pheromones:
            return None
            
        # Escolhe o mais próximo, ponderado pela intensidade
        best_pheromone = None
        best_attractiveness = -1
        
        for pheromone in in_range_pheromones:
            distance = max(1, euclidean_distance(position, pheromone.position))
            attractiveness = pheromone.intensity / distance
            
            if best_pheromone is None or attractiveness > best_attractiveness:
                best_pheromone = pheromone
                best_attractiveness = attractiveness
        
        return best_pheromone
    
    def find_nearest_food(self, position):
        """
        Encontra a fonte de comida mais próxima.

        Parameters:
            position: A posição (x, y) da formiga.

        Returns:
            FoodSource: A fonte de comida mais próxima ou None se nenhuma for encontrada.
        """
        if not self.food_sources:
            return None
        
        nearest_food = None
        min_distance = float('inf')
        for food in self.food_sources:
            distance = euclidean_distance(position, food.position)
            if distance < min_distance:
                min_distance = distance
                nearest_food = food
        
        return nearest_food
    
    def take_food(self, food_source):
        """
        Remove uma unidade de comida e verifica se ainda há comida.

        Parameters:
            food_source: A fonte de comida de onde será retirada a unidade.

        Returns:
            bool: True se ainda houver comida, False caso contrário.
        """
        has_food = food_source.decrement_food_stock()
        if not has_food:
            self.food_sources.remove(food_source)
        return has_food
    
    def add_pheromone(self, position, strength = 1.0):
        """
        Adiciona novo feromônio em determinada posição.

        Parameters:
            position: A posição (x, y) onde o feromônio será adicionado.
            strength (opcional): A força inicial do feromônio (padrão = 1.0).
        """
        intensity = GlobalVar.FOOD_STORAGE_CAPACITY * strength
        self.pheromones.append(Pheromone(position, intensity))
