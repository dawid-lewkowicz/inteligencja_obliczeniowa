import matplotlib.pyplot as plt
import random
import math
from aco import AntColony

plt.style.use("dark_background")

random.seed(301575) 
COORDS_RANDOM = tuple((random.randint(0, 100), random.randint(0, 100)) for _ in range(15))

COORDS_GRID = tuple((x*10, y*10) for x in range(5) for y in range(5))

def calculate_path_length(path):
    length = 0
    for i in range(len(path) - 1):
        dx = path[i][0] - path[i+1][0]
        dy = path[i][1] - path[i+1][1]
        length += math.sqrt(dx**2 + dy**2)
    return length

def run_and_plot(coords, title, **aco_params):
    plt.figure(figsize=(10, 6))
    for x, y in coords:
        plt.plot(x, y, "g.", markersize=15)
    plt.axis("off")
    
    colony = AntColony(coords, **aco_params)
    optimal_nodes = colony.get_path()
    
    for i in range(len(optimal_nodes) - 1):
        plt.plot(
            (optimal_nodes[i][0], optimal_nodes[i + 1][0]),
            (optimal_nodes[i][1], optimal_nodes[i + 1][1]),
            "c-"
        )
    
    length = calculate_path_length(optimal_nodes)
    plt.title(f"{title}\nDługość ścieżki: {length:.2f}")
    plt.show()
    return length

print("--- Testowanie 15 losowych punktów ---")
# 2C 
# 1: ziwekszenie alpha kosztem beta prowadzi do przedwczesnej zbieżności, mrówki wpadaja w min lokalne
# 2: Wysoki evaporation_rate powoduje że system zapomina wcześniejsze ścieżki zbyt szybko
# 3: Domyślne parametry są dobre ale zwiększyłem liczbę iteracji do 500, żeby wyniki były stabilne

run_and_plot(
    COORDS_RANDOM, 
    "Zad. 2b/2c: 15 Losowych Punktów",
    ant_count=300, alpha=0.5, beta=1.2, 
    pheromone_evaporation_rate=0.40, pheromone_constant=1000.0, iterations=500
)

print("\n--- Testowanie Grid 5x5 ---")
# 2D
# Ze względu na dużą liczbę bliskich sąsiadów, zwiększyłem beta, żeby szukanie najbliższego węzła miało wiekszy piorytet niż ślad feromonowy

run_and_plot(
    COORDS_GRID, 
    "Zad. 2d: Grid 5x5 (Zoptymalizowane parametry)",
    ant_count=500, alpha=1.0, beta=2.0, 
    pheromone_evaporation_rate=0.50, pheromone_constant=1000.0, iterations=600
)