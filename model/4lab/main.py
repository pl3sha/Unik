import random
import matplotlib.pyplot as plt

M = 5
N = 10
NUM_RUNS = 1000

def sampling_with_replacement(m, n):
    matrix = [[0] * n for _ in range(m)]
    positions = []
    for i in range(m):
        pos = random.randint(0, n - 1)
        matrix[i][pos] = 1
        positions.append(pos + 1)
    return matrix, positions

def sampling_without_replacement(m, n):
    if m > n:
        m = n
    matrix = [[0] * n for _ in range(m)]
    available = list(range(n))
    positions = []
    for i in range(m):
        pos = random.choice(available)
        matrix[i][pos] = 1
        available.remove(pos)
        positions.append(pos + 1)
    return matrix, positions

def arrangement(m, n):
    if m > n:
        m = n
    matrix = [[0] * n for _ in range(m)]
    available = list(range(n))
    random.shuffle(available)
    positions = []
    for i in range(m):
        pos = available[i]
        matrix[i][pos] = 1
        positions.append(pos + 1)
    return matrix, positions

def run_experiments(m, n, num_runs, sampling_func, name):
    position_counts = {i: 0 for i in range(n)}
    accumulated = [[0] * n for _ in range(m)]
    
    print(f"\n{name}")
    
    if name == 'With_replacement':
        print("\nSource array:")
        source_array = list(range(1, n + 1))
        print(source_array)
        print(f"Unique values: {len(set(source_array))}\n")
    
    for run in range(num_runs):
        matrix, positions = sampling_func(m, n)
        
        for pos in positions:
            position_counts[pos - 1] += 1
        
        for i in range(m):
            for j in range(n):
                accumulated[i][j] += matrix[i][j]
        
        if run < 3:
            print(f"Run {run + 1}:")
            print(f"Sample (positions): {positions}")
            print(f"Unique positions: {len(set(positions))} of {m}")
            print(f"Sample (values): {positions}")
            print("Matrix:")
            for row in matrix:
                print(row)
            print()
    
    print("Accumulated matrix (1000 runs):")
    for row in accumulated:
        print(row)
    print()
    
    return position_counts

def plot_histogram(position_counts, m, n, num_runs, title, filename, color):
    positions = list(range(1, n + 1))
    frequencies = [position_counts[i] for i in range(n)]
    percentages = [f / (m * num_runs) * 100 for f in frequencies]
    theoretical_pct = 100 / n
    
    plt.figure(figsize=(8, 4))
    plt.bar(positions, percentages, color=color, alpha=0.7, label='Experimental')
    plt.axhline(y=theoretical_pct, color='red', linestyle='--', linewidth=1.5, 
                label=f'Theoretical ({theoretical_pct:.1f}%)')
    plt.xlabel('Position')
    plt.ylabel('Relative frequency, %')
    plt.title(title)
    plt.xticks(positions)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{filename}")

def main():
    print(f"m={M}, n={N}, runs={NUM_RUNS}")
    
    results = {}
    results['With_replacement'] = run_experiments(M, N, NUM_RUNS, sampling_with_replacement, 'With_replacement')
    results['Without_replacement'] = run_experiments(M, N, NUM_RUNS, sampling_without_replacement, 'Without_replacement')
    results['Arrangement'] = run_experiments(N, N, NUM_RUNS, arrangement, 'Arrangement')
    
    print("\nStatistics:")

    for name, counts in results.items():

        if name == "Arrangement":
            m_used = N
        else:
            m_used = M

        total = m_used * NUM_RUNS
        expected_freq = total / N
        expected_pct = 100 / N

        print(f"\n{name}:")
        for pos in range(N):
            freq = counts[pos]
            pct = freq / total * 100
            print(f"Pos {pos+1}: {freq} ({pct:.2f}%) | Expected: {expected_freq:.1f} ({expected_pct:.1f}%)")
    
    print("\nSummary table:")
    print("Pos\tWith rep\tWithout rep\tArrangement")
    for pos in range(N):
        print(f"{pos+1}", end="\t")
        for name in results:
            cnt = results[name][pos]
            if name == "Arrangement":
                total = N * NUM_RUNS
            else:
                total = M * NUM_RUNS

            pct = cnt / total * 100
            print(f"{cnt}({pct:.1f}%)", end="\t")
        print()
    
    print("\nGenerating plots...")
    plot_histogram(results['With_replacement'], M, N, NUM_RUNS, 'With_replacement', 'hist_with.png', 'skyblue')
    plot_histogram(results['Without_replacement'], M, N, NUM_RUNS, 'Without_replacement', 'hist_without.png', 'lightgreen')
    plot_histogram(results['Arrangement'], N, N, NUM_RUNS, 'Arrangement', 'hist_arr.png', 'plum')

if __name__ == "__main__":
    random.seed(42)
    main()
