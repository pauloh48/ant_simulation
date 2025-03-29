import random
from global_var import GlobalVar
from ant import Ant
from ant_scout import Ant_Scout

class Colony:
    """
    Classe da colônia de formigas. Elas gerencia as formigas (normais e exploradoras) [criação, atualização 
    e evolução], coleta de comida e estatísticas da simulação. 
    
    Atributos:
        x, y: Coordenadas da colônia.
        food_collected: Quantidade de comida coletada.
        ants: Lista de formigas normais.
        ants_scout: Lista de formigas exploradoras.
        generation: Geração atual da colônia.

    Métodos:
        position(): Retorna a posição da colônia.
        create_ants(num_ants): Cria as formigas iniciais (normais e exploradoras).
        initialize_ants(num_ants, is_scout): Inicializa uma lista com todas as formigas.
        evolve_ants(): Evolui a população de formigas.
        get_ant_fitness(ant): Seleciona o fitness de uma formiga.
        evolve_population(): Evolui a população de formigas.
        tournament(): Seleciona dois pais para reprodução usando torneio.
        crossover_ants(parent1, parent2): Faz o cruzamento entre dois pais para gerar filho.
        select_elite_ants(): Escolhe as formigas de elite com base no fitness.
        select_parent(): Escolhe um pai para reprodução usando torneio.
        print_statistics(): Imprime estatísticas da geração atual.
    """
    def __init__(self, x, y):
        """
        Construtor da colônia de formigas.

        Parameters:
            x, y: Coordenadas da colônia.
        """
        self.x = x
        self.y = y
        self.food_collected = 0
        self.ants = []
        self.ants_scout = []
        self.generation = 1
    
    @property
    def position(self):
        """
        Retorna a posição da colônia.
        """
        return (self.x, self.y)
    
    def create_ants(self, num_ants):
        """
        Cria as formigas iniciais (normais e exploradoras).

        Parameters:
            num_ants: Quantidade de formigas normais.
        """
        self.ants = self.initialize_ants(num_ants, is_scout=False)
        self.ants_scout = self.initialize_ants(GlobalVar.ANT_SCOUT_COLOR_POPULATION_SIZE, is_scout=True)

    def initialize_ants(self, num_ants, is_scout=False):
        """
        Inicializa uma lista com todas as formigas.

        Parameters:
            num_ants: Quantidade a serem criadas.
            is_scout: Se é exporadora ou não.

        Returns:
            list: Lista de formigas geradas.
        """
        if not is_scout:
            Ant_Type = Ant   
        else:
            Ant_Type = Ant_Scout
        
        ants = []
        for _ in range(num_ants):
            ant = Ant_Type(self.x, self.y)
            ants.append(ant)
        return ants
    
    def evolve_ants(self):
        """
        Evolui a população de formigas usando algoritmo genético.
        """
        self.generation += 1
        
        self.evolve_population()

    def get_ant_fitness(self, ant):
        """
        Retorna o fitness de uma formiga.

        Parameters:
            ant: Formiga que fitness é retornado.

        Returns:
            float: O valor do fitness.
        """
        return ant.fitness_score

    def evolve_population(self):
        """
        Aplica evolução da população das formigas.
        """
        for ant in self.ants:
            ant.calculate_fitness()
        
        self.ants.sort(key=self.get_ant_fitness, reverse=True)
        self.print_statistics()
        elite = self.select_elite_ants()
        new_ants = elite.copy()
        
        while len(new_ants) < len(self.ants):
            parent1, parent2 = self.tournament()
            child = self.crossover_ants(parent1, parent2)
            child.mutate()
            new_ants.append(child)
        
        self.ants = new_ants
        
        # Reseta estatísticas para a nova geração
        for ant in self.ants:
            ant.fitness_food_collected = 0
            ant.fitness_steps_count = 0
            ant.exploration_route = []
            ant.has_food = False
            ant.exploring = True

    def tournament(self):
        """
        Escolhe dois pais para reprodução usando torneio.

        Returns:
            tuple: Dois pais selecionados.
        """
        parent1 = self.select_parent()
        parent2 = self.select_parent()
        return parent1, parent2

    def crossover_ants(self, parent1, parent2):
        """
        Realiza o cruzamento genético entre dois pais para gerar um filho. O filho herda 70% dos genes do melhor pai e 30% do outro pai.

        Parameters:
            parent1 (Ant): O primeiro pai.
            parent2 (Ant): O segundo pai.

        Returns:
            Ant: O filho gerado pelo cruzamento.
        """
        child = Ant(self.x, self.y)
            
        # Crossover com tendência para o melhor pai
        if parent1.fitness_score > parent2.fitness_score:
            better_parent, weaker_parent = parent1, parent2
        else:
            better_parent, weaker_parent = parent2, parent1
                
        child.ag_speed = better_parent.ag_speed * 0.7 + weaker_parent.ag_speed * 0.3
        child.ag_pheromone_detection_range = better_parent.ag_pheromone_detection_range * 0.7 + weaker_parent.ag_pheromone_detection_range * 0.3
        child.ag_pheromone_strength = better_parent.ag_pheromone_strength * 0.7 + weaker_parent.ag_pheromone_strength * 0.3
        return child

    def select_elite_ants(self):
        """
        Escolhea as formigas da elite usando o fitness.

        Returns:
            list: Lista de formigas da elite.
        """
        elite_size = max(2, int(len(self.ants) * GlobalVar.AG_ELITE_PERCENTAGE))
        elite = self.ants[0:elite_size]
        return elite

    def select_parent(self):
        """
        Escolhe um pai para reprodução usando torneio.

        Returns:
            Ant: A formiga selecionada como pai.
        """
        # se quantidade de formigas for menor que o tamanho do torneio, seleciona todas
        candidates = random.sample(self.ants, min(GlobalVar.AG_TOURNAMENT_SIZE, len(self.ants)))
        return max(candidates, key=self.get_ant_fitness)

    def calculate_average(self, ants, attribute):
        """
        Calcula a média de um atributo para a lista de formigas.

        Parameters:
            ants: Lista de formigas.
            attribute: Nome do atributo a ser calculado.

        Returns:
            float: Valor médio do atributo (0, se lista vazia).
        """
        if not ants:
            return 0
    
        total = 0
        for ant in ants:
            total += getattr(ant, attribute, 0)
        
        return total / len(ants)
    
    def print_statistics(self):
        """
        Imprime estatísticas da geração atual.
        """
        if self.ants:
            best_fitness = self.ants[0].fitness_score
        else:
            best_fitness = 0
            
        avg_speed = self.calculate_average(self.ants, "ag_speed")
        avg_sense = self.calculate_average(self.ants, "ag_pheromone_detection_range")
        avg_strength = self.calculate_average(self.ants, "ag_pheromone_strength")
        
        print(f"Geração {self.generation}: Melhor Fitness = {best_fitness:.2f}")
        print(f"Velocidade média: {avg_speed:.2f}, Detecção média: {avg_sense:.2f}, Feromônio médio: {avg_strength:.2f}")
