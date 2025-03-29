import math
import random
from global_var import GlobalVar

def euclidean_distance(point1, point2):
    """
    Calcula a distância euclidiana entre dois pontos (menor distância: reta).
    
    Parameters:
        point1: Coordenadas (x, y) do ponto 1.
        point2: Coordenadas (x, y) do  ponto 2.
    
    Returns:
        float: A distância entre os pontos point1 e point2.    
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

class Ant:
    """
    Classe da formiga. Ela possue atributos genéticos como velocidade, alcance de detecção de feromônios e força de 
    liberação de feromônios. Ela pode explorar o ambiente, coletar comida e retornar para a colônia, deixando feromônios 
    no caminho.

    Atributes:
        x, y: Coordenadas da formiga.
        has_food: Se a está ou não carregando comida.
        exploring: Se está explorando ou não o ambiente.
        food_return_route: Posições registradas durante o retorno para a colônia.
        ag_speed: Velocidade da formiga(Atributo genético).
        ag_pheromone_detection_range: Alcance de detecção de feromônios (Atributo genético).
        ag_pheromone_strength: Força dos feromônios liberados pela formiga (Atributo genético).
        fitness_food_collected: Quantidade de comida coletada.
        fitness_steps_count: Quantidade de passos dados.
        fitness_score: Pontuação da formiga.

    Methods:
        calculate_fitness(): Calcula o fitness da formiga usando quantidade de comida coletada e atributos genéticos.
        move(environment): Atualiza a posição da formiga.
        direction_exploration(environment): Escolhe a direção de movimento durante a exploração.
        check_for_food(environment): Verifica se a formiga encontrou comida.
        deposit_food(environment): Deposita comida na colônia e libera feromônios no caminho.
        get_color(): Retorna a cor da formiga com base no estado (com ou sem comida).
        get_display_position(): Retorna a posição da formiga para exibição na tela.
        mutate(): Aplica mutações aleatórias nos atributos da formiga.
    """
    def __init__(self, x, y):
        """
        Construtor da formiga.

        Parameters:
            x, y: Coordenadas da formiga
        """
        self.x = x
        self.y = y
        
        self.has_food = False
        self.exploring = True
        self.food_return_route = []
        
        self.ag_speed = GlobalVar.ANT_INITIAL_SPEED + random.uniform(-0.5, 0.5)
        self.ag_pheromone_detection_range = GlobalVar.ANT_INITIAL_PHEROMONE_SENSE + random.uniform(-10, 10)
        self.ag_pheromone_strength = GlobalVar.ANT_INITIAL_PHEROMONE_STRENGTH + random.uniform(-0.2, 0.2)
        
        self.fitness_food_collected = 0
        self.fitness_steps_count = 0
        self.fitness_score = 0.1
    
    @property
    def position(self):
        """
        Retorna a posição da formiga.
        """
        return (self.x, self.y)
    
    def calculate_fitness(self):
        """
        Calcula o fitness da formiga usando pesos e considerando:
            Eficiência (quantidade de comida coletada em relação ao número de passos) (60%).
            Velocidade (20%). 
            Alcance de detecção de feromônios (10%).
            Força dos feromônios liberados (10%).

        Returns:
            float: A pontuação de fitness calculada para a formiga.
        """
        # Se não coletou comida, fitness é baixo
        if self.fitness_food_collected == 0:
            self.fitness_score = 0.1
            return self.fitness_score
        
        # Recompensas por coleta, velocidade, sensibilidade e força de feromônio
        efficiency = self.fitness_food_collected / max(1, self.fitness_steps_count)
        speed_bonus = self.ag_speed / GlobalVar.ANT_INITIAL_SPEED
        sense_bonus = self.ag_pheromone_detection_range / GlobalVar.ANT_INITIAL_PHEROMONE_SENSE
        strength_bonus = self.ag_pheromone_strength / GlobalVar.ANT_INITIAL_PHEROMONE_STRENGTH
        
        self.fitness_score = efficiency * 0.6 + speed_bonus * 0.2 + sense_bonus * 0.1 + strength_bonus * 0.1
        return self.fitness_score
    
    def move(self, environment):
        """
        Move a formiga pelo ambiente. Pode explorar ou retornar à colônia. Se encontrar comida, para de explorar.

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).

        Returns:
            bool: Retorna True se a formiga depositou comida na colônia, caso contrário False.
        """
        self.fitness_steps_count += 1
        
        # Retorna para a colônia ou explora
        if self.has_food:
            dx = environment.colony.x - self.x
            dy = environment.colony.y - self.y
            self.food_return_route.append((self.x, self.y))
        else:
            dx, dy = self.direction_exploration(environment)
        
        # Normaliza e aplica o movimento
        norm = max(abs(dx), abs(dy), 1)
        self.x += self.ag_speed * dx / norm
        self.y += self.ag_speed * dy / norm
        
        # Mantém dentro dos limites da tela
        self.x = max(0, min(GlobalVar.WINDOW_WIDTH, self.x))
        self.y = max(0, min(GlobalVar.WINDOW_HEIGHT, self.y))
        
        if not self.has_food:
            self.check_for_food(environment)
        
        if self.has_food and euclidean_distance(self.position, environment.colony.position) < GlobalVar.COLONY_RADIUS:
            self.deposit_food(environment)
            return True
            
        return False
    
    def direction_exploration(self, environment):
        """
        Determina a direção de movimento (guiada por feromônio ou aleatório) durante a exploração.

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).

        Returns:
            tuple: Um vetor (dx, dy) que indica o deslocamento da formiga.
        """
        # Busca o feromônio mais próximo dentro do alcance de detecção
        nearest_pheromone = environment.find_nearest_pheromone(self.position, self.ag_pheromone_detection_range)
        
        if nearest_pheromone:
            # Segue o feromônio
            return (
                nearest_pheromone.position[0] - self.x,
                nearest_pheromone.position[1] - self.y
            )
        else:
            # Movimento aleatório com pequena tendência de exploração
            return (random.uniform(-10, 10), random.uniform(-10, 10))
    
    def check_for_food(self, environment):
        """
        Verifica se a formiga encontrou comida no ambiente (se sim, para de explorar).

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).
        """
        nearest_food = environment.find_nearest_food(self.position)
        if nearest_food and euclidean_distance(self.position, nearest_food.position) < 15:
            self.has_food = True
            self.exploring = False
            environment.take_food(nearest_food)
            
            # Atualiza estatísticas
            self.fitness_food_collected += 1
    
    def deposit_food(self, environment):
        """
        Deposita comida na colônia e libera feromônios no caminho percorrido.

        Parameters:
            environment: Representa o ambiente da simulação (contêm informações sobre a colônia, fontes de comida e feromônios).
        """
        self.has_food = False
        
        # Deposita feromônios no caminho com a intensidade da formiga
        for pos in self.food_return_route:
            if euclidean_distance(pos, environment.colony.position) > GlobalVar.COLONY_RADIUS * 2:
                environment.add_pheromone(pos, self.ag_pheromone_strength)
        
        self.food_return_route = []

    def get_color(self):
        """
        Retorna a cor da formiga com base no seu estado (com ou sem comida).
        """
        return GlobalVar.ANT_WITH_FOOD_COLOR if self.has_food else GlobalVar.ANT_COLOR
    
    def get_display_position(self):
        """
        Retorna a posição da formiga como inteiros (para renderização).
        """
        return (int(self.x), int(self.y))
    
    def mutate(self):
        """
        Aplica mutações aleatórias em algum dos atributos genéticos da formiga com 
        uma probabilidade definida por AG_MUTATION_RATE.
        """
        if random.random() < GlobalVar.AG_MUTATION_RATE:
            attribute = random.choice(["speed", "sense", "strength"])
            
            if attribute == "speed":
                # Mutação mais agressiva
                self.ag_speed += random.uniform(-1.0, 1.0) * GlobalVar.AG_MUTATION_FORCE
                self.ag_speed = max(1.0, min(GlobalVar.ANT_MAX_SPEED, self.ag_speed))
                
            elif attribute == "sense":
                self.ag_pheromone_detection_range += random.uniform(-20, 20) * GlobalVar.AG_MUTATION_FORCE
                self.ag_pheromone_detection_range = max(10.0, min(GlobalVar.ANT_MAX_PHEROMONE_SENSE, self.ag_pheromone_detection_range))
                
            elif attribute == "strength":
                self.ag_pheromone_strength += random.uniform(-0.5, 0.5) * GlobalVar.AG_MUTATION_FORCE
                self.ag_pheromone_strength = max(0.5, min(GlobalVar.ANT_MAX_PHEROMONE_STRENGTH, self.ag_pheromone_strength))