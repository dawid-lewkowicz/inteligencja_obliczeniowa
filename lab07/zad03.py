import pygad
import numpy as np
import time

maze = np.array([
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

start_pos = (1, 1)
exit_pos = (10, 10)

def fitness_func(ga_instance, solution, solution_idx):
    x, y = start_pos
    visited = set()
    visited.add((x, y))
    wall_bumps = 0
    steps_taken = 0
    
    for move in solution:
        steps_taken += 1
        next_x, next_y = x, y
        if move == 0:   next_x -= 1 #góra
        elif move == 1: next_y += 1 #prawo
        elif move == 2: next_x += 1 #dół
        elif move == 3: next_y -= 1 #lewo
        
        if maze[next_x, next_y] == 0:
            x, y = next_x, next_y
            visited.add((x, y)) 
        else:
            wall_bumps += 1
            
        if (x, y) == exit_pos:
            return 1000 + (30 - steps_taken) 
            
    distance = abs(exit_pos[0] - x) + abs(exit_pos[1] - y)
    
    fitness = (len(visited) * 2.0) - wall_bumps + (100.0 / (distance + 1.0))
    
    return max(0.1, fitness)

successful_times = []
total_runs = 0
best_ga_instance = None

while len(successful_times) < 10 and total_runs < 100:
    total_runs += 1
    
    ga_instance = pygad.GA(
        num_generations=100,          
        num_parents_mating=15,
        fitness_func=fitness_func,
        sol_per_pop=50,               
        num_genes=30,                 
        gene_space=[0, 1, 2, 3],      
        parent_selection_type="tournament", 
        keep_parents=2,
        crossover_type="single_point",
        mutation_type="random",
        mutation_percent_genes=4,     
        stop_criteria=["reach_1000"]
    )
    
    start_time = time.time()
    ga_instance.run()
    end_time = time.time()
    
    solution, solution_fitness, _ = ga_instance.best_solution()
    
    if solution_fitness >= 1000:
        successful_times.append(end_time - start_time)
        best_ga_instance = ga_instance
        print(f"Próba {total_runs}: SUKCES (Czas: {end_time - start_time:.4f}s)")
    else:
        print(f"Próba {total_runs}: Porażka")

if len(successful_times) == 10:
    print(f"\nŚredni czas znalezienia drogi z 10 udanych prób: {np.mean(successful_times):.4f} sekundy")
    
    solution, _, _ = best_ga_instance.best_solution()
    
    directions = ["G", "P", "D", "L"]
    decoded_path = [directions[int(move)] for move in solution]
    
    print("\nNajlepsza sekwencja ruchów:")
    print(solution)
    print("\nTłumaczenie ruchów:")
    print(" -> ".join(decoded_path))
    
else:
    print(f"\nNie udało się")