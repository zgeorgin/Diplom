import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp

n = 256  # Размер исходного сигнала
k = 20   # Количество ненулевых элементов (разреженность)
m = 100  # Число измерений (m < n)

x_real = np.zeros(n)
indices = np.random.choice(range(n), k, replace=False)
x_real[indices] = np.random.randn(k)

A = np.random.randn(m, n)

y = A @ x_real

x = cp.Variable(n)
objective = cp.Minimize(cp.norm1(x))
constraints = [A @ x == y]
prob = cp.Problem(objective, constraints)
result = prob.solve()

x_rec = x.value

plt.figure(figsize=(12, 6))

plt.subplot(1, 3, 1)
plt.stem(x_real)
plt.title('Исходный сигнал')

plt.subplot(1, 3, 2)
plt.stem(x_rec)
plt.title('Восстановленный сигнал')

plt.subplot(1, 3, 3)
plt.stem(x_real - x_rec)
plt.title('Разница')

plt.tight_layout()
plt.show()