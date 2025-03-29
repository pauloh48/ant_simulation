import math

class GlobalVar:
    """
    Configurações globais.
    """
    # Janela
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    WINDOW_BACKGROUND_COLOR = (81, 58, 42)  # Marrom

    # Colônia
    COLONY_COLOR = (53, 40, 30)  # Marrom escuro
    COLONY_RADIUS = 10

    # Formigas
    ANT_COLOR = (0, 0, 0)  # Preto
    ANT_WITH_FOOD_COLOR = (255, 0, 0)  # Vermelho
    ANT_SCOUT_COLOR = (0, 100, 0)  # Verde escuro
    ANT_SCOUT_WITH_FOOD_COLOR = (0, 255, 0)  # Verde
    ANT_POPULATION_SIZE = 200
    ANT_SCOUT_COLOR_POPULATION_SIZE = ANT_POPULATION_SIZE//4
    
    # Comida 
    FOOD_AVAILABLE = 40
    FOOD_STORAGE_CAPACITY = 15

    # Feromônio
    PHEROMONE_COLOR = (255, 255, 0)  # Amarelo
    PHEROMONE_DECAY_RATE = 0.2

    # Evolução
    AG_MUTATION_RATE = 0.3  # Probabilidade de mutação (Aumentado de 0.1 para 0.3)
    AG_MUTATION_FORCE = 2.5  # Intensidade da mutação (Novo parâmetro)
    AG_FOOD_COLLECT_TO_EVOLVE = 10  # Número de gerações para evolução (Reduzido de 5 para 3)
    AG_ELITE_PERCENTAGE = 0.2  # 20% das melhores formigas sobrevivem
    AG_TOURNAMENT_SIZE = 5  # Tamanho do torneio de seleção (Aumentado para 5)

    # Atributos iniciais e limites dasformigas
    ANT_INITIAL_SPEED = 3.0
    ANT_MAX_SPEED = 10.0
    ANT_INITIAL_PHEROMONE_SENSE = 50.0
    ANT_MAX_PHEROMONE_SENSE = 200.0
    ANT_INITIAL_PHEROMONE_STRENGTH = 1.0
    ANT_MAX_PHEROMONE_STRENGTH = 5.0

    FPS = 30  