import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].append(vertex2)
            self.graph[vertex2].append(vertex1)

    def dfs_tree(self, start):
        visited = set()
        dfs_tree = defaultdict(list)

        def dfs(v):
            visited.add(v)

            for neighbor in self.graph[v]:
                if neighbor not in visited:
                    dfs_tree[v].append(neighbor)
                    dfs(neighbor)

        dfs(start)
        return dfs_tree

    def display(self):
        for vertex, edges in self.graph.items():
            print(f"{vertex}: {edges}")

    def visualize(self, dfs_tree=None):
        G = nx.Graph(self.graph)
        pos = nx.spring_layout(G)

        plt.figure(figsize=(12, 6))

        plt.subplot(121)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            edge_color="gray",
            node_size=1000,
            font_size=15,
            font_weight="bold"
        )
        plt.title("Graph")

        if dfs_tree:
            T = nx.DiGraph(dfs_tree)
            pos_tree = nx.spring_layout(T)

            plt.subplot(122)
            nx.draw(
                T,
                pos_tree,
                with_labels=True,
                node_color="lightgreen",
                edge_color="blue",
                node_size=1000,
                font_size=15,
                font_weight="bold",
                arrows=True
            )
            plt.title("DFS Tree")

        plt.show()


if __name__ == "__main__":
    g = Graph()

    for v in ["A", "B", "C", "D", "E", "F"]:
        g.add_vertex(v)

    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    g.add_edge("C", "F")

    print("Graph:")
    g.display()

    start_vertex = "A"
    dfs_tree = g.dfs_tree(start_vertex)

    g.visualize(dfs_tree)
