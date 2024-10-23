from MLFMA import *

def main():
    # Параметры модели
    num_particles = 1000
    max_particles = 10
    bounds = np.array([0.0, 1.0, 0.0, 1.0])

    # Генерация случайных частиц
    particles = [Particle(position=np.random.rand(2), charge=np.random.randn()) for _ in range(num_particles)]
    
    compute_MLFMA(particles, max_particles, bounds)

    for i in range(10):
        print(f"Частица {i}: потенциал = {particles[i].potential}")

main()