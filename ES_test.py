from MLMFA import *
import numpy as np
def main():
    # Создаём заряженную пластину 1х1
    particles = list(np.array([[Particle(position=(j, i), charge=1) for j in np.linspace(1, 2, 10)] for i in np.linspace(1, 2, 10)]).flatten())
    
    num_particles = 1000
    max_particles = 10
    bounds = np.array([0.0, 3.0, 0.0, 3.0])
    
    shoot_particles = [[Particle(position=(j, i), charge=-1) for j in np.linspace(0, 3, 100)] for i in np.linspace(0, 3, 100)]
    
    for particle_line in shoot_particles:
        for p in particle_line:
            particles.append(p)
            compute_MLMFA(particles, max_particles, num_particles, bounds)
            print(p.potential)
            particles.pop(-1)
            
main()
    