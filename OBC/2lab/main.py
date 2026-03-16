import sys
import time
import random
import math
import csv

class Task:
    def __init__(self, id, t, r):
        self.id = id
        self.t = t  
        self.r = r  
        self.tau = 0 
        self.machines = [] 

class Level:
    def __init__(self, height, capacity, start_machine_idx):
        self.height = height
        self.capacity = capacity
        self.used = 0
        self.start_machine_idx = start_machine_idx
        self.tasks = []

    def free_space(self):
        return self.capacity - self.used

def counting_sort_tasks(tasks, max_t=10000):
    if not tasks:
        return []
    
    limit = max(max_t, max(t.t for t in tasks))
    count = [0] * (limit + 1)
    
    for task in tasks:
        if task.t <= limit:
            count[task.t] += 1
    
    for i in range(1, len(count)):
        count[i] += count[i-1]
    
    output = [None] * len(tasks)
    for i in range(len(tasks) - 1, -1, -1):
        t_val = tasks[i].t
        if t_val <= limit:
            count[t_val] -= 1
            output[count[t_val]] = tasks[i]
    
    return output[::-1]

class SegmentTree:
    def __init__(self, max_levels):
        self.n = 1
        while self.n < max_levels:
            self.n *= 2
        self.tree = [0] * (2 * self.n)
    
    def update(self, idx, value):
        pos = idx + self.n
        self.tree[pos] = value
        while pos > 1:
            self.tree[pos >> 1] = max(self.tree[pos], self.tree[pos ^ 1])
            pos >>= 1
            
    def find_first_fit(self, width):
        if self.tree[1] < width:
            return -1
        
        pos = 1
        while pos < self.n:
            if self.tree[pos * 2] >= width:
                pos = pos * 2
            else:
                pos = pos * 2 + 1
        
        if pos >= self.n and self.tree[pos] >= width:
            return pos - self.n
        return -1

def nfdh(tasks, n_machines):
    levels = []
    current_level = None
    
    for task in tasks:
        if current_level is None or current_level.free_space() < task.r:
            current_level = Level(task.t, n_machines, 1)
            levels.append(current_level)
            current_level.start_machine_idx = 1
        
        start_m = current_level.start_machine_idx + current_level.used
        task.machines = list(range(start_m + 1, start_m + task.r + 1))
        
        current_level.used += task.r
        current_level.tasks.append(task)
        task.tau = sum(l.height for l in levels[:-1])
        
    return levels

def ffdh(tasks, n_machines):
    levels = []
    st = SegmentTree(len(tasks))
    
    for task in tasks:
        level_idx = -1
        
        if len(levels) > 0:
            level_idx = st.find_first_fit(task.r)
        
        if level_idx == -1 or level_idx >= len(levels):
            level_idx = len(levels)
            new_level = Level(task.t, n_machines, 1)
            levels.append(new_level)
            st.update(level_idx, new_level.free_space())
        
        lvl = levels[level_idx]
        start_m = lvl.start_machine_idx + lvl.used
        task.machines = list(range(start_m + 1, start_m + task.r + 1))
        
        lvl.used += task.r
        lvl.tasks.append(task)
        task.tau = sum(l.height for l in levels[:level_idx])
        
        st.update(level_idx, lvl.free_space())

    return levels

def calculate_metrics(levels, n_machines, tasks):
    if not levels:
        return 0, 0.0
    
    t_s = sum(l.height for l in levels)
    sum_area = sum(t.t * t.r for t in tasks)
    t_prime = sum_area / n_machines
    
    epsilon = (t_s - t_prime) / t_prime if t_prime > 0 else 0.0
    return t_s, epsilon

def generate_random_tasks(m, n):
    tasks = []
    for i in range(m):
        r = random.randint(1, n)
        t = random.randint(1, 100)
        tasks.append(Task(i, t, r))
    return tasks

def parse_llnl_log(filename, m_limit):
    tasks = []
    count = 0
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.startswith(';'): continue
                parts = line.split()
                if len(parts) < 8: continue
                try:
                    t = int(parts[2])
                    r = int(parts[7])
                    if t <= 0 or r <= 0: continue
                    tasks.append(Task(count, t, r))
                    count += 1
                    if count >= m_limit:
                        break
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
    return tasks

def save_schedule(tasks, filename):
    with open(filename, 'w') as f:
        f.write("ID;T;R;Tau;Machines\n")
        for t in tasks:
            machines_str = ",".join(map(str, t.machines))
            f.write(f"{t.id};{t.t};{t.r};{t.tau};{machines_str}\n")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--exp":
        exp_type = sys.argv[2]
        
        if exp_type not in ['time', 'accuracy']:
            print(f"Неизвестный тип эксперимента: {exp_type}")
            print("Используйте: --exp time или --exp accuracy")
            sys.exit(1)
        
        print(f"Запуск экспериментов ({exp_type})...")
        results = []
        
        m_values = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
        n_values = [1024, 4096] if exp_type == 'time' else [1024]
        trials = 10
        
        for n in n_values:
            for m in m_values:
                eps_nfdh = []
                eps_ffdh = []
                time_nfdh = []
                time_ffdh = []
                
                for _ in range(trials):
                    tasks = generate_random_tasks(m, n)
                    sorted_tasks = counting_sort_tasks(tasks, max_t=100)
                    
                    # NFDH
                    t0 = time.time()
                    levels = nfdh(sorted_tasks, n)
                    t1 = time.time()
                    _, eps = calculate_metrics(levels, n, tasks)
                    time_nfdh.append(t1 - t0)
                    eps_nfdh.append(eps)
                    
                    # FFDH
                    tasks2 = generate_random_tasks(m, n)
                    sorted_tasks2 = counting_sort_tasks(tasks2, max_t=100)
                    t0 = time.time()
                    levels = ffdh(sorted_tasks2, n)
                    t1 = time.time()
                    _, eps = calculate_metrics(levels, n, tasks2)
                    time_ffdh.append(t1 - t0)
                    eps_ffdh.append(eps)
                
                avg_t_nfdh = sum(time_nfdh) / trials
                avg_t_ffdh = sum(time_ffdh) / trials
                avg_e_nfdh = sum(eps_nfdh) / trials
                avg_e_ffdh = sum(eps_ffdh) / trials
                
                results.append({
                    'm': m, 'n': n, 
                    't_nfdh': avg_t_nfdh, 't_ffdh': avg_t_ffdh,
                    'e_nfdh': avg_e_nfdh, 'e_ffdh': avg_e_ffdh
                })
                print(f"m={m}, n={n} -> T(NFDH):{avg_t_nfdh:.4f}, T(FFDH):{avg_t_ffdh:.4f}, E(NFDH):{avg_e_nfdh:.4f}, E(FFDH):{avg_e_ffdh:.4f}")

        with open('experiment_results.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['m', 'n', 't_nfdh', 't_ffdh', 'e_nfdh', 'e_ffdh'])
            writer.writeheader()
            writer.writerows(results)
        print("Результаты сохранены в experiment_results.csv")

    elif len(sys.argv) >= 4:
        filename = sys.argv[1]
        try:
            n_machines = int(sys.argv[2])
        except ValueError:
            print(f"Ошибка: второй аргумент должен быть числом (кол-во машин), получено: {sys.argv[2]}")
            sys.exit(1)
        algo_name = sys.argv[3].upper()
        
        tasks = []
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                parts = line.split()
                if len(parts) >= 2:
                    t, r = int(parts[0]), int(parts[1])
                    tasks.append(Task(i, t, r))
        
        sorted_tasks = counting_sort_tasks(tasks, max_t=100000)
        
        start = time.time()
        if algo_name == 'NFDH':
            levels = nfdh(sorted_tasks, n_machines)
        elif algo_name == 'FFDH':
            levels = ffdh(sorted_tasks, n_machines)
        else:
            print("Неизвестный алгоритм. Используйте NFDH или FFDH")
            sys.exit(1)
        end = time.time()
        
        t_s, eps = calculate_metrics(levels, n_machines, tasks)
        exec_time = end - start
        
        print(f"Алгоритм: {algo_name}")
        print(f"Задач: {len(tasks)}, Машин: {n_machines}")
        print(f"T(S): {t_s}")
        print(f"Epsilon: {eps:.6f}")
        print(f"Время выполнения: {exec_time:.6f} сек")
        
        save_schedule(tasks, f"schedule_{algo_name}.csv")
        print(f"Расписание сохранено в schedule_{algo_name}.csv")

    else:
        print("Использование:")
        print("  python main.py <input_file> <n_machines> <NFDH|FFDH>")
        print("  python main.py --exp time")
        print("  python main.py --exp accuracy")
        print("Пример входного файла (tasks.txt):")
        print("  50 10")
        print("  30 20")
        print("  (время количество_машин)")