import numpy as np
from scipy.special import hankel1

# Параметры задачи
wavelength = 1.0  # длина волны
k = 2 * np.pi / wavelength  # волновое число

# Дискретизация поверхности проводника
num_segments = 100
theta = np.linspace(0, 2 * np.pi, num_segments, endpoint=False)
surface_points = np.vstack((np.cos(theta), np.sin(theta))).T
delta = 2 * np.pi / num_segments

# Падающее поле
def incident_electric_field(point):
    return np.array([1.0, 0.0])  # Пример: постоянное поле

# Задаем ядро интегрального оператора
def kernel(r, r_prime):
    distance = np.linalg.norm(r - r_prime)
    return hankel1(0, k * distance)

# Решение функции плотности тока, используя FMM
def solve_current_density(surface_points, delta):
    num_points = surface_points.shape[0]
    Z = np.zeros((num_points, num_points), dtype=complex)
    V = np.zeros(num_points, dtype=complex)
    
    # Матрица импеданса
    for i in range(num_points):
        for j in range(num_points):
            if i != j:
                Z[i, j] = kernel(surface_points[i], surface_points[j]) * delta
        # Правая часть уравнения (вектор возбуждения)
        V[i] = np.dot(incident_electric_field(surface_points[i]), np.array([0, 1]))  # Примерная нормаль
    
    # Решаем систему для плотностей токов
    print(V)
    J = np.linalg.solve(Z, V)
    return J

# Решаем задачу и выводим плотности токов
current_densities = solve_current_density(surface_points, delta)

for i, J in enumerate(current_densities):
    print(f"Токовая плотность в сегменте {i}: {J.real:.4f} + {J.imag:.4f}j")