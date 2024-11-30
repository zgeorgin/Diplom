from MLFMA import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
c = 3 * 10**8

def X(theta, f, particles : list[Particle], r0):
    integral = 0
    for p in particles:
        u = p.position[0]
        v = p.position[1]
        integral += p.potential * np.exp(-1j * 4 * np.pi * f / c * (r0 + v * np.cos(theta) - u * np.sin(theta)))
    return integral
    
def main():
    num_particles = 25000
    max_particles = 10
    bounds = np.array([0.0, 3.0, 0.0, 3.0])

    r0 = 100
    f = 10 ** 8

    particles = list(np.array([[Particle(position=(j, i), charge=0) for j in np.x(1, 2, int(num_particles ** 0.5))] for i in np.linspace(1, 2, int(num_particles ** 0.5))]).flatten())
    particles.append(Particle(position = (1.5, 1.5), charge = 1))
    compute_MLFMA(particles, max_particles, bounds)
    x = [p.position[0] for p in particles]
    y = [p.position[1] for p in particles]
    xi, yi = np.meshgrid(np.linspace(min(x), max(x), 1000), np.linspace(min(y), max(y), 1000))
    zi = griddata((x, y), [p.potential for p in particles], (xi, yi), method = 'cubic')
    plt.contourf(xi, yi, zi, cmap='hot')
    plt.colorbar(label='Потенциал')
    plt.show()
    for p in particles:
        print(p.potential)
    X_array = []
    thetas = np.arange(0, 180, 0.1)
    for theta in thetas:
        X_array.append(X(theta * np.pi / 180, f, particles, r0))
        
    plt.semilogy(thetas, X_array)
    plt.show()
    
main()