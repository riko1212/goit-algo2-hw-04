from collections import deque, defaultdict

class MaxFlow:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, capacity):
        self.graph[u][v] = capacity
        if v not in self.graph or u not in self.graph[v]:
            self.graph[v][u] = 0  # зворотня місткість для алгоритму

    def bfs(self, source, sink, parent):
        visited = set()
        queue = deque([source])
        visited.add(source)
        while queue:
            u = queue.popleft()
            for v, cap in self.graph[u].items():
                if v not in visited and cap > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def edmonds_karp(self, source, sink):
        parent = {}
        max_flow = 0
        while self.bfs(source, sink, parent):
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]
            max_flow += path_flow
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]
        return max_flow

# Створення графа відповідно до завдання
mf = MaxFlow()

# Терминали → Склади
edges = [
    ("T1", "S1", 25), ("T1", "S2", 20), ("T1", "S3", 15),
    ("T2", "S2", 10), ("T2", "S3", 15), ("T2", "S4", 30),
    # Склади → Магазини
    ("S1", "M1", 15), ("S1", "M2", 10), ("S1", "M3", 20),
    ("S2", "M4", 15), ("S2", "M5", 10), ("S2", "M6", 25),
    ("S3", "M7", 20), ("S3", "M8", 15), ("S3", "M9", 10),
    ("S4", "M10", 20), ("S4", "M11", 10), ("S4", "M12", 15),
    ("S4", "M13", 5), ("S4", "M14", 10),
]

for u, v, cap in edges:
    mf.add_edge(u, v, cap)

# Додаткові суперджерело та суперсток для спрощення
for t in ["T1", "T2"]:
    mf.add_edge("Source", t, float('inf'))

for m in [f"M{i}" for i in range(1,15)]:
    mf.add_edge(m, "Sink", float('inf'))

max_flow = mf.edmonds_karp("Source", "Sink")
print("Максимальний потік у мережі:", max_flow)