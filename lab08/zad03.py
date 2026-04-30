import numpy as np
import random
import matplotlib.pyplot as plt

plt.style.use("dark_background")

MAZE = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

START = (0, 0)
END = (4, 6)

def build_graph(maze):
    graph = {}
    rows, cols = maze.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # góra, dół, lewo, prawo
    
    for r in range(rows):
        for c in range(cols):
            if maze[r, c] == 1:
                continue
            
            neighbors = []
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and maze[nr, nc] == 0:
                    neighbors.append((nr, nc))
            graph[(r, c)] = neighbors
    return graph

def run_maze_aco(graph, start, end, ants=50, iterations=100, alpha=1.0, evaporation=0.1):
    pheromones = {node: {neighbor: 1.0 for neighbor in graph[node]} for node in graph}
    best_path = None
    best_length = float('inf')

    for _ in range(iterations):
        all_paths = []
        
        for _ in range(ants):
            path = [start]
            current = start
            visited = set([start])
            
            while current != end:
                neighbors = graph[current]
                unvisited_neighbors = [n for n in neighbors if n not in visited]
                
                if not unvisited_neighbors:
                    break
                
                probabilities = [pheromones[current][n] ** alpha for n in unvisited_neighbors]
                total_prob = sum(probabilities)
                probabilities = [p / total_prob for p in probabilities]
                
                next_node = random.choices(unvisited_neighbors, weights=probabilities)[0]
                
                path.append(next_node)
                visited.add(next_node)
                current = next_node
                
            if current == end:
                all_paths.append(path)
                if len(path) < best_length:
                    best_length = len(path)
                    best_path = path

        for node in pheromones:
            for neighbor in pheromones[node]:
                pheromones[node][neighbor] *= (1.0 - evaporation)

        for path in all_paths:
            deposit = 100.0 / len(path) 
            for i in range(len(path) - 1):
                pheromones[path[i]][path[i+1]] += deposit
                
    return best_path

graph = build_graph(MAZE)
optimal_path = run_maze_aco(graph, START, END)

if not optimal_path:
    print("Rój nie znalazł drogi. Sprawdź czy labirynt ma fizyczne wyjście.")
else:
    print(f"Znaleziono optymalną ścieżkę o długości {len(optimal_path)} kroków.")
    print(f"Ścieżka: {optimal_path}")

    plt.figure(figsize=(8, 5))
    plt.imshow(MAZE, cmap='gray')
    
    if optimal_path:
        y_coords, x_coords = zip(*optimal_path)
        plt.plot(x_coords, y_coords, color='cyan', linewidth=3, marker='o')
        
    plt.plot(START[1], START[0], 'go', markersize=12, label="Start")
    plt.plot(END[1], END[0], 'ro', markersize=12, label="Koniec")
    
    plt.title("Zad. 3: ACO Pathfinding w Labiryncie")
    plt.legend()
    plt.axis("off")
    plt.show()