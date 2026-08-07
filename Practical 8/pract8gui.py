import heapq
import tkinter as tk
from tkinter import ttk, messagebox


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, z):
        y = z.left
        t3 = y.right

        y.right = z
        z.left = t3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def left_rotate(self, z):
        y = z.right
        t2 = y.left

        y.left = z
        z.right = t2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, root, key):
        if not root:
            return AVLNode(key)

        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(
            self.get_height(root.left),
            self.get_height(root.right)
        )

        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def preorder(self, root, result):
        if root:
            result.append(str(root.key))
            self.preorder(root.left, result)
            self.preorder(root.right, result)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AVL Tree, Heap & Priority Queue")
        self.root.geometry("700x650")

        self.avl = AVLTree()
        self.avl_root = None
        self.tasks = []

        title = tk.Label(
            root,
            text="AVL Tree, Heap & Priority Queue",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        frame1 = ttk.LabelFrame(root, text="AVL Tree")
        frame1.pack(fill="x", padx=10, pady=5)

        self.avl_entry = ttk.Entry(frame1, width=20)
        self.avl_entry.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(
            frame1,
            text="Insert",
            command=self.insert_avl
        ).grid(row=0, column=1, padx=5)

        self.avl_result = tk.Text(frame1, height=4, width=70)
        self.avl_result.grid(row=1, column=0, columnspan=3, pady=5)

        frame2 = ttk.LabelFrame(root, text="Heap")
        frame2.pack(fill="x", padx=10, pady=5)

        ttk.Label(
            frame2,
            text="Enter numbers (comma separated)"
        ).pack()

        self.heap_entry = ttk.Entry(frame2, width=50)
        self.heap_entry.pack(pady=5)

        ttk.Button(
            frame2,
            text="Create Heap",
            command=self.create_heap
        ).pack()

        self.heap_result = tk.Text(frame2, height=5, width=70)
        self.heap_result.pack(pady=5)

        frame3 = ttk.LabelFrame(root, text="Priority Queue")
        frame3.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame3, text="Priority").grid(row=0, column=0)

        self.priority_entry = ttk.Entry(frame3, width=10)
        self.priority_entry.grid(row=0, column=1)

        ttk.Label(frame3, text="Task").grid(row=0, column=2)

        self.task_entry = ttk.Entry(frame3, width=30)
        self.task_entry.grid(row=0, column=3)

        ttk.Button(
            frame3,
            text="Add Task",
            command=self.add_task
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            frame3,
            text="Process Tasks",
            command=self.process_tasks
        ).grid(row=1, column=0, columnspan=5, pady=5)

        self.task_result = tk.Text(frame3, height=8, width=70)
        self.task_result.grid(row=2, column=0, columnspan=5)

    def insert_avl(self):
        try:
            value = int(self.avl_entry.get())
            self.avl_root = self.avl.insert(self.avl_root, value)

            result = []
            self.avl.preorder(self.avl_root, result)

            self.avl_result.delete("1.0", tk.END)
            self.avl_result.insert(
                tk.END,
                "Preorder Traversal:\n" + " ".join(result)
            )

            self.avl_entry.delete(0, tk.END)

        except:
            messagebox.showerror("Error", "Enter a valid integer.")

    def create_heap(self):
        try:
            nums = list(map(int, self.heap_entry.get().split(",")))

            min_heap = nums.copy()
            heapq.heapify(min_heap)

            max_heap = [-x for x in nums]
            heapq.heapify(max_heap)

            self.heap_result.delete("1.0", tk.END)
            self.heap_result.insert(tk.END, f"Min Heap : {min_heap}\n")
            self.heap_result.insert(
                tk.END,
                f"Max Heap : {[-x for x in max_heap]}"
            )

        except:
            messagebox.showerror(
                "Error",
                "Enter numbers separated by commas."
            )

    def add_task(self):
        try:
            priority = int(self.priority_entry.get())
            task = self.task_entry.get()

            heapq.heappush(self.tasks, (priority, task))

            self.priority_entry.delete(0, tk.END)
            self.task_entry.delete(0, tk.END)

            messagebox.showinfo("Success", "Task Added")

        except:
            messagebox.showerror("Error", "Invalid Input")

    def process_tasks(self):
        self.task_result.delete("1.0", tk.END)

        while self.tasks:
            priority, task = heapq.heappop(self.tasks)
            self.task_result.insert(
                tk.END,
                f"Priority {priority} → {task}\n"
            )


root = tk.Tk()
App(root)
root.mainloop()
