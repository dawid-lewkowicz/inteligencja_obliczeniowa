import numpy as np
import math
import pyswarms as ps
from pyswarms.utils.plotters import plot_cost_history
import matplotlib.pyplot as plt

def endurance(x, y, z, u, v, w):
    return math.exp(-2*(y-math.sin(x))**2) + math.sin(z*u) + math.cos(v*w)

def f(particles):
    n_particles = particles.shape[0]
    costs = np.zeros(n_particles)
    
    for i in range(n_particles):
        costs[i] = -endurance(*particles[i])
        
    return costs

options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}

min_bound = np.zeros(6)
max_bound = np.ones(6)
bounds = (min_bound, max_bound)

optimizer = ps.single.GlobalBestPSO(
    n_particles=50, 
    dimensions=6, 
    options=options, 
    bounds=bounds
)

cost, pos = optimizer.optimize(f, iters=1000)

print("\n--- WYNIKI ---")
print(f"Najlepszy koszt (zanegowany): {cost}")
print(f"Rzeczywista max wytrzymałość: {-cost}")
print(f"Optymalne parametry stopu: {pos}")

plot_cost_history(optimizer.cost_history)
plt.show()