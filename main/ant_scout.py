import random
from global_var import GlobalVar
from ant import Ant

class Ant_Scout(Ant):
    """
    Formiga exploradora que tem características mais variáveis.
    Elas podem detectar mais feromônios, liberar mais feromônios ou se mover mais rápido.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        
        # Apresenta mais varições que formiga normal nos atributos genéticos
        self.ag_speed = GlobalVar.ANT_INITIAL_SPEED + random.uniform(-1.5, 1.5)
        self.ag_pheromone_detection_range = GlobalVar.ANT_INITIAL_PHEROMONE_SENSE + random.uniform(-20, 20)
        self.ag_pheromone_strength = GlobalVar.ANT_INITIAL_PHEROMONE_STRENGTH + random.uniform(-0.8, 0.8)
        
        self.fitness_food_collected = 0
        self.fitness_steps_count = 0
        self.fitness_score = 0.1
    
    def get_color(self):
        """
        Retorna a cor da formiga com base no seu estado (com ou sem comida).
        """
        return GlobalVar.ANT_SCOUT_WITH_FOOD_COLOR if self.has_food else GlobalVar.ANT_SCOUT_COLOR
