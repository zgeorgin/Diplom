import numpy as np
from sympy import legendre, jn
'''
Этот класс реализует метод FMM для решение CFIE
Обозначения:
- jn - Сферическая функция Ханкеля первого рода
- legendre - Многочлен Лежандра
'''
class FMMSolver:
    def __init__(self):
        self.wavelength = 6 * 10 ** (-6)
        self.k = 2 * np.pi / self.wavelength
    def alpha(self, r : np.array, k_sph : np.array, L = 5) -> complex:
        result = 0j
        r_norm = np.linalg.norm(r)
        for l in range(L + 1):
            result += 1j ** l * (2 * l + 1) * jn(l, self.k * r_norm) * legendre(np.dot(r, k_sph))
        return result