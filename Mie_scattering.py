import numpy as np
import matplotlib.pyplot as plt
import PyMieScatt as ps

x = np.linspace(0.1, 10, 500)

m = 1.5 + 0.01j  # Пример: стекло в воздухе (n=1.5, k=0.01)

Q = []

for xi in x:
    q = ps.MieQ(m, xi, diameter=1)
    Q.append(q[1])  

Q = np.array(Q)

plt.figure(figsize=(8, 6))
plt.plot(x, Q, label=r'Q для $m=1.5+0.01j$')
plt.title('Зависимость эффективности рассеяния Ми от размера параметра')
plt.xlabel('Размерный параметр x (2πr/λ)')
plt.ylabel('Эффективность рассеяния Q')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()