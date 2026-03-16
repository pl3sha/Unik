import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import random

class GraphBuilder:
    def __init__(self, points=100, space=100, seed=None):
        self.points = points
        self.space = space
        if seed:
            np.random.seed(seed)
            random.seed(seed)
        self.coords = np.random.rand(points, 2) * space
        self.graph = nx.Graph()
        for i in range(points):
            self.graph.add_node(i, xy=self.coords[i])
        self.parent = {i: i for i in range(points)}
        self.deg_limit = 5
        self.dist_limit = 40.0
        self.alpha = 0.15
        self.gamma = 2.0
        self.power = 1.0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def connect(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx != ry:
            self.parent[rx] = ry
            return True
        return False

    def measure(self, i, j):
        return np.sqrt(sum((self.coords[i] - self.coords[j]) ** 2))

    def get_candidates(self, node, formula):
        opts = []
        vals = []
        if self.graph.degree[node] >= self.deg_limit:
            return [], []
        for other in range(self.points):
            if other == node:
                continue
            if self.find(node) == self.find(other):
                continue
            if self.graph.degree[other] >= self.deg_limit:
                continue
            d = self.measure(node, other)
            if d > self.dist_limit or d < 0.01:
                continue
            if formula == 'exp':
                w = np.exp(-self.alpha * (d ** self.power))
            else:
                w = 1.0 / (d ** self.gamma)
            if np.isfinite(w) and w > 0:
                opts.append(other)
                vals.append(w)
        return opts, vals

    def construct(self, formula, max_iter=5000):
        added = 0
        goal = self.points - 1
        for _ in range(max_iter):
            if added >= goal:
                break
            src = random.randint(0, self.points - 1)
            targets, weights = self.get_candidates(src, formula)
            if not targets or not weights:
                continue
            s = sum(weights)
            if s <= 0 or not np.isfinite(s):
                continue
            probs = [w / s for w in weights]
            if not np.all(np.isfinite(probs)):
                continue
            dst = np.random.choice(targets, p=probs)
            self.graph.add_edge(src, dst)
            self.connect(src, dst)
            added += 1
        return self.graph

    def render(self, path, caption):
        positions = {n: self.graph.nodes[n]['xy'] for n in self.graph.nodes()}
        plt.figure(figsize=(9, 9))
        nx.draw(self.graph, positions, node_size=40, node_color='#FF9999',
                with_labels=False, edge_color='#6699CC', width=0.6, alpha=0.7)
        plt.title(caption, fontsize=10)
        plt.axis('equal')
        plt.axis('off')
        plt.savefig(path, dpi=120, bbox_inches='tight')
        plt.close()

def run():
    formulas = [('exp', 'Exponential'), ('pow', 'Power Law')]
    total_graphs = 0
    target_graphs = 20
    
    for fcode, fname in formulas:
        if total_graphs >= target_graphs:
            break
        for run in range(1, 11):
            sd = run * 77 + random.randint(0, 100)
            
            b_val = round(np.random.uniform(1.0, 3.0), 2)
            d_val = 40.0
            
            builder = GraphBuilder(points=100, space=100, seed=sd)
            builder.gamma = b_val
            builder.power = b_val
            builder.dist_limit = d_val
        
            if fcode == 'exp':
                a_val = round(np.random.uniform(0.1, 0.25), 3)
                builder.alpha = a_val
                label = f"{fname}: a={a_val}, b={b_val}, dist={d_val}"
            else:
                builder.alpha = 1.0 
                label = f"{fname}: b={b_val}, dist={d_val}"
            
            builder.construct(formula=fcode)
            
            outfile = f"run_{fcode}_{run:02d}.png"
            builder.render(outfile, label)
            
            total_graphs += 1
            if total_graphs >= target_graphs:
                break

if __name__ == "__main__":
    run()