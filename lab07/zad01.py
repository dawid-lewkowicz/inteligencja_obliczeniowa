import pygad
import numpy as np
import time

items = ["zegar", "obraz-pejzaż", "obraz-portret", "radio", "laptop", "lampka nocna", 
        "srebrne sztućce", "porcelana", "figura z brązu", "skórzana torebka", "odkurzacz"]
values = np.array([100, 300, 200, 40, 500, 70, 100, 250, 300, 280, 300])
weights = np.array([7, 7, 6, 2, 5, 6, 1, 3, 10, 3, 15])

weight_limit = 25
optimal_value = 1630 

def fitness_func(ga_instance, solution, solution_idx):
    total_weight = np.sum(solution * weights)
    total_value = np.sum(solution * values)
    
    if total_weight > weight_limit:
        return -100  
    return total_value

successful_times = []
total_runs = 0
success_in_first_10 = 0
best_ga_instance = None

while len(successful_times) < 10 and total_runs < 100:
    total_runs += 1
    
    ga_instance = pygad.GA(
        num_generations=25,
        num_parents_mating=5,
        fitness_func=fitness_func,
        sol_per_pop=10,
        num_genes=len(items),
        gene_space=[0, 1],
        parent_selection_type="sss",
        keep_parents=2,
        crossover_type="single_point", 
        mutation_type="random",
        mutation_percent_genes=10,
        stop_criteria=[f"reach_{optimal_value}"]
    )
    
    start = time.time()
    ga_instance.run()
    end = time.time()
    
    solution, solution_fitness, _ = ga_instance.best_solution()
    
    if solution_fitness == optimal_value:
        successful_times.append(end - start)
        best_ga_instance = ga_instance
        if total_runs <= 10:
            success_in_first_10 += 1
        print(f"Próba {total_runs}: SUKCES (Czas: {end - start:.4f}s)")
    else:
        print(f"Próba {total_runs}: PORAŻKA (Fitness: {solution_fitness})")

success_rate = (success_in_first_10 / 10) * 100
print(f"Skuteczność algorytmu przy 10 pierwszych odpaleniach: {success_rate}%")

if len(successful_times) == 10:
    print(f"\nŚredni czas z 10 udanych prób: {np.mean(successful_times):.4f}")
    
    solution, _, _ = best_ga_instance.best_solution() #chromosom, ocena fitness, index
    print("\nOstateczny zestaw przedmiotów do zabrania:")
    for idx, bit in enumerate(solution):
        if bit == 1:
            print(f"- {items[idx]} (Wartość: {values[idx]}, Waga: {weights[idx]})")
            
    best_ga_instance.plot_fitness()
else:
    print(f"\n Przekroczono limit, sprawdź parametry.")