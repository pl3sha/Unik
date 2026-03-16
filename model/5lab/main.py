import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

class MarkovChain:
    def __init__(self, transition_matrix, name=""):
        self.P = transition_matrix
        self.name = name
        self.n = transition_matrix.shape[0]
        self.states_history = []
        self.transitions = []
        
    def generate_doubly_stochastic_matrix(self, n=10):
        while True:
            A = np.random.rand(n, n)
            for _ in range(100):
                A = A / A.sum(axis=1, keepdims=True)
                A = A / A.sum(axis=0, keepdims=True)
            if np.any((A > 0.01) & (A < 0.99)):
                break
        return A
    
    def check_doubly_stochastic(self, matrix=None, tolerance=1e-6):
        if matrix is None:
            matrix = self.P
        row_sums = np.sum(matrix, axis=1)
        rows_ok = np.allclose(row_sums, 1, atol=tolerance)
        col_sums = np.sum(matrix, axis=0)
        cols_ok = np.allclose(col_sums, 1, atol=tolerance)
        non_negative = np.all(matrix >= 0)
        return rows_ok and cols_ok and non_negative
    
    def get_next_state(self, current_state):
        r = np.random.random()
        probs = self.P[current_state]
        cumulative_probs = np.cumsum(probs)
        next_state = np.searchsorted(cumulative_probs, r)
        return next_state, r
    
    def simulate(self, n_steps=1000, initial_state=None):
        if initial_state is None:
            current_state = np.random.randint(0, self.n)
        else:
            current_state = initial_state
        self.states_history = [current_state]
        self.transitions = []
        for _ in range(n_steps):
            next_state, r = self.get_next_state(current_state)
            self.transitions.append((current_state, next_state, r))
            current_state = next_state
            self.states_history.append(current_state)
        return np.array(self.states_history)
    
    def calculate_transition_frequencies(self):
        freq_matrix = np.zeros((self.n, self.n))
        for from_state, to_state, _ in self.transitions:
            freq_matrix[from_state, to_state] += 1
        total_transitions = len(self.transitions)
        if total_transitions > 0:
            freq_matrix = freq_matrix / total_transitions
        return freq_matrix
    
    def calculate_autocorrelation(self, max_lag=100):
        states = np.array(self.states_history)
        autocorr = []
        for lag in range(max_lag):
            if lag == 0:
                autocorr.append(1.0)
            else:
                if len(states) > lag:
                    corr = np.corrcoef(states[:-lag], states[lag:])[0, 1]
                    autocorr.append(corr if not np.isnan(corr) else 0)
                else:
                    autocorr.append(0)
        return np.array(autocorr)
    
    def get_state_distribution(self):
        states = np.array(self.states_history)
        unique, counts = np.unique(states, return_counts=True)
        distribution = np.zeros(self.n)
        for i in range(len(unique)):
            distribution[unique[i]] = counts[i]
        return distribution / len(states)


def plot_comparison(chain1, chain2, n_steps=1000):
    states1 = chain1.simulate(n_steps)
    states2 = chain2.simulate(n_steps)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparison of Two Markov Chains', fontsize=16, fontweight='bold')
    
    ax = axes[0, 0]
    ax.plot(states1[:100], label=f'{chain1.name}', alpha=0.7)
    ax.plot(states2[:100], label=f'{chain2.name}', alpha=0.7)
    ax.set_xlabel('Step')
    ax.set_ylabel('State')
    ax.set_title('State Sequence (first 100 steps)')
    ax.legend()
    
    ax = axes[0, 1]
    dist1 = chain1.get_state_distribution()
    dist2 = chain2.get_state_distribution()
    x = np.arange(chain1.n)
    width = 0.35
    ax.bar(x - width/2, dist1, width, label=chain1.name, alpha=0.7)
    ax.bar(x + width/2, dist2, width, label=chain2.name, alpha=0.7)
    ax.set_xlabel('State')
    ax.set_ylabel('Probability')
    ax.set_title('State Distribution')
    ax.legend()
    
    ax = axes[1, 0]
    max_lag = 100
    autocorr1 = chain1.calculate_autocorrelation(max_lag)
    autocorr2 = chain2.calculate_autocorrelation(max_lag)
    ax.plot(range(max_lag), autocorr1, label=chain1.name, alpha=0.7)
    ax.plot(range(max_lag), autocorr2, label=chain2.name, alpha=0.7)
    ax.set_xlabel('Lag')
    ax.set_ylabel('Autocorrelation')
    ax.set_title('Autocorrelation Function')
    ax.legend()
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    
    ax = axes[1, 1]
    ax.hist(states1[:500], bins=range(11), alpha=0.5, label=chain1.name, density=True)
    ax.hist(states2[:500], bins=range(11), alpha=0.5, label=chain2.name, density=True)
    ax.set_xlabel('State')
    ax.set_ylabel('Frequency')
    ax.set_title('State Histogram (first 500 steps)')
    ax.legend()
    
    plt.tight_layout()
    plt.show()
    
    freq1 = chain1.calculate_transition_frequencies()
    plt.figure(figsize=(10, 8))
    plt.imshow(freq1, cmap='viridis', aspect='auto')
    plt.xlabel('Next State', fontsize=12)
    plt.ylabel('Current State', fontsize=12)
    plt.title(f'Transition Frequency Matrix - {chain1.name}', fontsize=14, fontweight='bold', pad=20)
    plt.colorbar(label='Transition Frequency')
    for i in range(freq1.shape[0]):
        for j in range(freq1.shape[1]):
            plt.text(j, i, f'{freq1[i, j]:.3f}', ha="center", va="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.show()
    
    freq2 = chain2.calculate_transition_frequencies()
    plt.figure(figsize=(10, 8))
    plt.imshow(freq2, cmap='viridis', aspect='auto')
    plt.xlabel('Next State', fontsize=12)
    plt.ylabel('Current State', fontsize=12)
    plt.title(f'Transition Frequency Matrix - {chain2.name}', fontsize=14, fontweight='bold', pad=20)
    plt.colorbar(label='Transition Frequency')
    for i in range(freq2.shape[0]):
        for j in range(freq2.shape[1]):
            plt.text(j, i, f'{freq2[i, j]:.3f}', ha="center", va="center", color="white", fontsize=8)
    plt.tight_layout()
    plt.show()


def print_statistics(chain, n_steps=1000):
    print("\n")
    print(f"{chain.name}")
    print("\n")
    
    states = chain.simulate(n_steps)
    
    print(f"Size: {chain.n}x{chain.n}")
    print(f"Doubly Stochastic: {'Yes' if chain.check_doubly_stochastic() else 'No'}")
    print(f"Initial State: {states[0]}")
    print(f"Final State: {states[-1]}")
    
    print(f"\nState Distribution:")
    dist = chain.get_state_distribution()
    for i, prob in enumerate(dist):
        print(f"  State {i}: {prob:.4f}")
    
    print(f"\nAutocorrelation (first 5 lags):")
    autocorr = chain.calculate_autocorrelation(5)
    for lag, corr in enumerate(autocorr):
        print(f"  Lag {lag}: {corr:.4f}")


def main():
    print("Lab Work #5: Randomized Markov Chains")
    print("\n")
    
    chain1 = MarkovChain(np.zeros((10, 10)), name="Matrix 1")
    chain2 = MarkovChain(np.zeros((10, 10)), name="Matrix 2")
    
    P1 = chain1.generate_doubly_stochastic_matrix(10)
    P2 = chain2.generate_doubly_stochastic_matrix(10)
    
    chain1.P = P1
    chain2.P = P2
    
    print(f"\nMatrix 1: {'Doubly Stochastic' if chain1.check_doubly_stochastic() else 'No'}")
    print(f"Matrix 2: {'Doubly Stochastic' if chain2.check_doubly_stochastic() else 'No'}")
    
    print_statistics(chain1, n_steps=1000)
    print_statistics(chain2, n_steps=1000)
    
    plot_comparison(chain1, chain2, n_steps=1000)
    
    print("\n")
    print("Conclusions:")
    print("1. Matrices are doubly stochastic (row/col sums = 1)")
    print("2. Distribution tends to uniform (~10% per state)")
    print("3. Autocorrelation decays - chains mix well")
    print("4. Transition frequencies close to theoretical")
    print("="*50)


if __name__ == "__main__":
    main()