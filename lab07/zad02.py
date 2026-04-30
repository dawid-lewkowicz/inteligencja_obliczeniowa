import pygad
import math

def endurance(x, y, z, u, v, w):
    return math.exp(-2*(y-math.sin(x))**2) + math.sin(z*u) + math.cos(v*w)

def fitness_func(ga_instance, solution, solution_idx):
    return endurance(
        solution[0],
        solution[1],
        solution[2],
        solution[3],
        solution[4],
        solution[5]
    )

ga_instance = pygad.GA(
    num_generations=50,
    num_parents_mating=10,
    fitness_func=fitness_func,
    sol_per_pop=20,
    num_genes=6,
    gene_space={'low': 0.0, 'high': 0.999999},
    parent_selection_type="sss",
    keep_parents=2,
    crossover_type="single_point",
    mutation_type="random",
    mutation_percent_genes=17
)

ga_instance.run()

solution, solution_fitness, _ = ga_instance.best_solution()

print(f"Najlepsza wytrzymałość: {solution_fitness:.4f}")
print("Optymalne proporcje metali:")
print(f"x = {solution[0]:.4f}")
print(f"y = {solution[1]:.4f}")
print(f"z = {solution[2]:.4f}")
print(f"u = {solution[3]:.4f}")
print(f"v = {solution[4]:.4f}")
print(f"w = {solution[5]:.4f}")

ga_instance.plot_fitness()