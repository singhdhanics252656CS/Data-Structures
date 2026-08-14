import tkinter as tk
from tkinter import messagebox
from collections import deque, defaultdict
import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_vertex(self, v):
        self.graph[v]

    def add_edge(self, a, b):
        self.graph[a].append(b)
        self.graph[b].append(a)

    def bfs(self, start):
        visited, tree, q = {start}, defaultdict(list), deque([start])
        while q:
            v = q.popleft()
            for n in self.graph[v]:
                if n not in visited:
                    visited.add(n)
                    tree[v].append(n)
                    q.append(n)
        return tree

    def dfs(self, start):
        visited, tree = set(), defaultdict(list)

        def visit(v):
            visited.add(v)
            for n in self.graph[v]:
                if n not in visited:
                    tree[v].append(n)
                    visit(n)

        visit(start)
        return tree


def hash_insert():
    try:
        size = int(size_entry.get())
        data = map(int, data_entry.get().split())
        table = [None] * size

        for x in data:
            i = x % size
            start = i
            while table[i] is not None:
                i = (i + 1) % size
                if i == start:
                    raise ValueError("Hash table is full")
            table[i] = x

        output.delete("1.0", tk.END)
        for i, x in enumerate(table):
            output.insert(tk.END, f"Index {i}: {x}\n")

    except ValueError as e:
        messagebox.showerror("Error", str(e))


def graph_run(kind):
    try:
        g = Graph()

        for v in vertices.get().split():
            g.add_vertex(v)

        for edge in edges.get().split(","):
            a, b = edge.split()
            g.add_edge(a, b)

        start = start_entry.get()

        if start not in g.graph:
            raise ValueError("Invalid starting vertex")

        tree = g.bfs(start) if kind == "BFS" else g.dfs(start)

        output.delete("1.0", tk.END)
        output.insert(tk.END, f"{kind} Tree\n\n")

        for v in tree:
            output.insert(tk.END, f"{v} -> {tree[v]}\n")

        if kind == "DFS":
            G = nx.Graph(g.graph)
            T = nx.DiGraph(tree)

            plt.figure(figsize=(8, 4))

            plt.subplot(121)
            nx.draw(
                G,
                with_labels=True,
                node_color="#D8B4FE",
                node_size=1200
            )
            plt.title("Graph")

            plt.subplot(122)
            nx.draw(
                T,
                with_labels=True,
                node_color="#FDBA74",
                node_size=1200,
                arrows=True
            )
            plt.title("DFS Tree")

            plt.show()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid graph data."
        )


def clear():
    output.delete("1.0", tk.END)


root = tk.Tk()
root.title("Data Structures")
root.geometry("700x550")
root.configure(bg="#FFF7ED")


tk.Label(
    root,
    text="Data Structures",
    font=("Georgia", 24, "bold"),
    bg="#FFF7ED",
    fg="#6B21A8"
).pack(pady=20)


menu = tk.Frame(root, bg="#FFF7ED")
menu.pack()

content = tk.Frame(
    root,
    bg="white",
    padx=30,
    pady=20
)
content.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=15
)


def page(title):
    for w in content.winfo_children():
        w.destroy()

    tk.Label(
        content,
        text=title,
        font=("Georgia", 18, "bold"),
        bg="white",
        fg="#6B21A8"
    ).pack(pady=10)


def hash_page():
    page("Linear Probing")

    tk.Label(
        content,
        text="Hash Table Size",
        bg="white"
    ).pack()

    global size_entry
    size_entry = tk.Entry(content, width=35)
    size_entry.pack(pady=5)

    tk.Label(
        content,
        text="Data",
        bg="white"
    ).pack()

    global data_entry
    data_entry = tk.Entry(content, width=35)
    data_entry.pack(pady=5)

    tk.Button(
        content,
        text="Insert",
        command=hash_insert,
        bg="#8B5CF6",
        fg="white",
        width=15,
        relief="flat"
    ).pack(pady=10)


def graph_page(kind):
    page(kind)

    global vertices, edges, start_entry

    tk.Label(
        content,
        text="Vertices",
        bg="white"
    ).pack()

    vertices = tk.Entry(content, width=35)
    vertices.pack(pady=4)

    tk.Label(
        content,
        text="Edges",
        bg="white"
    ).pack()

    edges = tk.Entry(content, width=35)
    edges.pack(pady=4)

    tk.Label(
        content,
        text="Start Vertex",
        bg="white"
    ).pack()

    start_entry = tk.Entry(content, width=35)
    start_entry.pack(pady=4)

    tk.Button(
        content,
        text=f"Run {kind}",
        command=lambda: graph_run(kind),
        bg="#8B5CF6",
        fg="white",
        width=15,
        relief="flat"
    ).pack(pady=10)


for text, command in [
    ("Hash", hash_page),
    ("BFS", lambda: graph_page("BFS")),
    ("DFS", lambda: graph_page("DFS"))
]:
    tk.Button(
        menu,
        text=text,
        command=command,
        bg="#E9D5FF",
        fg="#6B21A8",
        width=12,
        relief="flat"
    ).pack(side="left", padx=5)


output = tk.Text(
    root,
    height=8,
    font=("Consolas", 11),
    bg="#FAF5FF",
    fg="#3B0764"
)
output.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Button(
    root,
    text="Clear Output",
    command=clear,
    bg="#F1F5F9",
    fg="#475569",
    width=15,
    relief="flat"
).pack(pady=5)


hash_page()
root.mainloop()
