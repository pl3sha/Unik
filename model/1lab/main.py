import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

PI = np.pi
K = 0.611603
Y_CRIT = 0.433013
C_CONST = 1.044616
BREAK_POINT = PI/6

def f_theory(x):
    res = np.zeros_like(x)
    m1 = (x > -PI/6) & (x <= PI/6)
    m2 = (x > PI/6) & (x < PI)
    res[m1] = 0.5 * np.cos(x[m1] + PI/6)
    res[m2] = K * np.exp(-(x[m2] - PI/6))
    return res

def F_theory(x):
    res = np.zeros_like(x)
    m1 = (x > -PI/6) & (x <= PI/6)
    m2 = (x > PI/6) & (x < PI)
    res[m1] = 0.5 * np.sin(x[m1] + PI/6)
    res[m2] = Y_CRIT + K * (1 - np.exp(-(x[m2] - PI/6)))
    res[x >= PI] = 1.0
    return res

def F_inverse(y):
    res = np.zeros_like(y)
    m1 = (y >= 0) & (y <= Y_CRIT)
    m2 = (y > Y_CRIT) & (y < 1)
    res[m1] = np.arcsin(2 * y[m1]) - PI/6
    res[m2] = PI/6 - np.log((C_CONST - y[m2]) / K)
    res[y >= 1] = PI
    return res

np.random.seed(42)
N = 1000000
sample = F_inverse(np.random.uniform(0, 1, N))

x_plot = np.linspace(-PI/6 - 0.3, PI + 0.3, 1000)

fig1, axes = plt.subplots(3, 1, figsize=(12, 14))

axes[0].plot(x_plot, f_theory(x_plot), 'b-', lw=3, label='Теоретическая $f(x)$')
axes[0].axvline(-PI/6, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
axes[0].axvline(BREAK_POINT, color='red', linestyle='--', alpha=0.7, linewidth=2, label=f'Разрыв при $x = \\pi/6$')
axes[0].axvline(PI, color='green', linestyle='--', alpha=0.5, linewidth=1.5)
axes[0].set_title('Теоретическая плотность вероятности $f(x)$', fontsize=14, fontweight='bold')
axes[0].set_xlabel('$x$', fontsize=12)
axes[0].set_ylabel('$f(x)$', fontsize=12)
axes[0].grid(alpha=0.3, linestyle=':')
axes[0].legend(fontsize=11)
axes[0].set_xlim(-PI/3, 1.2*PI)
axes[0].set_ylim(0, max(f_theory(x_plot)) * 1.1)

axes[1].plot(x_plot, F_theory(x_plot), 'r-', lw=3, label='Теоретическая $F(x)$')
axes[1].axhline(Y_CRIT, color='orange', linestyle='--', alpha=0.6, linewidth=1.5, label=f'$Y_{{crit}} = \\sqrt{{3}}/4 \\approx {Y_CRIT:.3f}$')
axes[1].axvline(BREAK_POINT, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
axes[1].axvline(PI, color='green', linestyle='--', alpha=0.5, linewidth=1.5)
axes[1].set_title('Функция распределения $F(x)$', fontsize=14, fontweight='bold')
axes[1].set_xlabel('$x$', fontsize=12)
axes[1].set_ylabel('$F(x)$', fontsize=12)
axes[1].grid(alpha=0.3, linestyle=':')
axes[1].legend(fontsize=11)
axes[1].set_xlim(-PI/3, 1.2*PI)
axes[1].set_ylim(-0.05, 1.05)

bins_left = np.linspace(-PI/6, BREAK_POINT, 25)
bins_right = np.linspace(BREAK_POINT, PI, 40)
bins = np.concatenate([bins_left[:-1], bins_right])

axes[2].hist(sample, bins=bins, density=True, alpha=0.65, color='skyblue', edgecolor='black', linewidth=0.8, label='Гистограмма выборки')
axes[2].plot(x_plot, f_theory(x_plot), 'b-', lw=3, label='Теоретическая $f(x)$')
axes[2].axvline(BREAK_POINT, color='red', linestyle='--', alpha=0.7, linewidth=2, label=f'Разрыв при $x = \\pi/6$')
axes[2].axvline(PI, color='green', linestyle='--', alpha=0.5, linewidth=1.5)
axes[2].set_title('Гистограмма выборки и теоретическая плотность вероятности', fontsize=14, fontweight='bold')
axes[2].set_xlabel('$x$', fontsize=12)
axes[2].set_ylabel('Плотность', fontsize=12)
axes[2].grid(alpha=0.3, linestyle=':')
axes[2].legend(fontsize=11)
axes[2].set_xlim(-PI/3, 1.2*PI)
axes[2].set_ylim(0, max(f_theory(x_plot)) * 1.1)

plt.tight_layout()
plt.savefig('probability_analysis2.png', dpi=300, bbox_inches='tight')
plt.show()

fig2, ax = plt.subplots(figsize=(14, 7))

x_dense = np.linspace(-PI/6, PI, 1000)
ax.plot(x_dense, f_theory(x_dense), 'b-', linewidth=3.5, label='Теоретическая плотность $f(x)$', zorder=10)

subset_size = 5000
subset_indices = np.random.choice(len(sample), subset_size, replace=False)
subset_x = sample[subset_indices]
subset_y = np.random.uniform(0, 1, subset_size) * f_theory(subset_x)

ax.scatter(subset_x, subset_y, c='red', alpha=0.3, s=15, edgecolors='none', label='Сгенерированные точки', zorder=5)

x_margin = (PI - (-PI/6)) * 0.08
ax.set_xlim(-PI/6 - x_margin, PI + x_margin)
ax.set_ylim(0, max(f_theory(x_dense)) * 1.2)

ax.axvline(-PI/6, color='gray', linestyle='--', alpha=0.5, linewidth=1.5, label='Границы распределения')
ax.axvline(PI, color='gray', linestyle='--', alpha=0.5, linewidth=1.5)
ax.axvline(BREAK_POINT, color='red', linestyle='--', alpha=0.6, linewidth=2)

ax.set_title('Теоретическая плотность и сгенерированные точки', fontsize=14, fontweight='bold')
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('Плотность', fontsize=12)
ax.grid(alpha=0.3, linestyle=':')
ax.legend(fontsize=11, loc='upper right')

plt.tight_layout()
plt.savefig('generator_verification.png', dpi=300, bbox_inches='tight')
plt.show()

integral1, _ = quad(lambda x: 0.5 * np.cos(x + PI/6), -PI/6, PI/6)
integral2, _ = quad(lambda x: K * np.exp(-(x - PI/6)), PI/6, PI)
total = integral1 + integral2

print(f"Выборка: N={N}, Диапазон=[{sample.min():.4f}, {sample.max():.4f}]")
print(f"Нормировка: {total:.8f} (отклонение: {abs(total-1):.2e})")