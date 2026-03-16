import matplotlib.pyplot as plt
import numpy as np
import csv
import random
import time
import sys
import os

from main import (
    Task, Level, counting_sort_tasks, 
    nfdh, ffdh, calculate_metrics, 
    generate_random_tasks, SegmentTree
)

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

COLORS = {'NFDH': '#2E86AB', 'FFDH': '#A23B72'}
MARKERS = {'NFDH': 'o', 'FFDH': 's'}

def run_accuracy_experiment(m_values, n, trials=10):
    results = {'m': [], 'nfdh_mean': [], 'nfdh_std': [], 'ffdh_mean': [], 'ffdh_std': []}
    
    for m in m_values:
        eps_nfdh = []
        eps_ffdh = []
        
        for _ in range(trials):
            tasks = generate_random_tasks(m, n)
            
            # NFDH
            tasks_copy1 = [Task(t.id, t.t, t.r) for t in tasks]
            sorted_tasks1 = counting_sort_tasks(tasks_copy1, max_t=100)
            levels1 = nfdh(sorted_tasks1, n)
            _, eps1 = calculate_metrics(levels1, n, tasks_copy1)
            eps_nfdh.append(eps1)
            
            # FFDH
            tasks_copy2 = [Task(t.id, t.t, t.r) for t in tasks]
            sorted_tasks2 = counting_sort_tasks(tasks_copy2, max_t=100)
            levels2 = ffdh(sorted_tasks2, n)
            _, eps2 = calculate_metrics(levels2, n, tasks_copy2)
            eps_ffdh.append(eps2)
        
        results['m'].append(m)
        results['nfdh_mean'].append(np.mean(eps_nfdh))
        results['nfdh_std'].append(np.std(eps_nfdh))
        results['ffdh_mean'].append(np.mean(eps_ffdh))
        results['ffdh_std'].append(np.std(eps_ffdh))
        
        print(f"✓ m={m}: ε(NFDH)={np.mean(eps_nfdh):.4f}±{np.std(eps_nfdh):.4f}, "
              f"ε(FFDH)={np.mean(eps_ffdh):.4f}±{np.std(eps_ffdh):.4f}")
    
    return results

def run_speed_experiment(m_values, n_values, trials=5):
    results = {'m': [], 'n': [], 'nfdh_time': [], 'ffdh_time': []}
    
    for n in n_values:
        for m in m_values:
            times_nfdh = []
            times_ffdh = []
            
            for _ in range(trials):
                tasks = generate_random_tasks(m, n)
                sorted_tasks = counting_sort_tasks(tasks, max_t=100)
                
                t0 = time.time()
                levels = nfdh(sorted_tasks, n)
                t1 = time.time()
                times_nfdh.append(t1 - t0)
                
                tasks2 = generate_random_tasks(m, n)
                sorted_tasks2 = counting_sort_tasks(tasks2, max_t=100)
                t0 = time.time()
                levels = ffdh(sorted_tasks2, n)
                t1 = time.time()
                times_ffdh.append(t1 - t0)
            
            results['m'].append(m)
            results['n'].append(n)
            results['nfdh_time'].append(np.mean(times_nfdh))
            results['ffdh_time'].append(np.mean(times_ffdh))
            
            print(f"✓ m={m}, n={n}: T(NFDH)={np.mean(times_nfdh)*1000:.2f}мс, "
                  f"T(FFDH)={np.mean(times_ffdh)*1000:.2f}мс")
    
    return results

def plot_accuracy(results, output_file='accuracy_plot.png'):
    plt.figure(figsize=(10, 6))
    
    plt.errorbar(results['m'], results['nfdh_mean'], 
                yerr=results['nfdh_std'], 
                label='NFDH', 
                color=COLORS['NFDH'],
                marker=MARKERS['NFDH'],
                capsize=4,
                linewidth=2)
    
    plt.errorbar(results['m'], results['ffdh_mean'], 
                yerr=results['ffdh_std'], 
                label='FFDH', 
                color=COLORS['FFDH'],
                marker=MARKERS['FFDH'],
                capsize=4,
                linewidth=2)
    
    plt.xlabel('Количество задач (m)', fontsize=11)
    plt.ylabel('Отклонение ε (относительная погрешность)', fontsize=11)
    plt.title('Сравнение точности алгоритмов упаковки (n=1024)', fontsize=13, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xticks(results['m'])
    
    plt.annotate('Меньше ε → точнее расписание', 
                xy=(0.02, 0.98), xycoords='axes fraction',
                fontsize=9, ha='left', va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ График точности сохранён: {output_file}")
    plt.close()

def plot_speed(results, output_file='speed_plot.png'):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    for idx, n_val in enumerate([1024, 4096]):
        ax = axes[idx]
        
        mask = [n == n_val for n in results['n']]
        m_filtered = [results['m'][i] for i in range(len(mask)) if mask[i]]
        nfdh_filtered = [results['nfdh_time'][i]*1000 for i in range(len(mask)) if mask[i]]
        ffdh_filtered = [results['ffdh_time'][i]*1000 for i in range(len(mask)) if mask[i]]
        
        ax.plot(m_filtered, nfdh_filtered, 
               label='NFDH', 
               color=COLORS['NFDH'],
               marker=MARKERS['NFDH'],
               linewidth=2, markersize=6)
        
        ax.plot(m_filtered, ffdh_filtered, 
               label='FFDH', 
               color=COLORS['FFDH'],
               marker=MARKERS['FFDH'],
               linewidth=2, markersize=6)
        
        ax.set_xlabel('Количество задач (m)', fontsize=10)
        ax.set_ylabel('Время выполнения (мс)', fontsize=10)
        ax.set_title(f'Скорость алгоритмов (n={n_val})', fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(m_filtered)
    
    plt.suptitle('Зависимость времени выполнения от количества задач', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ График скорости сохранён: {output_file}")
    plt.close()

def plot_utilization(m_values, n, trials=5, output_file='utilization_plot.png'):
    plt.figure(figsize=(10, 6))
    
    util_nfdh = []
    util_ffdh = []
    
    for m in m_values:
        u_nfdh = []
        u_ffdh = []
        
        for _ in range(trials):
            tasks = generate_random_tasks(m, n)
            
            tasks1 = [Task(t.id, t.t, t.r) for t in tasks]
            sorted1 = counting_sort_tasks(tasks1, max_t=100)
            levels1 = nfdh(sorted1, n)
            t_s1 = sum(l.height for l in levels1)
            area = sum(t.t * t.r for t in tasks1)
            u_nfdh.append(area / (t_s1 * n) if t_s1 * n > 0 else 0)
            
            tasks2 = [Task(t.id, t.t, t.r) for t in tasks]
            sorted2 = counting_sort_tasks(tasks2, max_t=100)
            levels2 = ffdh(sorted2, n)
            t_s2 = sum(l.height for l in levels2)
            area = sum(t.t * t.r for t in tasks2)
            u_ffdh.append(area / (t_s2 * n) if t_s2 * n > 0 else 0)
        
        util_nfdh.append(np.mean(u_nfdh))
        util_ffdh.append(np.mean(u_ffdh))
        
        print(f"✓ m={m}: Util(NFDH)={np.mean(u_nfdh)*100:.2f}%, Util(FFDH)={np.mean(u_ffdh)*100:.2f}%")
    
    x = np.arange(len(m_values))
    width = 0.35
    
    bars1 = plt.bar(x - width/2, [u*100 for u in util_nfdh], width, 
                   label='NFDH', color=COLORS['NFDH'], alpha=0.8)
    bars2 = plt.bar(x + width/2, [u*100 for u in util_ffdh], width, 
                   label='FFDH', color=COLORS['FFDH'], alpha=0.8)
    
    plt.xlabel('Количество задач (m)', fontsize=11)
    plt.ylabel('Коэффициент использования ресурсов (%)', fontsize=11)
    plt.title('Эффективность использования ЭМ (n=1024)', fontsize=13, fontweight='bold')
    plt.xticks(x, m_values)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3, axis='y')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
    
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ График заполнения сохранён: {output_file}")
    plt.close()

def main():
    print("Запуск экспериментов для построения графиков...\n")
    
    m_values = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    n_accuracy = 1024
    n_speed = [1024, 4096]
    trials = 10
    
    print("\nСбор данных для графика ТОЧНОСТИ (ε)...")
    acc_results = run_accuracy_experiment(m_values, n_accuracy, trials)
    plot_accuracy(acc_results)
    
    print("\nСбор данных для графика СКОРОСТИ...")
    speed_results = run_speed_experiment(m_values[:6], n_speed, trials=5)
    plot_speed(speed_results)
    
    print("\nбор данных для графика ЗАПОЛНЕНИЯ (utilization)...")
    plot_utilization(m_values, n_accuracy, trials=5)
    
    print("\nСохранение данных в CSV...")
    
    with open('accuracy_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['m', 'NFDH_mean', 'NFDH_std', 'FFDH_mean', 'FFDH_std'])
        for i in range(len(acc_results['m'])):
            writer.writerow([
                acc_results['m'][i],
                f"{acc_results['nfdh_mean'][i]:.6f}",
                f"{acc_results['nfdh_std'][i]:.6f}",
                f"{acc_results['ffdh_mean'][i]:.6f}",
                f"{acc_results['ffdh_std'][i]:.6f}"
            ])
    
    with open('speed_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['m', 'n', 'NFDH_time_ms', 'FFDH_time_ms'])
        for i in range(len(speed_results['m'])):
            writer.writerow([
                speed_results['m'][i],
                speed_results['n'][i],
                f"{speed_results['nfdh_time'][i]*1000:.4f}",
                f"{speed_results['ffdh_time'][i]*1000:.4f}"
            ])
    
    print("\nВсе графики и данные сохранены!")
    print("Файлы для отчета:")
    print("   • accuracy_plot.png")
    print("   • speed_plot.png")
    print("   • utilization_plot.png")
    print("   • accuracy_data.csv")
    print("   • speed_data.csv")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        print("Быстрый режим: уменьшено количество итераций")
        m_values = [500, 1000, 2000, 3000]
        trials = 3
        main()
    else:
        main()