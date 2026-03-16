import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

def create_payment_matrix(n, c1, c2, c3):
    """Создание матрицы платежей согласно условию [1, С. 187]"""
    C = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        for j in range(n + 1):
            if i >= j:
                C[i, j] = (i - j) * c2 + j * c1
            else:
                C[i, j] = i * c1 + (j - i) * c3
    return C

def browns_method(C, epsilon=0.01, max_iterations=10_000_000):
    n_rows, n_cols = C.shape
    row_cumulative = np.zeros(n_rows)
    col_cumulative = np.zeros(n_cols)
    row_counts = np.zeros(n_rows)
    col_counts = np.zeros(n_cols)
    
    # Начальный ход
    i_star, j_star = 0, 0
    row_counts[i_star] += 1
    col_counts[j_star] += 1
    row_cumulative += C[i_star, :]
    col_cumulative += C[:, j_star]
    
    for iteration in range(1, max_iterations + 1):
        # Выбор лучших ответов
        i_star = np.argmin(row_cumulative)  # ВЦ минимизирует потери
        j_star = np.argmax(col_cumulative)  # Диспетчер максимизирует
        
        row_counts[i_star] += 1
        col_counts[j_star] += 1
        row_cumulative += C[i_star, :]
        col_cumulative += C[:, j_star]
        
        # Оценка цены игры
        avg_row = row_cumulative / iteration
        avg_col = col_cumulative / iteration
        v_lower = np.min(avg_row)
        v_upper = np.max(avg_col)
        
        if abs(v_upper - v_lower) < epsilon:
            break
    
    p_optimal = row_counts / iteration
    pi_optimal = col_counts / iteration
    V = (v_lower + v_upper) / 2
    
    return p_optimal, pi_optimal, V, iteration

def solve_game(n, c1, c2, c3, epsilon=0.01):
    C = create_payment_matrix(n, c1, c2, c3)
    start_time = time.time()
    p_optimal, pi_optimal, V, iterations = browns_method(C, epsilon)
    end_time = time.time()
    return C, p_optimal, pi_optimal, V, iterations, end_time - start_time

def analyze_strategies(n, c1, c2, c3, p_optimal, pi_optimal, V):
    print("\nАнализ стратегий:")
    print("-" * 40)
    
    active_vc = [(i, p) for i, p in enumerate(p_optimal) if p > 0.01]
    active_disp = [(j, p) for j, p in enumerate(pi_optimal) if p > 0.01]
    
    print("Стратегия ВЦ:")
    for machines, prob in active_vc:
        print(f"  {machines} машин: {prob*100:.1f}%")
    
    print("\nСтратегия диспетчера:")
    for rank, prob in active_disp:
        print(f"  ранг {rank}: {prob*100:.1f}%")
    
    avg_machines = sum(i * p for i, p in enumerate(p_optimal))
    avg_rank = sum(j * p for j, p in enumerate(pi_optimal))
    
    print(f"\nСреднее число машин: {avg_machines:.2f}")
    print(f"Средний ранг задач: {avg_rank:.2f}")
    print(f"Цена игры: {V:.6f}")

def plot_time_complexity():
    n_values = [5, 10, 15, 20, 25, 30, 40, 50]
    times = []
    iterations_list = []
    c1, c2, c3 = 1.0, 4.0, 5.0
    epsilon = 0.01
    
    for n in n_values:
        C = create_payment_matrix(n, c1, c2, c3)
        start_time = time.time()
        _, _, _, iterations = browns_method(C, epsilon)
        end_time = time.time()
        times.append(end_time - start_time)
        iterations_list.append(iterations)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(n_values, times, 'o-', linewidth=2, markersize=8)
    axes[0].set_xlabel('Число машин (n)')
    axes[0].set_ylabel('Время (сек)')
    axes[0].set_title('Время работы алгоритма')
    axes[0].grid(True, alpha=0.3)
    
    axes[1].plot(n_values, iterations_list, 's-', color='red', linewidth=2, markersize=8)
    axes[1].set_xlabel('Число машин (n)')
    axes[1].set_ylabel('Итерации')
    axes[1].set_title('Число итераций')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('time_complexity.png', dpi=300)
    plt.show()

def main():
    n, c1, c2, c3, epsilon = 10, 1.0, 2.0, 3.0, 0.01
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if os.path.isfile(arg):
            try:
                with open(arg, 'r') as f:
                    content = f.read().strip()
                    if content:
                        params = content.split()
                        if len(params) >= 4:
                            n = int(params[0])
                            c1 = float(params[1])
                            c2 = float(params[2])
                            c3 = float(params[3])
                            if len(params) > 4:
                                epsilon = float(params[4])
            except Exception as e:
                print(f"Предупреждение: {e}, используются значения по умолчанию")
        else:
            try:
                if len(sys.argv) >= 5:
                    n = int(sys.argv[1])
                    c1 = float(sys.argv[2])
                    c2 = float(sys.argv[3])
                    c3 = float(sys.argv[4])
                    if len(sys.argv) > 5:
                        epsilon = float(sys.argv[5])
            except Exception as e:
                print(f"Предупреждение: {e}, используются значения по умолчанию")
    
    print(f"Параметры: n={n}, c1={c1}, c2={c2}, c3={c3}, eps={epsilon}\n")
    
    C, p_optimal, pi_optimal, V, iterations, comp_time = solve_game(n, c1, c2, c3, epsilon)
    
    print("Матрица платежей C:")
    np.set_printoptions(precision=2, suppress=True)
    print(C)
    
    print(f"\nИтераций: {iterations}")
    print(f"Цена игры V: {V:.6f}")
    print(f"Время: {comp_time:.4f} сек")
    
    print("\nСтратегии ВЦ:")
    print(" ".join([f"{x:.2f}" for x in p_optimal]))
    
    print("\nСтратегии диспетчера:")
    print(" ".join([f"{x:.2f}" for x in pi_optimal]))
    
    analyze_strategies(n, c1, c2, c3, p_optimal, pi_optimal, V)
    plot_time_complexity()
    
    print("\nРабота завершена.")

if __name__ == "__main__":
    main()